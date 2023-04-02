import os
from typing import List

import disnake
import pandas as pd
from disnake.ext import commands

from services.blizzard_api_client import BlizzardApiClient
from services.quickchart_service import QuickChartService

bot = commands.InteractionBot()

week_type = commands.option_enum({"Tyrranical": "tyrranical", "Fortified": "fortified"})

@bot.slash_command()
async def opt_score(
        inter: disnake.CommandInteraction,
        users: str,
        week: week_type
):
    await inter.response.defer()
    users = users.split(',')
    if len(users) > 0:
        players = [u.split('@')[0] for u in users]
        realms = [u.split('@')[1] for u in users]
        plot = get_score_data(players, realms, week)
        await inter.send(plot)
    else:
        await inter.send("Need to specify users as <usernmae>@<realm>")


def get_score_data(players, realms, week):
    client = BlizzardApiClient()
    player_data = []
    for idx, name in enumerate(players):
        if len(realms) < idx:
            realm = realms[0]
        else:
            realm = realms[idx]

        player = client.player_mythic_details(name, realm)
        player_data.append(player)
    qcs = QuickChartService()
    plot = qcs.rating_bars(player_data, week)
    return plot

bot.run(os.environ['DISCORD_KEY'])

