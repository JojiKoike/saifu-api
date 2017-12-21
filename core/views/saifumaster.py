from rest_framework import generics
from ..models.master.saifu import MSaifuCategory, MSaifu
from ..serializers.saifu import SaifuCategorySerializer, SaifuSerializer


class SaifuCategoryList(generics.ListCreateAPIView):
    """
    Saifu Category List View
    """
    queryset = MSaifuCategory.objects.all()
    serializer_class = SaifuCategorySerializer


class SaifuCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Saifu Category Detail View
    """
    queryset = MSaifuCategory.objects.all()
    serializer_class = SaifuCategorySerializer


class SaifuList(generics.ListCreateAPIView):
    """
    Saifu List View
    """
    queryset = MSaifu.objects.all()
    serializer_class = SaifuSerializer


class SaifuDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Saifu Detail View
    """
    queryset = MSaifu.objects.all()
    serializer_class = SaifuSerializer
