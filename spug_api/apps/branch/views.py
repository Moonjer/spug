from django.views.generic import View

from apps.branch.models import Branch
from libs import json_response


class BranchView(View):
    def get(self, request):
        branch_id = request.GET.get('id')
        if branch_id:
            return json_response(Branch.objects.get(pk=branch_id))
        branches = Branch.objects.filter(deleted_by_id__isnull=True)
        return json_response({'branches': [x.to_dict() for x in branches]})


def sync_branch_by_app(request):

    return
