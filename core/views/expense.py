from .base import viewbase
from ..models.master.expense import MExpenseCategoryMain, MExpenseCategorySub
from ..models.transaction.expense import TExpense
from ..serializers.expense import ExpenseCategorySerializer, \
    ExpenseCategoryMainSerializer, ExpenseCategorySubSerializer, \
    ExpenseSerializer


class ExpenseCategoryViewSet(viewbase.ReadOnlyViewSetBase):
    """
    A ViewSet for Expense Category List
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseCategoryMainViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Expense Category Main List
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategoryMainSerializer


class ExpenseCategorySubViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Expense Category Sub List
    """
    queryset = MExpenseCategorySub.objects.all()
    serializer_class = ExpenseCategorySubSerializer


class ExpenseViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Expense
    """
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return TExpense.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
