"""
Auctionation models.
"""

from django.db import models, connection, transaction
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Dates(models.Model):
    """
    Table for WoWAPI request time data.
    """
    value = models.DateTimeField(auto_now_add=True)


class Auction(models.Model):
    """
    Table for live auctions data.
    """
    realm = models.ForeignKey(
        to='Realms',
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    faction = models.CharField(
        max_length=1,
        default=None,
        null=True
    )
    wow_id = models.BigIntegerField()
    wow_item_id = models.IntegerField()
    buyout = models.IntegerField()
    quantity = models.IntegerField()
    api_request_time = models.ForeignKey(
        to=Dates,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    to_archive = models.BooleanField(
        default=False
    )


class AuctionItemArchive(models.Model):
    """
    Table for archived statistics data.
    """
    item = models.ForeignKey(
        to='Item',
        on_delete=models.CASCADE
    )
    date = models.ForeignKey(
        to='Dates',
        on_delete=models.CASCADE
    )

    mean_buyout = models.IntegerField()
    median_buyout = models.IntegerField()
    lowest_buyout = models.IntegerField()
    auctions_count = models.IntegerField()
    realm = models.ForeignKey(
        to='Realms',
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    faction = models.CharField(
        max_length=1,
        default=None,
        null=True
    )


class Realms(models.Model):
    """
    Table for WoWAPI realm data.
    """
    locale = models.CharField(max_length=8)
    api_id = models.IntegerField()
    name = models.CharField(max_length=64)


class Item(models.Model):
    """
    Table for item-specific data.
    """
    wow_id = models.IntegerField()
    name = models.CharField(
        max_length=256,
        null=True,
        default=None,
    )
    quality = models.CharField(
        max_length=32,
        null=True,
        default=None
    )
    archive_data = models.ManyToManyField(
        to='Dates',
        through='AuctionItemArchive'
    )
    slug = models.SlugField(
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)


class UserItemObserved(models.Model):
    """
    Table for user-observeditem relations.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
    )
    realm = models.ForeignKey(
        to=Realms,
        on_delete=models.CASCADE
    )
    faction = models.CharField(
        max_length=1,
        default=None,
        null=True
    )
    faction_name = models.CharField(
        max_length=16,
        default=None,
        null=True
    )


    def save(self, *args, **kwargs):
        self.item_name = Item.objects.get(id=self.item_id).name

        if self.faction == 'h':
            self.faction_name = 'Horde'
        elif self.faction == 'a':
            self.faction_name = 'Alliance'

        self.realm_name = Realms.objects.get(id=self.realm_id).name
        self.item_wow_id = Item.objects.get(id=self.item_id).wow_id

        if UserItemObserved.objects.filter(
            user=self.user_id,
            item=self.item_id,
            realm=self.realm_id,
            faction=self.faction
        ).exists():
            return None

        return super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Table for user comments.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
    )
    realm = models.ForeignKey(
        to=Realms,
        on_delete=models.CASCADE
    )
    faction = models.CharField(
        max_length=1,
        default=None,
        null=True
    )
