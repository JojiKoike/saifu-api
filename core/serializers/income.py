from rest_framework import serializers
from ..models.master.income import MIncomeCategoryMain, MIncomeCategorySub


class IncomeCategoryMainSerializer(serializers.ModelSerializer):
    """
    Income Category Sub Serializer
    """
    class Meta:
        model = MIncomeCategoryMain
        fields = ('id', 'name')


class IncomeCategorySubSerializer(serializers.ModelSerializer):
    """
    Income Category Sub Serializer
    """
    class Meta:
        model = MIncomeCategorySub
        fields = ('id', 'name', 'mIncomeCategoryMain')


class IncomeCategorySerializer(serializers.ModelSerializer):
    """
    Income Category Serializer (Main and Sub)
    """
    income_category_sub = IncomeCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = MIncomeCategoryMain
        fields = ('id', 'name', "income_category_sub")





