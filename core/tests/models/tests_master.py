from django.test import TestCase
from core.models.master.income import *
from core.models.master.expense import *


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

