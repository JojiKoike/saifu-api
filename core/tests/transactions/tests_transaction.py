from django.test import TestCase
from core.models.master.income import *
from core.models.master.expense import *
from core.models.master.credit import *
from core.models.transaction.income import *
from core.models.transaction.expense import *
from core.models.transaction.transfer import *
from core.models.transaction.credit import *
from core.models.user.saifu import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class TIncomeTests(TestCase):
    owner = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')


    """
    Income (Parent) Transaction Tests
    """

    def test_Income_Saved_Correctly(self):
        tincome = TIncome.objects.create(payment_source_name="ふぁみま",
                                         income_date="2017-12-15",
                                         note="テストテキスト",
                                         owner=self.owner)
        self.assertEqual(tincome.payment_source_name, "ふぁみま")
        self.assertEqual(tincome.income_date, '2017-12-15')
        self.assertEqual(tincome.note, 'テストテキスト')

    def test_Income_Saved_Illegal_Income_Date(self):
        with self.assertRaisesMessage(ValidationError, "2017-12-32' は有効な日付形式(YYYY-MM-DD)ですが、日付が不正です。"):
            TIncome.objects.create(payment_source_name="ふぁみま",
                                   income_date="2017-12-32", note="テストテキスト", owner=self.owner)


class TIncomeDetailTests(TestCase):
    """
    Income (Detail-Child) Transaction Tests
    """

    owner = None
    t_expense = None
    expense_amount = None
    m_expense_category_main = None
    m_expense_category_sub = None
    m_saifu_category = None
    u_saifu = None
    income_amount = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.t_income = TIncome.objects.create(payment_source_name="フリーメーソン",
                                               income_date="2017-12-17", note="テスト", owner=self.owner)
        self.m_income_category_main = MIncomeCategoryMain.objects.create(name="給与収入")
        self.m_income_category_sub = MIncomeCategorySub. \
            objects.create(name="通常給与", m_income_category_main=self.m_income_category_main)
        self.m_saifu_category = MSaifuCategory.objects.create(name="銀行口座")
        self.u_saifu = USaifu.objects.create(name="スイス銀行",
                                             current_balance=10000000, m_saifu_category=self.m_saifu_category,
                                             owner=self.owner)

    def test_IncomeDetail_Saved_Correctly(self):
        self.income_amount = 1000000
        tincomedetail = TIncomeDetail.objects.create(
            t_income=self.t_income, amount=self.income_amount,
            m_income_category_sub=self.m_income_category_sub, u_saifu=self.u_saifu, owner=self.owner)
        self.assertEqual(tincomedetail.t_income.payment_source_name, "フリーメーソン")
        self.assertEqual(tincomedetail.t_income.income_date, "2017-12-17")
        self.assertEqual(tincomedetail.t_income.note, "テスト")
        self.assertEqual(tincomedetail.amount, self.income_amount)
        self.assertEqual(tincomedetail.m_income_category_sub.m_income_category_main.name, "給与収入")
        self.assertEqual(tincomedetail.m_income_category_sub.name, "通常給与")
        """MSaifu残高更新処理"""
        oldCurrentBalance = self.u_saifu.current_balance
        self.u_saifu.current_balance += self.income_amount
        self.u_saifu.save()
        self.assertEqual(self.u_saifu.current_balance, oldCurrentBalance + self.income_amount)


class TExpenseTests(TestCase):
    """
    Expense (Parent) Transaction Tests
    """

    owner = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')

    def test_Expense_Saved_Correctly(self):
        expense = TExpense.objects.create(payment_recipient_name="ファミマ",
                                          expense_date="2017-12-17", note="Test", owner=self.owner)
        self.assertEqual(expense.payment_recipient_name, "ファミマ")
        self.assertEqual(expense.expense_date, "2017-12-17")
        self.assertEqual(expense.note, "Test")


