from django.db import models
from ..base.transactionbase import TransactionBase
from core.models.user.saifu import USaifu
from core.models.user.asset import UAsset


class TTransferBetweenSaifu(TransactionBase):
    """
    Transfer Between Saifu Model
    """
    transfer_date = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    from_u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE, related_name='from_u_saifu')
    to_u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE, related_name='to_u_saifu')
    owner = models.ForeignKey('auth.User',
                              related_name='t_transfer_between_saifus', on_delete=models.CASCADE)


class TTransferBetweenSaifuAndAsset(TransactionBase):
    """
    Transfer Between Saifu And Asset Model
    """
    transfer_date = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE, related_name='u_saifu')
    u_asset = models.ForeignKey(UAsset, on_delete=models.CASCADE, related_name='u_asset')
    owner = models.ForeignKey('auth.User',
                              related_name='t_transfer_between_saifu_and_assets', on_delete=models.CASCADE)
