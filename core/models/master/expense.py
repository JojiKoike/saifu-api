from django.db import models
from core.models.base.mastarbase import MasterBase


class MExpenseCategoryMain(MasterBase):
    """
    Expense Category Master (Main)
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MExpenseCategorySub(MasterBase):
    """
    Expense Category Master (Sub)
    """
    mExpenseCategoryMain = models.ForeignKey(MExpenseCategoryMain, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
