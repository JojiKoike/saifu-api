from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models.master.saifu import MSaifuCategory, MSaifu
from ..serializers.saifu import SaifuCategorySerializer, SaifuSerializer


class SaifuCategoryList(generics.ListCreateAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    """
    Saifu Category List View
    """
    queryset = MSaifuCategory.objects.all()
    serializer_class = SaifuCategorySerializer


class SaifuCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    """
    Saifu Category Detail View
    """
    queryset = MSaifuCategory.objects.all()
    serializer_class = SaifuCategorySerializer


class SaifuList(generics.ListCreateAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    """
    Saifu List View
    """
    queryset = MSaifu.objects.all()
    serializer_class = SaifuSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(owner=self.request.user)


class SaifuDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    """
    Saifu Detail View
    """
    queryset = MSaifu.objects.all()
    serializer_class = SaifuSerializer
