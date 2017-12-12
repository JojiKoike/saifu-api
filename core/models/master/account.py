from django.db import models
from core.models.base.mastarbase import MasterBase


class MAccountCategory(MasterBase):
    """
    Account Category Master
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MAccount(MasterBase):
    """
    Account Master
    """
    name = models.CharField(max_length=30)
    initialBalance = models.BigIntegerField()
    mAccountCategory = models.ForeignKey(MAccountCategory, on_delete=models.CASCADE)
