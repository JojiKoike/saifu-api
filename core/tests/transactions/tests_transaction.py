from django.test import TestCase
from core.models.master.income import *
from core.models.master.expense import *
from core.models.master.saifu import *
from core.models.master.credit import *
from core.models.transaction.income import *
from core.models.transaction.expense import *
from core.models.transaction.saifu import *
from core.models.transaction.transfer import *
from core.models.transaction.credit import *
from django.core.exceptions import ValidationError


class TSaifuHistoryTests(TestCase):
    """
    Saifu History Transaction Tests
    """

    def setUp(self):
        msaifucategory = MSaifuCategory.objects.create(name="銀行")
        MSaifu.objects.create(name="スイス銀行",  currentBalance=10000000000, mSaifuCategory=msaifucategory)

    def test_SaifuHistory_Saved_Correctly(self):
        msaifu = MSaifu.objects.get(name="スイス銀行")
        tsaifuhistory = TSaifuHistory.objects.create(recordDate="2017-12-17", balance=10000000000, mSaifu=msaifu)
        self.assertEqual(tsaifuhistory.recordDate, "2017-12-17")
        self.assertEqual(tsaifuhistory.balance, 10000000000)
        self.assertEqual(tsaifuhistory.mSaifu.name, "スイス銀行")
        self.assertEqual(tsaifuhistory.mSaifu.currentBalance, 10000000000)
        self.assertEqual(tsaifuhistory.mSaifu.mSaifuCategory.name, "銀行")



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


class TExpenseTests(TestCase):
    """
    Expense (Parent) Transaction Tests
    """

    def test_Expense_Saved_Correctly(self):
        expense = TExpense.objects.create(paymentRecipientName="ファミマ",
                                          expenseDate="2017-12-17", note="Test")
        self.assertEqual(expense.paymentRecipientName, "ファミマ")
        self.assertEqual(expense.expenseDate, "2017-12-17")
        self.assertEqual(expense.note, "Test")


class TExpenseDetailTests(TestCase):
    """
    Expense (Detail) Transaction Tests
    """

    def test_ExpenseDetail_Saved_Correctly(self):
        expenseAmount = 10000000
        """収入記録親オブジェクト生成"""
        texpense = TExpense.objects.create(paymentRecipientName="ファミマ", expenseDate="2017-12-17", note="テスト")
        """収入カテゴリオブジェクト生成"""
        mexpensecategorymain = MExpenseCategoryMain.objects.create(name="食費")
        mexpensecategorysub = MExpenseCategorySub.objects.create(name="外食", mExpenseCategoryMain=mexpensecategorymain)
        """MSaufuオブジェクト生成"""
        msaifucategory = MSaifuCategory.objects.create(name="クレジットカード")
        msaifu = MSaifu.objects.create(name="VISA", currentBalance=10000000, mSaifuCategory=msaifucategory)
        """TSaifuHistoryオブジェクト生成"""
        tsaifuhistory = TSaifuHistory.objects.create(
            recordDate="2017-12-17", balance=msaifu.currentBalance - expenseAmount, mSaifu=msaifu)
        """収入明細レコード保存処理"""
        texpensedetail = TExpenseDetail.objects.create(
            tExpense=texpense, amount=expenseAmount, mExpenseCategorySub=mexpensecategorysub, tSaifuHistory=tsaifuhistory)
        self.assertEqual(texpensedetail.tExpense.paymentRecipientName, "ファミマ")
        self.assertEqual(texpensedetail.tExpense.expenseDate, "2017-12-17")
        self.assertEqual(texpensedetail.tExpense.note, "テスト")
        self.assertEqual(texpensedetail.amount, expenseAmount)
        self.assertEqual(texpensedetail.mExpenseCategorySub.mExpenseCategoryMain.name, "食費")
        self.assertEqual(texpensedetail.mExpenseCategorySub.name, "外食")
        self.assertEqual(texpensedetail.tSaifuHistory.balance, msaifu.currentBalance - expenseAmount)
        """MSaifu残高更新処理"""
        oldCurrentBalance = msaifu.currentBalance
        msaifu.currentBalance = oldCurrentBalance - expenseAmount
        msaifu.save()
        self.assertEqual(msaifu.currentBalance, oldCurrentBalance - expenseAmount)


class TTransferBetweenSaifuTests(TestCase):
    """
    Transfer Between Saifu Transaction Tests
    """
    fromSaifuCategory = None
    toSaifuCategory = None
    fromSaifu = None
    toSaifu = None
    
    def setUp(self):
        self.fromSaifuCategory = MSaifuCategory.objects.create(name="クレジットカード")
        self.fromSaifu = MSaifu.objects.create(name="JCB", currentBalance=-100000, mSaifuCategory=self.fromSaifuCategory)
        self.toSaifuCategory = MSaifuCategory.objects.create(name="電子マネー")
        self.toSaifu = MSaifu.objects.create(name="Suica", currentBalance=3000, mSaifuCategory=self.toSaifuCategory)
        
    def test_TransferBetweenSaifu_Saved_Correctly(self):
        transferamount = 5000
        fromsaifuhisotory = TSaifuHistory.objects.create(recordDate="2017-12-18", 
                                                         balance=self.fromSaifu.currentBalance - transferamount,
                                                         mSaifu=self.fromSaifu)
        tosaifuhistory = TSaifuHistory.objects.create(recordDate="2017-12-18",
                                                      balance=self.toSaifu.currentBalance + transferamount,
                                                      mSaifu=self.toSaifu)
        ttransferbetweensaifu = TTransferBetweenSaifu.objects.create(transferDate="2017-12-18", 
                                                                     amount=transferamount, 
                                                                     note="Suicaチャージシナリオ",
                                                                     fromSaifuHistory=fromsaifuhisotory,
                                                                     toSaifuHistory=tosaifuhistory)
        self.fromSaifu.currentBalance -= transferamount
        self.fromSaifu.save()
        self.toSaifu.currentBalance += transferamount
        self.toSaifu.save()
        self.assertEqual(ttransferbetweensaifu.amount, 5000)
        self.assertEqual(ttransferbetweensaifu.fromSaifuHistory.balance, -105000)
        self.assertEqual(ttransferbetweensaifu.toSaifuHistory.balance, 8000)
        self.assertEqual(self.fromSaifu.currentBalance, -105000)
        self.assertEqual(self.toSaifu.currentBalance, 8000)


class TCreditTests(TestCase):
    """
    Credit Transfer Tests
    """
    mcreditcategorymain = None
    mcreditcategorysub = None
    tincome = None

    def setUp(self):
        self.mcreditcategorymain = MCreditCategoryMain.objects.create(name="税金")
        self.mcreditcategorysub = MCreditCategorySub.objects.create(
            mCreditCategoryMain=self.mcreditcategorymain, name="所得税")
        self.tincome = TIncome.objects.create(paymentSourceName="フリーメーソン", incomeDate="2017-12-18", note="Test")

    def test_TCredit_Saved_Correctly(self):
        tcredit = TCredit.objects.create(
            amount=10000, mCreditCategorySub=self.mcreditcategorysub, tIncome=self.tincome)
        self.assertEqual(tcredit.amount, 10000)
        self.assertEqual(tcredit.mCreditCategorySub.name, "所得税")
        self.assertEqual(tcredit.mCreditCategorySub.mCreditCategoryMain.name, "税金")
        self.assertEqual(tcredit.tIncome.paymentSourceName, "フリーメーソン")
        self.assertEqual(tcredit.tIncome.incomeDate, "2017-12-18")


