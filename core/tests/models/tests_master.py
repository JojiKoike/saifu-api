from django.test import TestCase
from core.models.master.income import *
from core.models.master.expense import *
from core.models.master.credit import *
from core.models.master.saifu import *


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
        incomecategorysub = MIncomeCategorySub(mIncomeCategoryMain=incomecategorymain, name="家賃収入")
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
        expensecategorysub = MExpenseCategorySub(mExpenseCategoryMain=expensecategorymain, name="洗剤")
        self.assertEqual(expensecategorysub.name, "洗剤")


class MCreditCategoryMainTests(TestCase):
    """
    Credit Category Main Master Tests
    """

    def setUp(self):
        MCreditCategoryMain.objects.create(name="税金")

    def test_MCreditCategoryMainName_Saved_Correctly(self):
        mCreditCategoryMain = MCreditCategoryMain.objects.get(name="税金")
        self.assertEqual(mCreditCategoryMain.name, "税金")


class MCreditCategorySubTests(TestCase):
    """
    Credit Category Sub Master Tests
    """

    def setUp(self):
        MCreditCategoryMain.objects.create(name="社会保険料")

    def test_MCreditCategorySubName_Saved_Correctly(self):
        creditCategoryMain = MCreditCategoryMain.objects.get(name="社会保険料")
        MCreditCategorySub.objects.create(name="厚生年金保険料", mCreditCategoryMain=creditCategoryMain)
        mCreditCategorySub = MCreditCategorySub.objects.get(name="厚生年金保険料")
        self.assertEqual(mCreditCategorySub.name, "厚生年金保険料")
        self.assertEqual(mCreditCategorySub.mCreditCategoryMain.name, "社会保険料")


class MSaifuCategoryTests(TestCase):
    """
    Saifu Category Master Tests
    """

    def setUp(self):
        MSaifuCategory.objects.create(name="銀行口座")

    def test_MSaifuName_Saved_Correctly(self):
        mSaifuCategory = MSaifuCategory.objects.get(name="銀行口座")
        self.assertEqual(mSaifuCategory.name, "銀行口座")

        """
        TODO 名称重複登録をはねる事をテスト
        """


class MSaifuTests(TestCase):
    """
    Saifu Master Tests
    """

    def setUp(self):
        MSaifuCategory.objects.create(name="電子マネー")

    def test_MSaifu_Saved_Correctly(self):
        saifuCategory = MSaifuCategory.objects.get(name="電子マネー")
        mSaifu = MSaifu.objects.create(name="Suica", currentBalance=5000, mSaifuCategory=saifuCategory)
        self.assertEqual(mSaifu.name, "Suica")
        self.assertEqual(mSaifu.mSaifuCategory.name, "電子マネー")
