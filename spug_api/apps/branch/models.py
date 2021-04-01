from django.db import models

from apps.account.models import User
from libs import ModelMixin


class Branch(models.Model, ModelMixin):
    name = models.CharField(max_length=50)
    sprint = models.CharField(max_length=50)

    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    class Meta:
        db_table = 'branch'
        ordering = ('-id',)
