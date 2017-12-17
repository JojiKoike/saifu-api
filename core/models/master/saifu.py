from django.db import models
from core.models.base.mastarbase import MasterBase


class MSaifuCategory(MasterBase):
    """
    Account Category Master
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MSaifu(MasterBase):
    """
    Account Master
    """
    name = models.CharField(max_length=30)
    currentBalance = models.BigIntegerField()
    mSaifuCategory = models.ForeignKey(MSaifuCategory, on_delete=models.CASCADE)
