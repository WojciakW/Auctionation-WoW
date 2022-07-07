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
from app_auctionation.views import (
    LandingView,
    ItemStatsView,
    LoginView,
    RegisterView,
    LogoutView,
    ResetPasswordView,
    CommentView
)
from api_auctionation.views import (
    APIAuctionsView,
    APIItemStatsView,
    APIGetIconView,
    APIItemView,
    APIItemViewSlug,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API URLS:
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
        'api/item/<slug:slug>/',
        APIItemViewSlug.as_view()
    ),
    # APP URLS:
    path(
        'item/<int:realm>/<str:faction>/<int:item_id>/',
        ItemStatsView.as_view()
    ),
    path(
        '',
        LandingView.as_view(),
    ),
    path(
        'login/',
        LoginView.as_view()
    ),
    path(
        'register/',
        RegisterView.as_view()
    ),
    path(
        'logout/',
        LogoutView.as_view()
    ),
    path(
        'change_password/',
        ResetPasswordView.as_view()
    ),
    path(
        'comment/<int:realm>/<str:faction>/<int:item_id>/',
        CommentView.as_view()
    )
]
