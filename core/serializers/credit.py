from rest_framework import serializers
from ..models.master.credit import MCreditCategoryMain, MCreditCategorySub


class CreditCategoryMainSerializer(serializers.ModelSerializer):
    """
    Credit Category (Main) Serializer
    """
    class Meta:
        model = MCreditCategoryMain
        fields = ('id', 'name')


class CreditCategorySubSerializer(serializers.ModelSerializer):
    """
    Credit Category (Sub) Serializer
    """
    class Meta:
        model = MCreditCategorySub
        fields = ('id', 'name', 'mCreditCategoryMain')


class CreditCategorySerializer(serializers.ModelSerializer):
    credit_category_subs = CreditCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = MCreditCategoryMain
        fields = ('id', 'name', 'credit_category_subs')
