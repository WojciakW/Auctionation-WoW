from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.views import View

import os

import json

from app_auctionation.models import (
    Auction,
    Item,
    AuctionItemArchive,
    Realms,
    Dates
)

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AuctionSerializer, ItemSerializer, ItemArchiveSerializer

file_dir = os.path.dirname(__file__)


class APIAuctionsView(ListAPIView):
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()

    def get_queryset(self):
        realm = self.kwargs['realm']
        faction = self.kwargs['faction']
        query = self.kwargs['slug']

        items = Item.objects.filter(slug__icontains=query)

        return Auction.objects.filter(
            faction=faction,
            realm_id=realm,
            wow_item_id__in=[item.wow_id for item in items[:]]
        ).order_by('wow_item_id')


class APIItemStatsView(APIView):
    def get(self, request, faction, realm, item_id):
        item_data = AuctionItemArchive.objects.filter(
            item_id=item_id,
            faction=faction,
            realm_id=realm
        )
        print('asd')
        serializer = ItemArchiveSerializer(item_data, many=True)

        return Response(serializer.data)


class APIGetIconView(View):
    def get(self, request, item_id):
        path = f'icons/{item_id}'

        with open(os.path.join(file_dir, path)+'.jpeg', 'rb') as icon:
            icon_data = icon.read()

        return HttpResponse(icon_data, content_type='image/jpeg')


class APIItemView(APIView):
    def get(self, request, wow_id):
        item = Item.objects.get(wow_id=wow_id)
        serializer = ItemSerializer(item)

        return Response(serializer.data)

