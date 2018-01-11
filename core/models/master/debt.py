from django.db import models
from ..base.mastarbase import MasterBase


class MDebtCategoryMain(MasterBase):
    """
    Debt Category Main Master
    """
    name = models.CharField(max_length=10, unique=True)


class MDebtCategorySub(MasterBase):
    """
    Debt Category Sub Master
    """
    name = models.CharField(max_length=30)
    m_debt_category_main = models.ForeignKey(MDebtCategoryMain,
                                             on_delete=models.CASCADE, related_name='m_debt_category_subs')
