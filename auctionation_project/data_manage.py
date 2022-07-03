from blizz_api_connection import api_response, get_api_token
import json
from app_auctionation.models import (
    Auction,
    Dates,
    Realms,
    AuctionItemArchive,
    Item
)
import time
from statistics import mean as st_mean, median
from datetime import datetime


# ``````````````````````
# constants
# ``````````````````````
API_URLS = {
    'realms': 'https://eu.api.blizzard.com/data/wow/realm/index?namespace=dynamic-classic-eu&locale=en_GB&access_token=',
    'auctions': [
        'https://eu.api.blizzard.com/data/wow/connected-realm/',
        '/auctions/',
        '?namespace=dynamic-classic-eu&locale=en_GB&access_token='
    ],
    'items': [
        'https://eu.api.blizzard.com/data/wow/item/',
        '?namespace=static-classic-eu&locale=en_GB&access_token='
    ]
}

ACCESS_TOKEN = get_api_token()


# ``````````````````````
# functions
# ``````````````````````
def populate_realms():
    response = api_response(
        API_URLS['realms'],
        ACCESS_TOKEN
    )
    print(response)
    realms_data_list = []

    response_json = json.loads(response.content)

    for i in range(len(response_json.get('realms')[:])):
        if response_json.get('realms')[i].get('name')[0:2] == 'EU':
            continue

        realm_data = {
            'locale': 'en_GB',
            'api_id': response_json.get('realms')[i].get('id'),
            'name': response_json.get('realms')[i].get('name')
        }

        realms_data_list.append(Realms(**realm_data))
        print(i)

    Realms.objects.bulk_create(realms_data_list)


def get_item_data():
    item_all_ids = Auction.objects.values('wow_item_id').distinct()

    for i, item_id in enumerate(item_all_ids):
        url = API_URLS['items'][0] + str(item_id['wow_item_id']) + API_URLS['items'][1]
        try:
            response = api_response(
                url,
                ACCESS_TOKEN
            )
            print(i, response)

            response_json = json.loads(response.content)

        except json.decoder.JSONDecodeError as err:
            print(err)
            continue

        item_data = {
            'wow_id': item_id['wow_item_id'],
            'name': response_json.get('name'),
            'quality': response_json.get('preview_item').get('quality').get('name')
        }

        Item.objects.create(**item_data)


def get_current_auctions_data():
    print('Fetching live auctions data...')

    api_request_time = Dates.objects.create()

    factions = {
        'a': 2,
        'h': 6
    }

    for realm in Realms.objects.all():
        for key in factions:
            connected = False

            start = time.time()

            url = API_URLS['auctions'][0] + str(realm.api_id) + API_URLS['auctions'][1] + str(factions[key]) + \
                  API_URLS['auctions'][2]

            while not connected:
                response, connection = api_response(
                    url,
                    ACCESS_TOKEN
                )

                if connection:
                    connected = True

            response_json = json.loads(response.content)

            allowed_items = [item['wow_id'] for item in Item.objects.values('wow_id')]

            auction_data_list = []
            try:
                for i in range(len(response_json.get('auctions')[:])):
                    if response_json.get('auctions')[i].get('buyout') == 0:
                        continue

                    if response_json.get('auctions')[i].get('item').get('id') not in allowed_items:
                        continue

                    auction_data = {
                        'wow_id': response_json.get('auctions')[i].get('id'),
                        'wow_item_id': response_json.get('auctions')[i].get('item').get('id'),
                        'buyout': response_json.get('auctions')[i].get('buyout'),
                        'api_request_time': api_request_time,
                        'faction': key,
                        'realm': realm,
                        'quantity': response_json.get('auctions')[i].get('quantity')
                    }

                    auction_data_list.append(Auction(**auction_data))

            except TypeError as err:
                print(err)

            Auction.objects.bulk_create(auction_data_list)

            end = time.time()

            print(f"Data from {realm.name, key} fetched and saved in {round(end - start, 2)} s.")


def change_archive_flag(value):
    print('Changing archive flags...')

    auctions = Auction.objects.all()
    if not value:
        auctions.filter(to_archive=True).update(to_archive=False)
        auctions_changed = auctions.filter(to_archive=False)
    elif value:
        auctions.filter(to_archive=False).update(to_archive=True)
        auctions_changed = auctions.filter(to_archive=True)

    print(f'Successfully changed archive flag for {len(auctions_changed)} auctions.')


def archive_data():
    print('Archiving data...')

    for realm in Realms.objects.all():
        for faction in 'a', 'h':
            auction_data_list = []
            unique_items = []
            for auction in Auction.objects.filter(to_archive=True).filter(realm=realm.id).filter(faction=faction):
                item = Item.objects.get(wow_id=auction.wow_item_id)
                if item.wow_id in unique_items:
                    continue

                calc = AuctionStatsCalculator(auction.wow_item_id, realm, faction)

                unique_items.append(item.wow_id)
                auction_stats_data = {
                    'item': item,
                    'auctions_count': calc.auctions_count,
                    'date': auction.api_request_time,
                    'lowest_buyout': calc.lowest_buyout,
                    'faction': auction.faction,
                    'realm': auction.realm,
                    'mean_buyout': calc.mean,
                    'median_buyout': calc.median
                }

                auction_data_unpacked = AuctionItemArchive(**auction_stats_data)
                auction_data_list.append(auction_data_unpacked)

            AuctionItemArchive.objects.bulk_create(auction_data_list)
            print(f'Data from {realm.name} {faction} succesfully archived ({len(unique_items)} entries).')


def delete_from_current_auctions():
    print('Deleting current auction entries...')

    for auction in Auction.objects.filter(to_archive=True):
        auction.delete()

    print('Auctions deleted.')


# ``````````````````````
# classes
# ``````````````````````
class AuctionStatsCalculator:
    def __init__(self, item, realm, faction):
        self.realm = realm
        self.faction = faction
        self.item = item
        self.Model = Auction
        self.loaded_objects = self.load_objects()
        self.buyout_list = self.get_unit_buyout_list()
        self.auctions_count = self.get_auction_count()
        self.is_only_one = self.set_flag()

        self.lowest_buyout = self.get_lowest_buyout()
        self.median = self.get_median()
        self.mean = self.get_mean()

    def __str__(self):
        return f"item_id: {self.item}"

    def load_objects(self):
        return self.Model.objects.all().filter(
            wow_item_id=self.item
        ).filter(
            realm=self.realm
        ).filter(
            faction=self.faction
        )

    def set_flag(self):
        if self.auctions_count == 1:
            return True
        else:
            return False

    def get_unit_buyout_list(self):
        return [obj.buyout / obj.quantity for obj in self.loaded_objects]

    def get_mean(self):
        if self.is_only_one:
            return self.buyout_list[0]

        return st_mean(self.buyout_list)

    def get_median(self):
        if self.is_only_one:
            return self.buyout_list[0]

        return median(self.buyout_list)

    def get_auction_count(self):
        return self.loaded_objects.count()

    def get_lowest_buyout(self):
        return self.loaded_objects.order_by('buyout').first().buyout


# ``````````````````````
# script execution
# ``````````````````````
while True:
    print(f'Data management on {datetime.now()}')

    connected = True
    change_archive_flag(True)
    get_current_auctions_data()
    archive_data()
    delete_from_current_auctions()

    print('Data management complete.')
    time.sleep(3600)
