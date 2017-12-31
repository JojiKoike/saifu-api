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
    name = models.CharField(max_length=30)
    m_income_category_main = models.ForeignKey(MIncomeCategoryMain,
                                               on_delete=models.CASCADE, related_name='m_income_category_subs')

    def __str__(self):
        return self.name
