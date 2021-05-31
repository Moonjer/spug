# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.

from django.db.models import F
from django.http.response import HttpResponseBadRequest
from django.views.generic import View
from openpyxl import load_workbook
from paramiko.ssh_exception import BadAuthenticationType

from apps.account.models import Role
from apps.app.models import Deploy
from apps.host.models import Host, Datacenter, Zone, DeviceVersion, OperatingSystem
from apps.monitor.models import Detection
from apps.schedule.models import Task
from apps.setting.utils import AppSetting
from libs import human_datetime, AttrDict
from libs import json_response, JsonParser, Argument
from libs.ssh import SSH, AuthenticationException


class HostView(View):
    def get(self, request):
        host_id = request.GET.get('id')
        if host_id:
            if not request.user.has_host_perm(host_id):
                return json_response(error='无权访问该主机，请联系管理员')
            return json_response(Host.objects.get(pk=host_id))
        hosts = Host.objects.filter(deleted_by_id__isnull=True)
        host_machines = Host.objects.filter(deleted_by_id__isnull=True, type__exact=1)
        datacenters = [x.to_dict() for x in Datacenter.objects.all()]
        zones = [x.to_dict() for x in Zone.objects.all()]
        device_versions = [x.to_dict() for x in DeviceVersion.objects.all()]
        operating_systems = [x.to_dict() for x in OperatingSystem.objects.all()]
        perms = [x.id for x in hosts] if request.user.is_supper else request.user.host_perms

        return json_response({'hosts': [x.to_dict() for x in hosts], 'datacenters': datacenters, 'zones': zones,
                              'device_versions': device_versions,
                              'operating_systems': operating_systems,
                              'perms': perms, 'host_machines': [x.to_dict() for x in host_machines]})

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('type', type=int, help='请选择类型'),
            Argument('cpu_core_num', type=int, help='请输入cpu核数'),
            Argument('mem_num', type=int, help='请输入内存大小'),
            Argument('hard_disk', type=int, help='请输入硬盘大小'),
            Argument('datacenter', required=False, help='请选择机房'),
            Argument('device_version', required=False, help='请选择型号'),
            Argument('operating_system', required=False, help='请选择操作系统'),
            Argument('host_machine', required=False, help='请选择宿主机'),
            Argument('zone', help='请输入主机类型'),
            Argument('name', help='请输入主机名称'),
            Argument('hostname', handler=str.strip, help='请输入主机名或IP'),
            Argument('pkey', required=False),
            Argument('desc', required=False),
        ).parse(request.body)
        if error is None:
            # if valid_ssh(form.hostname, form.port, form.username, password=form.pop('password'),
            #              pkey=form.pkey) is False:
            #     return json_response('auth fail')

            if form.id:
                Host.objects.filter(pk=form.pop('id')).update(**form)
            elif Host.objects.filter(name=form.name, deleted_by_id__isnull=True).exists():
                return json_response(error=f'已存在的主机名称【{form.name}】')
            else:
                host = Host.objects.create(created_by=request.user, **form)
                if request.user.role:
                    request.user.role.add_host_perm(host.id)
        return json_response(error=error)

    def patch(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('zone', help='请输入主机类别')
        ).parse(request.body)
        if error is None:
            host = Host.objects.filter(pk=form.id).first()
            if not host:
                return json_response(error='未找到指定主机')
            count = Host.objects.filter(zone=host.zone, deleted_by_id__isnull=True).update(zone=form.zone)
            return json_response(count)
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            deploy = Deploy.objects.filter(host_ids__regex=fr'[^0-9]{form.id}[^0-9]').annotate(
                app_name=F('app__name'),
                env_name=F('env__name')
            ).first()
            if deploy:
                return json_response(error=f'应用【{deploy.app_name}】在【{deploy.env_name}】的发布配置关联了该主机，请解除关联后再尝试删除该主机')
            task = Task.objects.filter(targets__regex=fr'[^0-9]{form.id}[^0-9]').first()
            if task:
                return json_response(error=f'任务计划中的任务【{task.name}】关联了该主机，请解除关联后再尝试删除该主机')
            detection = Detection.objects.filter(type__in=('3', '4'), addr=form.id).first()
            if detection:
                return json_response(error=f'监控中心的任务【{detection.name}】关联了该主机，请解除关联后再尝试删除该主机')
            role = Role.objects.filter(host_perms__regex=fr'[^0-9]{form.id}[^0-9]').first()
            if role:
                return json_response(error=f'角色【{role.name}】的主机权限关联了该主机，请解除关联后再尝试删除该主机')
            Host.objects.filter(pk=form.id).update(
                deleted_at=human_datetime(),
                deleted_by=request.user,
            )
        return json_response(error=error)


