# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
import os
import shutil

from django.conf import settings

from apps.app.models import Deploy, App
from apps.git.models import Branch


def parse_envs(text):
    data = {}
    if text:
        for line in text.split('\n'):
            fields = line.split('=', 1)
            if len(fields) != 2 or fields[0].strip() == '':
                raise Exception(f'解析自定义全局变量{line!r}失败，确认其遵循 key = value 格式')
            data[fields[0].strip()] = fields[1].strip()
    return data


def fetch_versions(deploy: Deploy):
    app = App.objects.filter(id=deploy.app_id).first()
    return Branch.objects.filter(project_id=app.git_repo.id).all()


def remove_repo(deploy_id):
    shutil.rmtree(os.path.join(settings.REPOS_DIR, str(deploy_id)), True)
