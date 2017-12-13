from django.db import models
from ..base.transactionbase import TransactionBase
from ..master.saifu import MSaifu


class TTransferBetweenAccounts(TransactionBase):
    """
    Transfer Between Accounts Model
    """
    transferDate = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    fromSaifu = models.ForeignKey(MSaifu, on_delete=models.CASCADE, related_name='FromSaifu')
    toSaifu = models.ForeignKey(MSaifu, on_delete=models.CASCADE, related_name='ToSaifu')
