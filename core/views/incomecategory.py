from rest_framework import generics
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub
from ..serializers.income import IncomeCategorySerializer, IncomeCategoryMainSerializer, IncomeCategorySubSerializer


class IncomeCategoryList(generics.ListAPIView):
    """
    Income Category List View (Full Tree Structure)
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategorySerializer


class IncomeCategoryMainList(generics.ListCreateAPIView):
    """
    Income Category Main List View (ONLY for Edit)
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategoryMainSerializer


class IncomeCategoryMainDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Income Category Main Detail View (ONLY for Edit)
    """
    queryset = MIncomeCategoryMain.objects.all()
    serializer_class = IncomeCategoryMainSerializer


class IncomeCategorySubList(generics.ListCreateAPIView):
    """
    Income Category Sub List View (ONLY for Edit)
    """
    queryset = MIncomeCategorySub.objects.all()
    serializer_class = IncomeCategorySubSerializer


class IncomeCategorySubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Income Category Sub Detail View (ONLY for Edit)
    """
    queryset = MIncomeCategorySub.objects.all()
    serializer_class = IncomeCategorySubSerializer