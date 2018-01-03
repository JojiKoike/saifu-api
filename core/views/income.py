from .base import viewbase
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from ..models.transaction.income import TIncome
from ..serializers.income import IncomeCategorySerializer, IncomeCategoryMainSerializer, \
    IncomeCategorySubSerializer, IncomeSerializer


class IncomeCategoryViewSet(viewbase.ReadOnlyViewSetBase):
    """
    A ViewSet for Income Category List
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategorySerializer


class IncomeCategoryMainViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Income Category Main List
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategoryMainSerializer


class IncomeCategorySubViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Income Category Sub List
    """
    queryset = MIncomeCategorySub.objects.all()
    serializer_class = IncomeCategorySubSerializer


class IncomeViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Income
    """
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return TIncome.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
