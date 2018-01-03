from .base import viewbase
from ..models.master.credit import MCreditCategoryMain
from ..models.transaction.credit import TCredit
from ..serializers.credit import CreditCategorySerializer, CreditSerializer


class CreditCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Credit Category List
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategorySerializer


class CreditViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Credit
    """
    serializer_class = CreditSerializer

    def get_queryset(self):
        return TCredit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
