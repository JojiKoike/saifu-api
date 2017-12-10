from django.db import models
from core.models.base.mastarbase import MasterBase


class MasterExpenseCategoryMain(MasterBase):
    """
    Expense Category Master (Main)
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MasterExpenseCategorySub(MasterBase):
    """
    Expense Category Master (Sub)
    """
    masterExpenseCategoryMain = models.ForeignKey(MasterExpenseCategoryMain, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class MasterIncomeCategoryMain(MasterBase):
    """
    Income Category Master (Main)
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MasterIncomeCategorySub(MasterBase):
    """
    Income Category Master (Sub)
    """
    masterIncomeCategoryMain = models.ForeignKey(MasterIncomeCategoryMain, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

