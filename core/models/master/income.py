from django.db import models
from core.models.base.mastarbase import MasterBase


class MIncomeCategoryMain(MasterBase):
    """
    Income Category Master (Main)
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MIncomeCategorySub(MasterBase):
    """
    Income Category Master (Sub)
    """
    mIncomeCategoryMain = models.ForeignKey(MIncomeCategoryMain, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
