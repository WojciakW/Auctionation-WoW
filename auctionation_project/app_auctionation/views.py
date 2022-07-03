from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from .models import Auction, Realms
import requests
# Create your views here.
from django.views import View


# class FirstView(View):
#     pass
#     def get(self, request):
#         all_auctions = AuctionTEST.objects.all().order_by('-buyout')
#         paginator = Paginator(all_auctions, 10)
#
#         page = request.GET.get('page', 1)
#         all_auctions_on_page = paginator.page(page)
#
#         return render(
#             request,
#             'test.html',
#             context={
#                 'all_auctions_on_page': all_auctions_on_page
#             }
#         )
#
#     def post(self, request):
#         search = request.POST.get('search')
#         requests.get(f'https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&name.en_US={search}&orderby=id&_page=1&access_token=USHPrxtIW9KtEcG9gGPgZTBM0yKY4WKeS7')
#         entries = AuctionTEST.objects.all().filter()


class LandingView(View):
    def get(self, request):
        realms = Realms.objects.all()

        return render(
            request,
            'landing.html',
            context={
                'realms': realms
            }
        )


class ItemStatsView(View):
    def get(self, request):
        pass