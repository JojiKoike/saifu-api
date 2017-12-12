from django.db import models
from ..base.transactionbase import TransactionBase
from ..master.account import MAccount


class TTransferBetweenAccounts(TransactionBase):
    """
    Transfer Between Accounts Model
    """
    transferDate = models.DateField()
    amount = models.BigIntegerField()
    note = models.TextField()
    fromAccount = models.ForeignKey(MAccount, on_delete=models.CASCADE, related_name='FromAccount')
    toAccount = models.ForeignKey(MAccount, on_delete=models.CASCADE, related_name='ToAccount')
