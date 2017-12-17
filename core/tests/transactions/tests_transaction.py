from django.test import TestCase
from core.models.master.income import *
from core.models.master.saifu import *
from core.models.transaction.income import *
from core.models.transaction.expense import *
from core.models.transaction.saifu import *
from django.core.exceptions import ValidationError


class TIncomeTests(TestCase):
    """
    Income (Parent) Transaction Tests
    """

    def test_Income_Saved_Correctly(self):
        tincome = TIncome.objects.create(paymentSourceName="ふぁみま", incomeDate="2017-12-15", note="テストテキスト")
        self.assertEqual(tincome.paymentSourceName, "ふぁみま")
        self.assertEqual(tincome.incomeDate, '2017-12-15')
        self.assertEqual(tincome.note, 'テストテキスト')

    def test_Income_Saved_Illegal_Income_Date(self):
        with self.assertRaisesMessage(ValidationError, "2017-12-32' は有効な日付形式(YYYY-MM-DD)ですが、日付が不正です。"):
            TIncome.objects.create(paymentSourceName="ふぁみま", incomeDate="2017-12-32", note="テストテキスト")


class TIncomeDetailTests(TestCase):
    """
    Income (Detail-Child) Transaction Tests
    """

    def test_IncomeDetail_Saved_Correctly(self):
        incomeAmount = 10000000
        """収入記録親オブジェクト生成"""
        tincome = TIncome.objects.create(paymentSourceName="フリーメーソン", incomeDate="2017-12-17", note="テスト")
        """収入カテゴリオブジェクト生成"""
        mincomecategorymain = MIncomeCategoryMain.objects.create(name="給与")
        mincomecategorysub = MIncomeCategorySub.objects.create(name="通常給与", mIncomeCategoryMain=mincomecategorymain)
        """MSaufuオブジェクト生成"""
        msaifucategory = MSaifuCategory.objects.create(name="銀行")
        msaifu = MSaifu.objects.create(name="スイス銀行", currentBalance=10000000, mSaifuCategory=msaifucategory)
        """TSaifuHistoryオブジェクト生成"""
        tsaifuhistory = TSaifuHistory.objects.create(
            recordDate="2017-12-17", balance=msaifu.currentBalance+incomeAmount, mSaifu=msaifu)
        """収入明細レコード保存処理"""
        tincomedetail = TIncomeDetail.objects.create(
            tIncome=tincome, amount=incomeAmount, mIncomeCategorySub=mincomecategorysub, tSaifuHistory=tsaifuhistory)
        self.assertEqual(tincomedetail.tIncome.paymentSourceName, "フリーメーソン")
        self.assertEqual(tincomedetail.tIncome.incomeDate, "2017-12-17")
        self.assertEqual(tincomedetail.tIncome.note, "テスト")
        self.assertEqual(tincomedetail.amount, incomeAmount)
        self.assertEqual(tincomedetail.mIncomeCategorySub.mIncomeCategoryMain.name, "給与")
        self.assertEqual(tincomedetail.mIncomeCategorySub.name, "通常給与")
        self.assertEqual(tincomedetail.tSaifuHistory.balance, msaifu.currentBalance+incomeAmount)
        """MSaifu残高更新処理"""
        oldCurrentBalance = msaifu.currentBalance
        msaifu.currentBalance = oldCurrentBalance + incomeAmount
        msaifu.save()
        self.assertEqual(msaifu.currentBalance, oldCurrentBalance + incomeAmount)
        print(msaifu.currentBalance)

class TExpenseTests(TestCase):
    """
    Expense (Parent) Transaction Tests
    """

    def test_Expense_Saved_Correctly(self):
        expense = TExpense.objects.create(paymentRecipientName="ファミマ",
                                          expenseDate="2017-12-16", note="Test")
        self.assertEqual(expense.paymentRecipientName, "ファミマ")

