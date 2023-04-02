import requests
import json
import os

from models import Player

BLIZ_ROOT = 'https://us.api.blizzard.com/'


class BlizzardApiClient:
    def __init__(self, client_id=os.environ['BLIZZ_ID'], client_secret=os.environ['BLIZZ_SECRET']):
        token_req = requests.post('https://oauth.battle.net/token', data={'grant_type': 'client_credentials'},
                                  auth=(client_id, client_secret))
        token = json.loads(token_req.content)
        self.token = token['access_token']
        self.season = self.get_current_season()
        self.dungeon_shorthands = {
            'Ruby Life Pools': 'RLP',
            'Halls of Valor': 'HOV',
            'Temple of the Jade Serpent': 'TJS',
            'The Azure Vault': 'AV',
            "Algeth'ar Academy": "AA",
            "The Nokhud Offensive": "NO",
            "Court of Stars": "CoS",
            "Shadowmoon Burial Grounds": "SBG"
        }

    def rename_keys(self, ratings: dict):
        keys = {}
        for k, v in ratings.items():
            keys[self.dungeon_shorthands[k]] = v
        return keys

    def player_mythic_details(self, player: str, realm: str):
        player, realm = player.lower(), realm.lower()
        url = f'{BLIZ_ROOT}profile/wow/character/{realm}/{player}/mythic-keystone-profile/season/{self.season}?namespace=profile-us&locale=en_US&access_token={self.token}'
        results = requests.get(url)
        data = results.json()
        best_runs = data["best_runs"]
        player = Player(player, realm, {}, {})
        for run in best_runs:
            rating = run["mythic_rating"]['rating']
            alt_rating = 2 * (run["map_rating"]['rating'] - 1.5 * rating)
            dungeon = run["dungeon"]["name"]
            affix = run["keystone_affixes"][0]["name"]
            if affix == "Fortified":
                if rating > 0 and (dungeon not in player.fort_keys.keys() or rating > player.fort_keys[dungeon]):
                    player.fort_keys[dungeon] = rating
                    if alt_rating <= rating:
                        player.tyrrannical_keys[dungeon] = alt_rating
            elif affix == "Tyrannical":
                if rating > 0 and (dungeon not in player.tyrrannical_keys.keys() or rating > player.tyrrannical_keys[dungeon]):
                    player.tyrrannical_keys[dungeon] = rating
                    if alt_rating <= rating:
                        player.fort_keys[dungeon] = alt_rating
        player.fort_keys = self.rename_keys(player.fort_keys)
        player.tyrrannical_keys = self.rename_keys(player.tyrrannical_keys)
        return player

    def get_current_season(self):
        url = f'{BLIZ_ROOT}/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token={self.token}'
        results = requests.get(url)
        data = results.json()
        return data["current_season"]["id"]
