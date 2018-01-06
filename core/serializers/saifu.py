from rest_framework import serializers
from django.db import transaction
from core.models.master.saifu import MSaifuCategoryMain, MSaifuCategorySub
from core.models.user.saifu import USaifu


class SaifuCategorySubSerializer(serializers.ModelSerializer):
    """
    Saifu Category Sub Serializer
    """
    class Meta:
        model = MSaifuCategorySub
        fields = ('id', 'name')


class SaifuCategorySerializer(serializers.ModelSerializer):
    """
    Saifu Category Serializer
    """
    m_saifu_category_subs = SaifuCategorySubSerializer(many=True)

    class Meta:
        model = MSaifuCategoryMain
        fields = ('id', 'name', 'm_saifu_category_subs')

    def create(self, validated_data):
        m_saifu_category_subs_data = validated_data.pop('m_saifu_category_subs')
        m_saifu_category_main = MSaifuCategoryMain.objects.create(**validated_data)
        for m_saifu_category_sub_data in m_saifu_category_subs_data:
            MSaifuCategorySub.objects.create(m_saifu_category_main=m_saifu_category_main,
                                             **m_saifu_category_sub_data)
        return m_saifu_category_main


class SaifuSerializer(serializers.ModelSerializer):
    """
    Saifu Serializer
    """
    class Meta:
        model = USaifu
        fields = ('id', 'name', 'current_balance', 'm_saifu_category_sub')
