from django.db import models
from core.models.base.mastarbase import MasterBase


class MExpenseCategoryMain(MasterBase):
    """
    Expense Category Master (Main)
    """
    name = models.CharField(max_length=10)


class MExpenseCategorySub(MasterBase):
    """
    Expense Category Master (Sub)
    """
    name = models.CharField(max_length=30)
    m_expense_category_main = models.ForeignKey(MExpenseCategoryMain,
                                                on_delete=models.CASCADE, related_name="m_expense_category_subs")
