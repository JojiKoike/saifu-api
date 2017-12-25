from django.db import models
from ..base.transactionbase import UnModifiableTransactionBase


class TTransferBetweenSaifu(UnModifiableTransactionBase):
    """
    Transfer Between Saifu Model
    """
    transferDate = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    fromSaifu = models.UUIDField()
    toSaifu = models.UUIDField()
