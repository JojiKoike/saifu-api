from .base import viewbase
from ..models.master.expense import MExpenseCategoryMain
from ..models.transaction.expense import TExpense
from ..serializers.expense import ExpenseCategorySerializer, ExpenseSerializer


class ExpenseCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Expense Category List
    """
    queryset = MExpenseCategoryMain.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Expense
    """
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return TExpense.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
