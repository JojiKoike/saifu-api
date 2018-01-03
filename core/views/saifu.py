from core.models.master.saifu import MSaifuCategory
from core.models.user.saifu import USaifu
from .base import viewbase
from ..serializers.saifu import SaifuCategorySerializer, SaifuSerializer


class SaifuCategoryViewSet(viewbase.AdminEditableViewSetBase):
    """
    A ViewSet for Saifu Category
    """
    queryset = MSaifuCategory.objects.all()
    serializer_class = SaifuCategorySerializer


class SaifuViewSet(viewbase.IsOwnerOnlyViewSetBase):
    """
    A ViewSet for Saifu
    """
    serializer_class = SaifuSerializer

    def get_queryset(self):
        return USaifu.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
