from django.db import models
from ..base.mastarbase import MasterBase


class MAssetCategoryMain(MasterBase):
    """
    Asset Category Main Master
    """
    name = models.CharField(max_length=10)


class MAssetCategorySub(MasterBase):
    """
    Asset Category Sub Master
    """
    name = models.CharField(max_length=30)
    m_asset_category_main = models.ForeignKey(MAssetCategoryMain,
                                              on_delete=models.CASCADE, related_name='m_asset_category_subs')
