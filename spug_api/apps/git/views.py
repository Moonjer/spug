from django.views.generic import View

from apps.git.models import Branch, Group, Project
from libs import json_response
from libs.git_warehouse import GitWarehouse


class BranchView(View):
    def get(self, request):
        branch_id = request.GET.get('id')
        if branch_id:
            return json_response(Branch.objects.get(pk=branch_id))
        branches = Branch.objects.filter(deleted_by_id__isnull=True)
        return json_response({'branches': [x.to_dict() for x in branches]})


def sync_group(request):
    group_list_db = Group.objects.all()
    group_map_db = {}
    for group_db in group_list_db:
        group_map_db[group_db.id] = group_db

    gw = GitWarehouse()
    group_list_gw = gw.get_all_group()
    for group_dw in group_list_gw:
        if not group_map_db.__contains__(group_dw.id):
            group = Group.objects.create(id=group_dw.id, name=group_dw.name)
            group.save()

    return json_response()


def sync_project(request):
    gw = GitWarehouse()

    group_list = Group.objects.all()
    for group in group_list:
        project_list_gw = gw.get_all_project_by_group_id(group.id)

        for project_gw in project_list_gw:
            project = Project.objects.create(id=project_gw.id, name=project_gw.name, group_id=group.id)
            project.save()

    return json_response()
