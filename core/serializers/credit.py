from rest_framework import serializers
from ..models.master.credit import MCreditCategoryMain, MCreditCategorySub
from ..models.transaction.credit import TCredit


class CreditCategorySubSerializer(serializers.ModelSerializer):
    """
    Credit Category (Sub) Serializer
    """
    m_credit_category_main = serializers.UUIDField(read_only=True)

    class Meta:
        model = MCreditCategorySub
        fields = ('id', 'name', 'm_credit_category_main')


class CreditCategorySerializer(serializers.ModelSerializer):
    """
    Credit Category (Main & Sub) Serializer
    """
    m_credit_category_subs = CreditCategorySubSerializer(many=True)

    class Meta:
        model = MCreditCategoryMain
        fields = ('id', 'name', 'm_credit_category_subs')

    def create(self, validated_data):
        m_credit_category_subs_data = validated_data.pop('m_credit_category_subs')
        m_credit_category_main = MCreditCategoryMain.objects.create(**validated_data)
        for m_credit_category_sub_data in m_credit_category_subs_data:
            MCreditCategorySub.objects.create(m_credit_category_main=m_credit_category_main,
                                              **m_credit_category_sub_data)
        return m_credit_category_main


class CreditSerializer(serializers.ModelSerializer):
    """
    Credit Transaction Serializer
    """
    class Meta:
        model = TCredit
        fields = ('id', 'amount', 'm_credit_category_sub')
