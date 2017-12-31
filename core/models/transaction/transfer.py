from django.db import models
from ..base.transactionbase import TransactionBase
from core.models.user.saifu import USaifu


class TTransferBetweenSaifu(TransactionBase):
    """
    Transfer Between Saifu Model
    """
    transfer_date = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    from_u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE, related_name='from_u_saifu')
    to_u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE, related_name='to_u_saifu')
    owner = models.ForeignKey('auth.User', related_name='t_transfer_between_saifus', on_delete=models.CASCADE)
