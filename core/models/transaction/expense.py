from django.db import models
from core.models.base.transactionbase import TransactionBase, UnModifiableTransactionBase
from ..master.expense import MExpenseCategorySub
from .saifu import TSaifuHistory


class TExpense(TransactionBase):
    """
    Expense Transaction
    """
    paymentRecipientName = models.CharField(max_length=30, blank=True, default='')
    expenseDate = models.DateField()
    note = models.TextField()


class TExpenseDetail(UnModifiableTransactionBase):
    """
    Expense Detail Transaction
    """
    tExpense = models.ForeignKey(TExpense, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    mExpenseCategorySub = models.ForeignKey(MExpenseCategorySub, on_delete=models.CASCADE)
    tSaifuHistory = models.OneToOneField(TSaifuHistory, on_delete=models.CASCADE)