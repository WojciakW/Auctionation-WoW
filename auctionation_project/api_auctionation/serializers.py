from rest_framework import serializers
from app_auctionation.models import Auction, Item, AuctionItemArchive

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = [
            'faction',
            'wow_item_id',
            'quantity',
            'realm_id',
            'buyout'
        ]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'wow_id',
            'name',
            'quality'
        ]


class ItemArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionItemArchive
        fields = '__all__'