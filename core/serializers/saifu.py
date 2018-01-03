from rest_framework import serializers
from core.models.user.saifu import MSaifuCategory, USaifu


class SaifuCategorySerializer(serializers.ModelSerializer):
    """
    Saifu Category Serializer
    """
    class Meta:
        model = MSaifuCategory
        fields = ('id', 'name')


class SaifuSerializer(serializers.ModelSerializer):
    """
    Saifu Serializer
    """
    class Meta:
        model = USaifu
        fields = ('id', 'name', 'current_balance', 'm_saifu_category')
