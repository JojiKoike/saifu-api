from django.db import models
from core.models.base.transactionbase import TransactionBase, UnModifiableTransactionBase
from ..master.income import MIncomeCategorySub
from .saifu import TSaifuHistory


class TIncome(TransactionBase):
    """
    Income Transaction
    """
    paymentSourceName = models.CharField(max_length=30, blank=True, default='')
    incomeDate = models.DateField()
    note = models.TextField()


class TIncomeDetail(UnModifiableTransactionBase):
    """
    Income Detail Transaction
    """
    tIncome = models.ForeignKey(TIncome, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    mIncomeCategorySub = models.ForeignKey(MIncomeCategorySub, on_delete=models.CASCADE)
    tSaifu = models.OneToOneField(TSaifuHistory, on_delete=models.CASCADE)