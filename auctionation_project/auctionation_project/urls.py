"""auctionation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_auctionation.views import LandingView, ItemStatsView
from api_auctionation.views import APIAuctionsView, APIItemStatsView, APIGetIconView, APIItemView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '',
        LandingView.as_view(),
        name='first'
    ),
    path(
        'api/auctions/<int:realm>/<str:faction>/<slug:slug>/',
        APIAuctionsView.as_view()
    ),
    path(
        'api/item_stats/<int:realm>/<str:faction>/<int:item_id>/',
        APIItemStatsView.as_view()
    ),
    path(
        'api/icon/<int:item_id>/',
        APIGetIconView.as_view()
    ),
    path(
        'api/item/<int:wow_id>/',
        APIItemView.as_view()
    ),
    path(
        '/item/<int:realm>/<str:faction>/<int:item_id>/',
        ItemStatsView.as_view()
    )
]
