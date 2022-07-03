from django.db import models, connection, transaction
from django.template.defaultfilters import slugify
# Create your models here.


class Dates(models.Model):
    value = models.DateTimeField(auto_now_add=True)


class Auction(models.Model):
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
    locale = models.CharField(max_length=8)
    api_id = models.IntegerField()
    name = models.CharField(max_length=64)


class Item(models.Model):
    wow_id = models.IntegerField()
    name = models.CharField(
        max_length=256,
        null=True,
        default=None
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
