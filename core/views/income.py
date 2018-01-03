from .base import viewbase
from ..models.master.income import MIncomeCategoryMain
from ..models.transaction.income import TIncome
from ..serializers.income import IncomeCategorySerializer, IncomeSerializer


class IncomeCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Income Category List
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategorySerializer


class IncomeViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Income
    """
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return TIncome.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
