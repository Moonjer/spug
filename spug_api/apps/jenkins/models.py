from django.db import models

from apps.account.models import User
from libs import ModelMixin


class Job(models.Model, ModelMixin):
    name = models.CharField(max_length=50, db_column='job_name')
    url = models.CharField(max_length=512, db_column='job_url')

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    class Meta:
        db_table = 'jenkins_job'
        ordering = ('-id',)
