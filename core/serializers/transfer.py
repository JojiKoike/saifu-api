from rest_framework import serializers
from django.db import transaction
from ..models.transaction.transfer import TTransferBetweenSaifu
from core.models.user.saifu import USaifu


class TransferBetweenSaifuSerializer(serializers.ModelSerializer):
    from_u_saifu = serializers.UUIDField(required=True)
    to_u_saifu = serializers.UUIDField(required=True)
    """
    Transfer Between Saifu Serializer
    """
    class Meta:
        model = TTransferBetweenSaifu
        fields = ('id', 'transfer_date', 'amount', 'note', 'from_u_saifu', 'to_u_saifu')

    @transaction.atomic
    def create(self, validated_data):
        """
        Create Transfer Between Saifu Record
        :param validated_data:
        :return: TransferBetweenSaifu
        """

        transfer_amount = validated_data.pop('amount')
        owner = validated_data.pop('owner')
        u_saifu_query_set = USaifu.objects.filter(owner=owner)

        """
        Update From Saifu Current Balance
        """
        from_u_saifu = u_saifu_query_set.get(pk=validated_data.pop('from_u_saifu'))
        from_u_saifu.currentBalance -= transfer_amount
        from_u_saifu.save()
        """
        Update To Saifu Current Balance
        """
        to_u_saifu = u_saifu_query_set.get(pk=validated_data.pop('to_u_saifu'))
        to_u_saifu.currentBalance += transfer_amount
        to_u_saifu.save()
        """
        Create Transfer Between Saifu Transaction Record
        """
        transfer_between_saifu = TTransferBetweenSaifu.objects.create(amount=transfer_amount,
                                                                      from_u_saifu=from_u_saifu,
                                                                      to_u_saifu=to_u_saifu, owner=owner,
                                                                      **validated_data)

        return transfer_between_saifu