def post_import(request):
    password = request.POST.get('password')
    file = request.FILES['file']
    ws = load_workbook(file, read_only=True)['Sheet1']
    summary = {'invalid': [], 'skip': [], 'fail': [], 'network': [], 'repeat': [], 'success': [], 'error': []}

    # 准备字典
    datacenters = {}
    for datacenter in Datacenter.objects.all():
        datacenters[datacenter.name] = datacenter
    zones = {}
    for zone in Zone.objects.all():
        zones[zone.name] = zone
    host_type = {
        '物理机': 1,
        '虚拟机': 2
    }
    device_versions = {}
    for device_version in DeviceVersion.objects.all():
        device_versions[device_version.name] = device_version
    operating_systems = {}
    for operating_system in OperatingSystem.objects.all():
        operating_systems[operating_system.name] = operating_system

    for i, row in enumerate(ws.rows):
        if i == 0:  # 第1行是表头 略过
            continue
        if not all([row[x].value for x in range(5)]):
            summary['invalid'].append(i)
            continue
        data = AttrDict(
            name=row[0].value,
            hostname=row[1].value,
            datacenter=datacenters[row[2].value],
            zone=zones[row[3].value],
            cpu_core_num=row[4].value,
            mem_num=row[5].value,
            hard_disk=row[6].value,
            type=host_type[row[7].value],
            desc=row[11].value
        )
        if data['type'] == 1:
            data['device_version'] = device_versions[row[8].value]
        else:
            data['host_machine'] = Host.objects.get(name=row[9].value)
            data['operating_system'] = operating_systems[row[10].value]

        if Host.objects.filter(hostname=data.hostname, deleted_by_id__isnull=True).exists():
            summary['skip'].append(i)
            continue
        # try:
        #     if valid_ssh(data.hostname, data.port, data.username, data.pop('password') or password, None,
        #                  False) is False:
        #         summary['fail'].append(i)
        #         continue
        # except AuthenticationException:
        #     summary['fail'].append(i)
        #     continue
        # except socket.error:
        #     summary['network'].append(i)
        #     continue
        # except Exception:
        #     summary['error'].append(i)
        #     continue
        if Host.objects.filter(name=data.name, deleted_by_id__isnull=True).exists():
            summary['repeat'].append(i)
            continue
        host = Host.objects.create(created_by=request.user, **data)
        if request.user.role:
            request.user.role.add_host_perm(host.id)
        summary['success'].append(i)
    return json_response(summary)


def valid_ssh(hostname, port, username, password=None, pkey=None, with_expect=True):
    try:
        private_key = AppSetting.get('private_key')
        public_key = AppSetting.get('public_key')
    except KeyError:
        private_key, public_key = SSH.generate_key()
        AppSetting.set('private_key', private_key, 'ssh private key')
        AppSetting.set('public_key', public_key, 'ssh public key')
    if password:
        _cli = SSH(hostname, port, username, password=str(password))
        _cli.add_public_key(public_key)
    if pkey:
        private_key = pkey
    try:
        cli = SSH(hostname, port, username, private_key)
        cli.ping()
    except BadAuthenticationType:
        if with_expect:
            raise TypeError('该主机不支持密钥认证，请参考官方文档，错误代码：E01')
        return False
    except AuthenticationException:
        if password and with_expect:
            raise ValueError('密钥认证失败，请参考官方文档，错误代码：E02')
        return False
    return True


def post_parse(request):
    file = request.FILES['file']
    if file:
        data = file.read()
        return json_response(data.decode())
    else:
        return HttpResponseBadRequest()
