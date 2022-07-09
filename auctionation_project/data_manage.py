"""
Auctionation data management script.

In 1-hour cycle:
    - mark current auctions present in the 'Auctions' table as "to be archived",
    - fetch live auctions data from WoWAPI,
    - save fetched data into the 'Auctions' table and "mark it" as "to read" for AuctionationAPI,
    - calculate all statistics of entries present in 'Auctions' marked by "to be archived",
    - save those statistics into 'AuctionItemArchive' table,
    - delete all entries marked by "to be archived" from 'Auctions'

Run in django shell using terminal command:
    ./manage.py shell << data_manage.py

!!! Warning:
        script requires proper database setup, that is:
            - database creation,
            - correct django migrations,
            - populated 'Realms' table (can be done using 'populate_realms()' func below)
            - populated 'Items' table (can be done using 'get_item_data()' func below)


Once correctly run, it won't stop unless killed (ctrl+c) or got an unforeseen error.

"""

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
    """
    1. Get WoW API Realms data (code below only for EU realms),
    2. Write data into 'Realms' table.
    """
    connected = False

    while not connected:
        response, connection = api_response(
            API_URLS['realms'],
            ACCESS_TOKEN
        )

        if connection:
            connected = True

    realms_data_list = []

    response_json = json.loads(response.content)

    for i in range(len(response_json.get('realms')[1:5])):
        if response_json.get('realms')[i].get('name')[0:2] == 'EU':  # reject those realms that start with 'EU'
            continue

        realm_data = {
            'locale': 'en_GB',
            'api_id': response_json.get('realms')[i].get('id'),
            'name': response_json.get('realms')[i].get('name')
        }

        realms_data_list.append(Realms(**realm_data))

    Realms.objects.bulk_create(realms_data_list)


def get_item_data():
    """
    1. Get WoW API Items data (code below returns only items in id range 1000, 1100),
    2. Write data into 'Item' table.
    """

    for i in range(1000, 1100):
        url = API_URLS['items'][0] + str(i) + API_URLS['items'][1]

        connected = False

        while not connected:
            response, connection = api_response(
                url,
                ACCESS_TOKEN
            )

            if connection:
                connected = True

        if response.status_code != 200:
            continue

        response_json = json.loads(response.content)

        print(i)
        item_data = {
            'wow_id': response_json.get('id'),
            'name': response_json.get('name'),
            'quality': response_json.get('preview_item').get('quality').get('name')
        }

        Item.objects.create(**item_data)


def get_current_auctions_data():
    """
    In loop:
        - fetch live auctions data from WoW API for every realm present in Realms table and
          each of two faction sides (neutral auction house omitted),
        - write all the data into 'Auctions' table

    Note: from my experience, Blizzard API requests can return odd responses sometimes.

    """
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


def change_archive_flag(value: bool):
    """
    Switches 'to_archive' flag for all entries in the 'Auctions' table, target value specified as param.
    """
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
    """
    Archives the data using 'AuctionStatsCalculator' class:
        - calculates appropriate statistics for all the valid entries,
        - creates new objects in the 'AuctionItemArchive' table based on calculated data
    """
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
    """
    Deletes all the entries from the 'Auctions' table marked as 'to_archive'.
    """
    print('Deleting current auction entries...')

    for auction in Auction.objects.filter(to_archive=True):
        auction.delete()

    print('Auctions deleted.')


# ``````````````````````
# classes
# ``````````````````````
class AuctionStatsCalculator:
    """
    Calculator-style class used for auction statistics calculations.

    """
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
        """
        Returns all the valid auction entries.
        """
        return self.Model.objects.all().filter(
            wow_item_id=self.item,
            realm=self.realm,
            faction=self.faction
        )

    def set_flag(self):
        """
        Sets the 'is_only_one' attr.
        Required by 'statistics' python module.
        """
        if self.auctions_count == 1:
            return True
        else:
            return False

    def get_unit_buyout_list(self):
        """
        Calculates price per unit for all the entries.
        """
        return [obj.buyout / obj.quantity for obj in self.loaded_objects]

    def get_mean(self):
        """
        Calculates mean buyout.
        """
        if self.is_only_one:
            return self.buyout_list[0]

        return st_mean(self.buyout_list)

    def get_median(self):
        """
        Calculates median buyout.
        """
        if self.is_only_one:
            return self.buyout_list[0]

        return median(self.buyout_list)

    def get_auction_count(self):
        """
        Calculates item auctions count.
        """
        return self.loaded_objects.count()

    def get_lowest_buyout(self):
        """
        Returns the lowest buyout.
        """
        return self.loaded_objects.order_by('buyout').first().buyout


# ``````````````````````
# script execution
# ``````````````````````
while True:
    if len(Realms.objects.all()) == 0:
        print('Database startup...')

        populate_realms()
        get_item_data()
        get_current_auctions_data()

    print(f'Data management on {datetime.now()}')

    connected = True
    change_archive_flag(True)
    get_current_auctions_data()
    archive_data()
    delete_from_current_auctions()

    print('Data management complete.')
    time.sleep(3600)