class TExpenseDetailTests(TestCase):
    """
    Expense (Detail) Transaction Tests
    """
    owner = None
    t_expense = None
    expense_amount = None
    m_expense_category_main = None
    m_expense_category_sub = None
    m_saifu_category = None
    u_saifu = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.t_expense = TExpense.objects.create(payment_recipient_name="ファミマ",
                                                 expense_date="2017-12-17", note="テスト", owner=self.owner)
        self.m_expense_category_main = MExpenseCategoryMain.objects.create(name="食費")
        self.m_expense_category_sub = MExpenseCategorySub.\
            objects.create(name="外食",  m_expense_category_main=self.m_expense_category_main)
        self.m_saifu_category = MSaifuCategory.objects.create(name="クレジットカード")
        self.u_saifu = USaifu.objects.create(name="VISA",
                                             current_balance=10000000, m_saifu_category=self.m_saifu_category,
                                             owner=self.owner)

    def test_ExpenseDetail_Saved_Correctly(self):
        self.expense_amount = 10000000

        texpensedetail = TExpenseDetail.objects.create(
            t_expense=self.t_expense,
            amount=self.expense_amount,
            m_expense_category_sub=self.m_expense_category_sub, u_saifu=self.u_saifu, owner=self.owner)
        self.assertEqual(texpensedetail.t_expense.payment_recipient_name, "ファミマ")
        self.assertEqual(texpensedetail.t_expense.expense_date, "2017-12-17")
        self.assertEqual(texpensedetail.t_expense.note, "テスト")
        self.assertEqual(texpensedetail.amount, self.expense_amount)
        self.assertEqual(texpensedetail.m_expense_category_sub.m_expense_category_main.name, "食費")
        self.assertEqual(texpensedetail.m_expense_category_sub.name, "外食")
        oldCurrentBalance = self.u_saifu.current_balance
        self.u_saifu.current_balance -= self.expense_amount
        self.u_saifu.save()
        self.assertEqual(self.u_saifu.current_balance, oldCurrentBalance - self.expense_amount)


class TTransferBetweenSaifuTests(TestCase):
    """
    Transfer Between Saifu Transaction Tests
    """
    fromSaifuCategory = None
    toSaifuCategory = None
    fromSaifu = None
    toSaifu = None
    owner = None
    
    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.fromSaifuCategory = MSaifuCategory.objects.create(name="クレジットカード")
        self.fromSaifu = USaifu.objects.create(name="JCB", current_balance=-100000,
                                               m_saifu_category=self.fromSaifuCategory, owner=self.owner)
        self.toSaifuCategory = MSaifuCategory.objects.create(name="電子マネー")
        self.toSaifu = USaifu.objects.create(name="Suica", current_balance=3000,
                                             m_saifu_category=self.toSaifuCategory, owner=self.owner)
        
    def test_TransferBetweenSaifu_Saved_Correctly(self):
        transferamount = 5000
        ttransferbetweensaifu = TTransferBetweenSaifu.objects.create(transfer_date="2017-12-18",
                                                                     amount=transferamount, 
                                                                     note="Suicaチャージシナリオ",
                                                                     from_u_saifu=self.fromSaifu,
                                                                     to_u_saifu=self.toSaifu,
                                                                     owner=self.owner)
        self.fromSaifu.current_balance -= transferamount
        self.fromSaifu.save()
        self.toSaifu.current_balance += transferamount
        self.toSaifu.save()
        self.assertEqual(ttransferbetweensaifu.amount, 5000)
        self.assertEqual(self.fromSaifu.current_balance, -105000)
        self.assertEqual(self.toSaifu.current_balance, 8000)


class TCreditTests(TestCase):
    """
    Credit Transfer Tests
    """
    mcreditcategorymain = None
    mcreditcategorysub = None
    tincome = None
    owner = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.mcreditcategorymain = MCreditCategoryMain.objects.create(name="税金")
        self.mcreditcategorysub = MCreditCategorySub.objects.create(
            m_credit_category_main=self.mcreditcategorymain, name="所得税")
        self.tincome = TIncome.objects.create(payment_source_name="フリーメーソン",
                                              income_date="2017-12-18", note="Test", owner=self.owner)

    def test_TCredit_Saved_Correctly(self):
        tcredit = TCredit.objects.create(
            amount=10000, m_credit_category_sub=self.mcreditcategorysub, t_income=self.tincome, owner=self.owner)
        self.assertEqual(tcredit.amount, 10000)
        self.assertEqual(tcredit.m_credit_category_sub.name, "所得税")
        self.assertEqual(tcredit.m_credit_category_sub.m_credit_category_main.name, "税金")
        self.assertEqual(tcredit.t_income.payment_source_name, "フリーメーソン")
        self.assertEqual(tcredit.t_income.income_date, "2017-12-18")
