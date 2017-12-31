from rest_framework import serializers
from ..models.master.credit import MCreditCategoryMain, MCreditCategorySub
from ..models.transaction.credit import TCredit


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
        fields = ('id', 'name', 'm_credit_category_main')


class CreditCategorySerializer(serializers.ModelSerializer):
    """
    Credit Category (Main & Sub) Serializer
    """
    m_credit_category_subs = CreditCategorySubSerializer(many=True, read_only=True)

    class Meta:
        model = MCreditCategoryMain
        fields = ('id', 'name', 'm_credit_category_subs')


class CreditSerializer(serializers.ModelSerializer):
    """
    Credit Transaction Serializer
    """
    class Meta:
        model = TCredit
        fields = ('id', 'amount', 'm_credit_category_sub')
