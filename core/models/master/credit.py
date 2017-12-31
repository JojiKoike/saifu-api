from django.db import models
from core.models.base.mastarbase import MasterBase


class MCreditCategoryMain(MasterBase):
    """
    Credit Category Main Master
    """
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class MCreditCategorySub(MasterBase):
    """
    Credit Category Sub Master
    """
    name = models.CharField(max_length=30)
    m_credit_category_main \
        = models.ForeignKey(MCreditCategoryMain,
                            on_delete=models.CASCADE, related_name='m_credit_category_subs')

    def __str__(self):
        return self.name
