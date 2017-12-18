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
    fromSaifuHistory = models.OneToOneField(TSaifuHistory, on_delete=models.CASCADE, related_name='FromSaifu')
    toSaifuHistory = models.OneToOneField(TSaifuHistory, on_delete=models.CASCADE, related_name='ToSaifu')
