from django.db import models
from core.models.base.transactionbase import TransactionBase
from ..master.expense import MExpenseCategorySub
from core.models.user.saifu import USaifu


class TExpense(TransactionBase):
    """
    Expense Transaction
    """
    payment_recipient_name = models.CharField(max_length=30, blank=True, default='')
    expense_date = models.DateField()
    note = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='t_expenses', on_delete=models.CASCADE)


class TExpenseDetail(TransactionBase):
    """
    Expense Detail Transaction
    """
    t_expense = models.ForeignKey(TExpense, on_delete=models.CASCADE, related_name='t_expense_details')
    amount = models.BigIntegerField()
    m_expense_category_sub = models.ForeignKey(MExpenseCategorySub, on_delete=models.CASCADE)
    u_saifu = models.ForeignKey(USaifu, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='t_expense_details', on_delete=models.CASCADE)
