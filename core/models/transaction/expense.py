from django.db import models
from core.models.base.transactionbase import TransactionBase
from ..master.expense import MExpenseCategorySub
from ..master.account import MAccount


class TExpense(TransactionBase):
    """
    Expense Transaction
    """
    paymentRecipientName = models.CharField(max_length=30, blank=True, default='')
    expenseDate = models.DateField()
    note = models.TextField()


class TExpenseDetail(TransactionBase):
    """
    Expense Detail Transaction
    """
    amount = models.BigIntegerField()
    mExpenseCategorySub = models.ForeignKey(MExpenseCategorySub, on_delete=models.CASCADE)
    mAccount = models.ForeignKey(MAccount, on_delete=models.CASCADE)
