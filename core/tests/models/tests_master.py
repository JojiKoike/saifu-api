from django.test import TestCase
from core.models.master.income import *
from core.models.master.expense import *
from core.models.master.credit import *
from core.models.master.saifu import *
from core.models.user.saifu import *
from django.contrib.auth.models import User


class MIncomeCategoryMainTests(TestCase):
    """
    Income Category Main Master Tests
    """

    def setUp(self):
        MIncomeCategoryMain.objects.create(name="給与")

    def test_IncomeCategoryName_Saved_Correctly(self):
        incomecategorymain = MIncomeCategoryMain.objects.get(name="給与")
        self.assertEqual(incomecategorymain.name, "給与")


class MIncomeCategorySubTests(TestCase):
    """
    Income Category Sub Master Tests
    """

    def setUp(self):
        MIncomeCategoryMain.objects.create(name="資産収入")

    def test_IncomeCategorySubName_Saved_Correctly(self):
        incomecategorymain = MIncomeCategoryMain.objects.get(name="資産収入")
        incomecategorysub = MIncomeCategorySub(m_income_category_main=incomecategorymain, name="家賃収入")
        self.assertEqual(incomecategorysub.name, "家賃収入")


class MExpenseCategoryMainTests(TestCase):
    """
    Expense Category Main Master Tests
    """

    def setUp(self):
        MExpenseCategoryMain.objects.create(name="食費")

    def test_ExpenseCategoryMainName_Saved_Correctly(self):
        expensecategorymain = MExpenseCategoryMain.objects.get(name="食費")
        self.assertEqual(expensecategorymain.name, "食費")


class MExpenseCategorySubTests(TestCase):
    """
    Expense Category Sub Master Tests
    """

    def setUp(self):
        MExpenseCategoryMain.objects.create(name="日用品費")

    def test_ExpenseCategorySubName_Saved_Correctly(self):
        expensecategorymain = MExpenseCategoryMain.objects.get(name="日用品費")
        expensecategorysub = MExpenseCategorySub(m_expense_category_main=expensecategorymain, name="洗剤")
        self.assertEqual(expensecategorysub.name, "洗剤")


class MCreditCategoryMainTests(TestCase):
    """
    Credit Category Main Master Tests
    """

    def setUp(self):
        MCreditCategoryMain.objects.create(name="税金")

    def test_MCreditCategoryMainName_Saved_Correctly(self):
        m_credit_category_main = MCreditCategoryMain.objects.get(name="税金")
        self.assertEqual(m_credit_category_main.name, "税金")


class MCreditCategorySubTests(TestCase):
    """
    Credit Category Sub Master Tests
    """

    def setUp(self):
        MCreditCategoryMain.objects.create(name="社会保険料")

    def test_MCreditCategorySubName_Saved_Correctly(self):
        credit_category_main = MCreditCategoryMain.objects.get(name="社会保険料")
        MCreditCategorySub.objects.create(name="厚生年金保険料", m_credit_category_main=credit_category_main)
        m_credit_category_sub = MCreditCategorySub.objects.get(name="厚生年金保険料")
        self.assertEqual(m_credit_category_sub.name, "厚生年金保険料")
        self.assertEqual(m_credit_category_sub.m_credit_category_main.name, "社会保険料")


class MSaifuCategoryMainTests(TestCase):
    """
    Saifu Category Main Master Tests
    """

    def test_MSaifuName_Saved_Correctly(self):
        m_saifu_category_main = MSaifuCategoryMain.objects.create(name="銀行口座")
        self.assertEqual(m_saifu_category_main.name, "銀行口座")


class MSaifuCategorySubTests(TestCase):
    """
    Saifu Category Sub Master Tests
    """
    m_saifu_category_main = None

    def setUp(self):
        self.m_saifu_category_main = MSaifuCategoryMain.objects.create(name="銀行口座")

    def test_MSaifuCategorySub_Name_Saved_Correctly(self):
        m_saifu_category_sub = MSaifuCategorySub.objects.create(name="普通口座",
                                                                m_saifu_category_main=self.m_saifu_category_main)
        self.assertEqual(m_saifu_category_sub.name, "普通口座")


class MSaifuTests(TestCase):
    """
    Saifu Master Tests
    """

    owner = None
    m_saifu_category_main = None
    m_saifu_category_sub = None

    def setUp(self):
        self.owner = User.objects.create_user("TestUser", 'test@test.com', 'password')
        self.m_saifu_category_main = MSaifuCategoryMain.objects.create(name='銀行口座')
        self.m_saifu_category_sub = MSaifuCategorySub.objects.create(name='普通預金',
                                                                     m_saifu_category_main=self.m_saifu_category_main)

    def test_MSaifu_Saved_Correctly(self):
        u_saifu = USaifu.objects.create(name="Suica", current_balance=5000,
                                        m_saifu_category_sub=self.m_saifu_category_sub, owner=self.owner)
        self.assertEqual(u_saifu.name, "Suica")
        self.assertEqual(u_saifu.current_balance, 5000)
        self.assertEqual(u_saifu.m_saifu_category_sub.name, "普通預金")
