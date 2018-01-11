from django.db import models
from core.models.base.mastarbase import MasterBase


class MSaifuCategoryMain(MasterBase):
    """
    Saifu Category Master (Main)
    """
    name = models.CharField(max_length=10, unique=True)


class MSaifuCategorySub(MasterBase):
    """
    Saifu Category Master (Sub)
    """
    name = models.CharField(max_length=30)
    m_saifu_category_main = models.ForeignKey(MSaifuCategoryMain,
                                              on_delete=models.CASCADE, related_name='m_saifu_category_subs')
