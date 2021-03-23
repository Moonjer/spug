from django.views.generic import View

from apps.branch.models import Branch
from libs import json_response


class BranchView(View):
    def get(self, request):
        host_id = request.GET.get('id')
        return json_response(Branch.objects.get(pk=host_id))
