from django.db import models
from django.utils import timezone

from apps.account.models import User
from libs import ModelMixin


class Group(models.Model, ModelMixin):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, db_column='group_name')
    created_at = models.DateTimeField(default=timezone.now)

    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    class Meta:
        db_table = 'git_group'
        ordering = ('-id',)


class Project(models.Model, ModelMixin):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, db_column='project_name')
    created_at = models.DateTimeField(default=timezone.now)

    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    class Meta:
        db_table = 'git_project'
        ordering = ('-id',)


class Branch(models.Model, ModelMixin):
    branch = models.CharField(max_length=50, db_column='branch_name')
    sprint = models.CharField(max_length=50)

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    class Meta:
        db_table = 'git_branch'
        ordering = ('-id',)
