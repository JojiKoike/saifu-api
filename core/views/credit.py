from .base import viewbase
from ..models.master.credit import MCreditCategoryMain, MCreditCategorySub
from ..models.transaction.credit import TCredit
from ..serializers.credit import CreditCategorySerializer, \
    CreditCategoryMainSerializer, CreditCategorySubSerializer, CreditSerializer


class CreditCategoryViewSet(viewbase.ReadOnlyViewSetBase):
    """
    A ViewSet for Credit Category List
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategorySerializer


class CreditCategoryMainViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Credit Category Main List
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategoryMainSerializer


class CreditCategorySubViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Credit Category Sub List
    """
    queryset = MCreditCategorySub.objects.all()
    serializer_class = CreditCategorySubSerializer


class CreditViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Credit
    """
    serializer_class = CreditSerializer

    def get_queryset(self):
        return TCredit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
