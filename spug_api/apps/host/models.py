# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models

from apps.account.models import User
from apps.setting.utils import AppSetting
from libs import ModelMixin, human_datetime
from libs.ssh import SSH


class Datacenter(models.Model, ModelMixin):
    name = models.CharField(max_length=50)

    def __repr__(self):
        return '<Datacenter %r>' % self.name

    class Meta:
        db_table = 'datacenter'
        ordering = ('-id',)


class Zone(models.Model, ModelMixin):
    name = models.CharField(max_length=50)

    def __repr__(self):
        return '<Zone %r>' % self.name

    class Meta:
        db_table = 'zone'
        ordering = ('-id',)


class DeviceVersion(models.Model, ModelMixin):
    name = models.CharField(max_length=50)

    def __repr__(self):
        return '<DeviceVersion %r>' % self.name

    class Meta:
        db_table = 'device_version'
        ordering = ('-id',)


class OperatingSystem(models.Model, ModelMixin):
    name = models.CharField(max_length=50)

    def __repr__(self):
        return '<OperatingSystem %r>' % self.name

    class Meta:
        db_table = 'operating_system'
        ordering = ('-id',)


class Host(models.Model, ModelMixin):
    name = models.CharField(max_length=50)
    type = models.IntegerField()
    hostname = models.CharField(max_length=50)
    port = models.IntegerField(null=True)
    username = models.CharField(max_length=50, null=True)
    pkey = models.TextField(null=True)
    desc = models.CharField(max_length=255, null=True)

    host_machine = models.ForeignKey("Host", models.PROTECT, related_name='+', null=True)

    datacenter = models.ForeignKey(Datacenter, models.PROTECT, related_name='+')
    zone = models.ForeignKey(Zone, models.PROTECT, related_name='+')
    device_version = models.ForeignKey(DeviceVersion, models.PROTECT, related_name='+', null=True)
    operating_system = models.ForeignKey(OperatingSystem, models.PROTECT, related_name='+', null=True)

    created_at = models.CharField(max_length=20, default=human_datetime)
    created_by = models.ForeignKey(User, models.PROTECT, related_name='+')
    deleted_at = models.CharField(max_length=20, null=True)
    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    @property
    def private_key(self):
        return self.pkey or AppSetting.get('private_key')

    def get_ssh(self, pkey=None):
        pkey = pkey or self.private_key
        return SSH(self.hostname, self.port, self.username, pkey)

    def __repr__(self):
        return '<Host %r>' % self.name

    class Meta:
        db_table = 'hosts'
        ordering = ('-id',)
