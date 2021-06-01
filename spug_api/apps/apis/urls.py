# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.urls import path

from apps.apis import config, branch

urlpatterns = [
    path('config/', config.get_configs),
    path('branch/hook', branch.get_hook),
]
