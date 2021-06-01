import json

from django.http import HttpResponse

from apps.git.models import Branch


def get_hook(request):
    event = json.loads(request.body)
    project_id = event['project_id']
    project_name = event['project']['name']

    changes = event['changes']
    for change in changes:
        branch_name = change['ref'][11:]

        # 保存新分支
        if change['before'] == '0000000000000000000000000000000000000000':
            branch = Branch.objects.create(project_id=project_id, project_name=project_name, branch_name=branch_name)

            # 判断sprint
            if branch_name.startswith('release') or branch_name.startswith('hotfix'):
                branch.sprint = branch_name

            branch.save()
            print('branch: ', branch)

    return HttpResponse(json.dumps(request.POST), content_type='application/json')
