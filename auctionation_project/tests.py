from django.test import TestCase
import pytest
from faker import Faker
from django.contrib.auth.models import User
from app_auctionation.models import UserItemObserved, Comment
# Create your tests here.


# ----------tests to check if every APP url is reachable:----------

@pytest.mark.django_db
def test_reachable_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_reachable_login_page(client):
    response = client.get('/login/')
    assert response.status_code == 200


def test_reachable_register_page(client):
    response = client.get('/register/')
    assert response.status_code == 200


def test_reachable_reset_password(client):
    response = client.get('/change_password/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_reachable_item_stats(client, realm, faction, item):
    response = client.get(f'/item/{realm.id}/{faction}/{item.wow_id}/')
    assert response.status_code == 200


# ----------tests to check if every API url is reachable:----------

@pytest.mark.django_db
def test_reachable_api_auctions(client, realm, faction, item):
    url = f'/api/auctions/{realm.id}/{faction}/{item.slug}/'

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_reachable_api_icons(client, item):
    url = f'/api/icon/{item.wow_id}/'

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_reachable_api_item_stats(client, realm, faction, item):

    url = f'/api/item_stats/{realm.id}/{faction}/{item.id}/'

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_reachable_api_item(client, item):

    url = f'/api/item/{item.wow_id}/'

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_reachable_api_item_slug(client, item):

    url = f'/api/item/{item.slug}/'

    response = client.get(url)

    assert response.status_code == 200


# ----------tests to check if registration is correct:----------

@pytest.mark.django_db
def test_register_user_correct(client):
    data = {
            'username': 'test',
            'password': 'test123321test2',
            'password2': 'test123321test2',
            'email': 'test@test.com'
        }

    response = client.post(
        '/register/',
        data=data
    )

    assert User.objects.filter(
        username=data['username'],
    ).exists()


@pytest.mark.django_db
def test_register_user_username_already_exists(client):
    data = {
            'username': 'test',
            'password': 'test123321test2',
            'password2': 'test123321test2',
            'email': 'test@test.com'
        }

    response = client.post(
        '/register/',
        data=data
    )

    data = {
            'username': 'test',
            'password': 'test123321test2',
            'password2': 'test123321test2',
            'email': 'test2@test.com'
        }

    response = client.post(
        '/register/',
        data=data
    )

    assert not User.objects.filter(
        username=data['username'],
        email=data['email']
    ).exists()


@pytest.mark.django_db
def test_register_user_wrong_password(client):
    data = {
            'username': 'test',
            'password': 'test123321test2',
            'password2': 'qwerty',
            'email': 'test@test.com'
        }

    response = client.post(
        '/register/',
        data=data
    )

    assert not User.objects.filter(
        username=data['username'],
    ).exists()


@pytest.mark.django_db
def test_register_user_empty_credentials(client):
    data = {
            'username': '',
            'password': 'test123321test2',
            'password2': 'test123321test2',
            'email': 'test@test.com'
        }

    response = client.post(
        '/register/',
        data=data
    )

    assert not User.objects.filter(
        username=data['username'],
    ).exists()


# ----------login tests:----------

@pytest.mark.django_db
def test_login(client, create_test_user, password):
    user = create_test_user

    assert client.login(
        username=user.username,
        password=password
    )


@pytest.mark.django_db
def test_login_redirect(client, create_test_user, password):
    user = create_test_user

    response = client.post(
        '/login/?next=/',
        data={
            'username': user.username,
            'password': password
        }
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_login_redirect_item(client, create_test_user, password, item, realm, faction):
    user = create_test_user

    response = client.post(
        f'/login/?next=/item/{realm.id}/{faction}/{item.wow_id}/',
        data={
            'username': user.username,
            'password': password
        }
    )

    assert response.status_code == 302


# ----------forms tests:----------

@pytest.mark.django_db
def test_item_forms_logged_in(client, create_test_user, password, item, realm, faction):
    user = create_test_user

    client.login(
        username=user.username,
        password=password
    )

    response = client.get(f'/item/{realm.id}/{faction}/{item.wow_id}/').content
    response_decoded = response.decode('utf-8')

    assert response_decoded.count('form method="POST"') == 2


@pytest.mark.django_db
def test_item_forms_not_logged_in(client, create_test_user, password, item, realm, faction):

    response = client.get(f'/item/{realm.id}/{faction}/{item.wow_id}/').content
    response_decoded = response.decode('utf-8')

    assert response_decoded.count('form method="POST"') == 0


@pytest.mark.django_db
def test_item_observed(client, create_test_user, password, item, realm, faction):
    user = create_test_user

    client.login(
        username=user.username,
        password=password
    )

    response = client.post(
        f'/item/{realm.id}/{faction}/{item.wow_id}/',
        data={
            'observed': 'False'
        }
    )

    assert UserItemObserved.objects.filter(
        user=user,
        faction=faction,
        realm=realm,
        item=item
    ).exists()


@pytest.mark.django_db
def test_item_not_observed(client, create_test_user, password, item, realm, faction):
    user = create_test_user

    client.login(
        username=user.username,
        password=password
    )

    response = client.post(
        f'/item/{realm.id}/{faction}/{item.wow_id}/',
        data={
            'observed': 'False'
        }
    )

    response = client.post(
        f'/item/{realm.id}/{faction}/{item.wow_id}/',
        data={
            'observed': 'True'
        }
    )

    assert not UserItemObserved.objects.filter(
        user=user,
        faction=faction,
        realm=realm,
        item=item
    ).exists()


@pytest.mark.django_db
def test_comment(client, create_test_user, password, item, realm, faction):
    user = create_test_user

    client.login(
        username=user.username,
        password=password
    )

    faker = Faker()
    content = faker.text()

    response = client.post(
        f'/comment/{realm.id}/{faction}/{item.wow_id}/?next=/item/{realm.id}/{faction}/{item.wow_id}/',
        data={
            'content': content
        }
    )

    assert response.status_code == 302

    assert Comment.objects.filter(
        user=user,
        faction=faction,
        item=item,
        realm=realm,
        content=content
    )
