from rest_framework import serializers
from ..models.master.saifu import MSaifuCategory, MSaifu
from ..models.transaction.saifu import TSaifuHistory


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
        model = MSaifu
        fields = ('id', 'name', 'currentBalance', 'mSaifuCategory')
