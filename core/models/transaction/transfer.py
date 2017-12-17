from django.db import models
from ..base.transactionbase import UnModifiableTransactionBase
from .saifu import TSaifuHistory


class TTransferBetweenSaifu(UnModifiableTransactionBase):
    """
    Transfer Between Saifu Model
    """
    transferDate = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    fromSaifu = models.OneToOneField(TSaifuHistory, on_delete=models.CASCADE, related_name='FromSaifu')
    toSaifu = models.OneToOneField(TSaifuHistory, on_delete=models.CASCADE, related_name='ToSaifu')
