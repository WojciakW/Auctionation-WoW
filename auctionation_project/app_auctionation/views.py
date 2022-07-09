"""
Auctionation Web APP endpoint views.
"""
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import (
    Realms,
    Dates,
    AuctionItemArchive,
    Item,
    UserItemObserved,
    Comment
)
from .forms import UserCreateForm, UserLoginForm, UserResetPasswordForm, CommentForm
from django.views import View
from datetime import datetime


class LandingView(View):
    """
        Landing page:
            -GET: Display search field, Observed Items list (logged users only).
    """
    def get(self, request):
        realms = Realms.objects.all()
        try:
            data_time = Dates.objects.all().order_by('-id').first().value
        except AttributeError:
            data_time = None

        if request.user.is_authenticated:
            user = request.user
            user_observed_items = UserItemObserved.objects.filter(user_id=user.id)

            return render(
                request,
                'landing.html',
                context={
                    'realms': realms,
                    'data_time': data_time,
                    'user_observed_items': user_observed_items
                }
            )

        return render(
            request,
            'landing.html',
            context={
                'realms': realms,
                'data_time': data_time
            }
        )


class ItemStatsView(View):
    """
        View for displaying chosen item stats:
            -GET: A base to put the graphs on, display users comments
            -POST: Add/remove specific item to/from Observed Items list (logged users only).
    """
    now = datetime.now()

    def get(self, request, realm, faction, item_id):
        item = Item.objects.get(wow_id=item_id)
        realm = Realms.objects.get(id=realm)
        try:
            data_time = Dates.objects.all().order_by('-id').first().value
        except AttributeError:
            data_time = None

        comments = Comment.objects.filter(
            realm=realm,
            faction=faction,
            item_id=item.id
        ).order_by('-created')

        if faction == 'a':
            faction_name = 'Alliance'
        elif faction == 'h':
            faction_name = 'Horde'

        if request.user.is_authenticated:
            user = request.user

            if UserItemObserved.objects.filter(
                user_id=user.id,
                item_id=item.id,
                realm_id=realm,
                faction=faction
            ).exists():
                observed = True

            else:
                observed = False

            return render(
                request,
                'item_template.html',
                context={
                    'item': item,
                    'realm': realm,
                    'data_time': data_time,
                    'faction': faction,
                    'faction_name': faction_name,
                    'observed': observed,
                    'comments': comments,
                    'now': self.now
                }
            )

        return render(
            request,
            'item_template.html',
            context={
                'item': item,
                'realm': realm,
                'data_time': data_time,
                'faction': faction,
                'faction_name': faction_name,
                'comments': comments,
                'now': self.now
            }
        )

    def post(self, request, realm, faction, item_id):
        if request.user.is_authenticated:
            item = Item.objects.get(wow_id=item_id)

            if AuctionItemArchive.objects.filter(
                realm_id=realm,
                faction=faction,
                item_id=item.id
            ) is None:
                return Http404

            observed = request.POST.get('observed')

            if observed == 'False':
                UserItemObserved.objects.create(
                    item_id=item.id,
                    user_id=request.user.id,
                    faction=faction,
                    realm_id=realm
                )

                return redirect(request.path)

            elif observed == 'True':
                observed_item = get_object_or_404(
                    UserItemObserved,
                    user_id=request.user.id,
                    realm_id=realm,
                    faction=faction,
                    item_id=item.id
                )
                observed_item.delete()

                return redirect(request.path)

        else:
            raise PermissionDenied()


class LoginView(View):
    """
        Simple login view:
            -GET: Display login form.
            -POST: Validate data, make an attempt to log in.
    """
    def get(self, request):
        return render(
            request,
            'login.html',
        )

    def post(self, request):
        form = UserLoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = authenticate(
                username=username,
                password=password
            )

            if user:
                login(request, user)
                previous_page = request.GET.get('next')
                return redirect(previous_page)

            else:
                msg="Wrong username or password"
                return render(
                    request,
                    'login.html',
                    context={
                        'msg': msg
                    }
                )
        else:
            return render(
                request,
                'login.html'
            )


class LogoutView(View):
    """
        Logout view. Displays nothing, only logs user out.
    """
    def get(self, request):
        logout(request)
        previous_page = request.GET.get('next')
        return redirect(previous_page)


class RegisterView(View):
    """
        Simple register view:
            -GET: Display register form consisting of username, one-time repeated password, email
            -POST: Validate given data, create new user
    """
    def get(self, request):
        form = UserCreateForm()
        return render(
            request,
            'register.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                email=data.get('email')
            )

            return redirect('/')

        else:
            return render(
                request,
                'register.html',
                context={
                    'form': form
                }
            )


class ResetPasswordView(View):
    """
        Change password view:
            -GET: Display form consisting of username, current password, one-time repeated new password
            -POST: Validate data, save to user database
    """
    def get(self, request):
        form = UserResetPasswordForm()

        return render(
            request,
            'reset_password.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        form = UserResetPasswordForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')

            user = User.objects.get(username=username)

            user.set_password(data.get('new_password'))
            user.save()

            return redirect('/')

        else:
            return render(
                request,
                'reset_password.html',
                context={
                    'form': form
                }
            )


class CommentView(View):
    """
        View for adding comment to database (logged users only):
            -POST: Add new user comment on item
    """
    def post(self, request, realm, faction, item_id):
        if request.user.is_authenticated:
            form = CommentForm(request.POST)

            if form.is_valid():
                item = get_object_or_404(Item, wow_id=item_id)
                user = request.user

                Comment.objects.create(
                    user=user,
                    content=request.POST.get('content'),
                    faction=faction,
                    item_id=item.id,
                    realm_id=realm
                )

            previous_page = request.GET.get('next')
            return redirect(previous_page)

        else:
            raise PermissionDenied()
