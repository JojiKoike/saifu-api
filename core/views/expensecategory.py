from rest_framework import generics
from ..models.master.expense import MExpenseCategoryMain, MExpenseCategorySub
from ..serializers.expense import ExpenseCategorySerializer, \
    ExpenseCategoryMainSerializer, ExpenseCategorySubSerializer


class ExpenseCategoryList(generics.ListAPIView):
    """
    Expense Category List View (Full Tree Structure)
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseCategoryMainList(generics.ListCreateAPIView):
    """
    Expense Category Main List View (ONLY for Edit)
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategoryMainSerializer


class ExpenseCategoryMainDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Expense Category Main Detail View (ONLY for Edit)
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategoryMainSerializer


class ExpenseCategorySubList(generics.ListCreateAPIView):
    """
    Expense Category Sub List View (ONLY for Edit)
    """
    queryset = MExpenseCategorySub.objects.all()
    serializer_class = ExpenseCategorySubSerializer


class ExpenseCategorySubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Expense Category Sub Detail View (ONLY for Edit)
    """
    queryset = MExpenseCategorySub.objects.all()
    serializer_class = ExpenseCategorySubSerializer
