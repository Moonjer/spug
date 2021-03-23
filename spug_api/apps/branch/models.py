from django.db import models

from libs import ModelMixin


class Branch(models.Model, ModelMixin):
    name = models.CharField(max_length=50)
    sprint = models.CharField(max_length=50)

    class Meta:
        db_table = 'branch'
        ordering = ('-id',)
