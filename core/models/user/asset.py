from django.db import models
from ..base.userbase import UserBase
from ..master.asset import MAssetCategorySub


class UAsset(UserBase):
    """
    Asset User Table
    """
    name = models.CharField(max_length=30)
    current_capital_amount = models.BigIntegerField()
    current_evaluated_amount = models.BigIntegerField()
    m_asset_category_sub = models.ForeignKey(MAssetCategorySub, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='assets', on_delete=models.CASCADE)
