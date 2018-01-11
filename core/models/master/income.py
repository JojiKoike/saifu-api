from django.db import models
from core.models.base.mastarbase import MasterBase


class MIncomeCategoryMain(MasterBase):
    """
    Income Category Master (Main)
    """
    name = models.CharField(max_length=10, unique=True)


class MIncomeCategorySub(MasterBase):
    """
    Income Category Master (Sub)
    """
    name = models.CharField(max_length=30)
    m_income_category_main = models.ForeignKey(MIncomeCategoryMain,
                                               on_delete=models.CASCADE, related_name='m_income_category_subs')
