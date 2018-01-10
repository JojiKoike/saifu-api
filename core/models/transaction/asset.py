from django.db import models
from ..base.transactionbase import TransactionBase
from ..user.asset import UAsset


class TAssetEvaluate(TransactionBase):
    """
    Asset Evaluate Transaction Model
    """
    evaluate_date = models.DateField()
    evaluated_amount = models.BigIntegerField()
    note = models.TextField()
    u_asset = models.ForeignKey(UAsset, on_delete=models.CASCADE, related_name='t_asset_evaluates')
    owner = models.ForeignKey('auth.User', related_name='t_asset_evaluates', on_delete=models.CASCADE)
