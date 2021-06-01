from django.views.generic import View

from apps.jenkins.models import Job
from libs import json_response
from libs.python_jenkins import PythonJenkins


class JobView(View):
    def get(self, request):
        job_id = request.GET.get('id')
        if job_id:
            return json_response(Job.objects.get(pk=job_id))
        jobs = Job.objects.filter(deleted_by_id__isnull=True).order_by('name')
        return json_response({'jobs': [x.to_dict() for x in jobs]})


def sync_jobs(request):
    pj = PythonJenkins()
    job_list_jenkins = pj.server.get_all_jobs()
    for job_jenkins in job_list_jenkins:
        job = Job.objects.create(name=job_jenkins['name'], url=job_jenkins['url'])
        job.save()

    return json_response()
