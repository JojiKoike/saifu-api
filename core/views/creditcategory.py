from rest_framework import generics
from ..models.master.credit import MCreditCategoryMain, MCreditCategorySub
from ..serializers.credit import CreditCategorySerializer, \
    CreditCategoryMainSerializer, CreditCategorySubSerializer


class CreditCategoryList(generics.ListAPIView):
    """
    Credit Category List View (Full Tree Structure)
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategorySerializer


class CreditCategoryMainList(generics.ListCreateAPIView):
    """
    Credit Category Main ListView
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategoryMainSerializer


class CreditCategoryMainDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Credit Category Main Detail
    """
    queryset = MCreditCategoryMain.objects.all()
    serializer_class = CreditCategoryMainSerializer


class CreditCategorySubList(generics.ListCreateAPIView):
    """
    Credit Category Sub ListView
    """
    queryset = MCreditCategorySub.objects.all()
    serializer_class = CreditCategorySubSerializer


class CreditCategorySubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Credit Category Sub Detail
    """
    queryset = MCreditCategorySub.objects.all()
    serializer_class = CreditCategorySubSerializer