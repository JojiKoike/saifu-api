from core.serializers.income import IncomeEditSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class IncomeEdit(APIView):

    def post(self, request, format=None):
        serializer = IncomeEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
