"""
Auctionation serializers for proper JSON API responses.
"""

from rest_framework import serializers
from app_auctionation.models import Auction, Item, AuctionItemArchive, Dates


class DateSerializer(serializers.Serializer):
    value = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


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
    date = DateSerializer()

    class Meta:
        model = AuctionItemArchive
        fields = [
            'auctions_count',
            'date',
            'lowest_buyout',
            'faction',
            'realm_id',
            'mean_buyout',
            'median_buyout',
            'item_id'
        ]