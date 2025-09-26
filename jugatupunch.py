from dotenv import load_dotenv
import os

from discord import app_commands
import discord
from discord.ext import tasks
from typing import Optional

# from datetime import datetime
# from zoneinfo import ZoneInfo
import math
import random
import json

import requests

load_dotenv(dotenv_path="key.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
MEOW_GUILD_ID = 415003906951610378
RAT_GUILD_ID = 909589494490087494
BEENAN_ID = 207672531585466369
COW_ID = 334315992694128652
EMO_ID = 760609035346247710
MATCH_HISTORY_ID = 1420647209468166174
JUGATU_PUUID = "_F146yiCz2CqL5rRj2KmPpOu6qHhOQX_URjHQsNEYPnYHyM0E1GcgnqZdN_lRI-2AsNjrCTH-o0UOA"
JUGATU_NAME = "白蟹翡翠王"
JUGATU_TAG = "6 7"
# BEENAN_BET = datetime(2025, 9, 12, 18, 38, tzinfo=ZoneInfo("America/New_York"))
JUGATU_LP_GOAL = 3000

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

GUILD_LIST = [discord.Object(id=RAT_GUILD_ID), discord.Object(id=MEOW_GUILD_ID)]

CONFIG_FILE = "config.json"
CHAMPION_THUMBNAIL_URL = "https://ddragon.leagueoflegends.com/cdn/15.19.1/img/champion/"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
CHAMPION_ID = json.load(open("championID.json", "r"))

# useless test command
@tree.command(name="test", description="test random", guilds=GUILD_LIST)
async def test(interaction: discord.Interaction):
    start = 1758834195
    embed = discord.Embed(
        title="Jugatu Punch",
        description=f"START: <t:{start}:t>",
        colour=5763719,
    )
    # embed = discord.Embed(
    #     title="Jugatu Punch",
    #     description=""
    #     colour=3447003,
    #     # colour=15548997,
    # )
    embed.set_thumbnail(url="https://ddragon.leagueoflegends.com/cdn/15.19.1/img/champion/Aatrox.png")
    await interaction.response.send_message(embed=embed)

# converts seconds to MM:SS
def secondStringDisplay(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02}:{s:02}"

@tree.command(name="money", description="where's my money?", guilds=GUILD_LIST)
async def money(interaction: discord.Interaction):
    await interaction.response.send_message(f"<@{BEENAN_ID}> hasn't paid for <t:1757716680:R> days...")

TIER_LP = {
    "IRON"     : 0,
    "BRONZE"   : 400,
    "SILVER"   : 800,
    "GOLD"     : 1200,
    "PLATINUM" : 1600,
    "EMERALD"  : 2000,
    "DIAMOND"  : 2400,
    "MASTER"   : 2800,
}

RANK_LP = {
    "I"   : 300,
    "II"  : 200,
    "III" : 100,
    "IV"  : 0
}

@tree.command(name="jugatbet", description="gat", guilds=GUILD_LIST)
async def jugatbet(interaction: discord.Interaction):
    await interaction.response.send_message("Jugatu has made a bet with his master and overlord drbaobaomd for $100 CAD that he will be able to reach the astounding lp measurements of master 200lp by the end of the 2025 league of legends rank season est. date december 9th. Therefore the young white warrior is on his way to sweat his ass off thru the depths of iron 4 lp(he chose to start there, hesRegarded) and the swamps of saucelo and he is forced to stream it for the young baobao and not deafen him hahaha...")

# JUGATU PUNCH!
@tree.command(name="jugatupunch", description="Jugatu remaining LP", guilds=GUILD_LIST)
async def jugatupunch(interaction: discord.Interaction):
    HEADER = { 'X-Riot-Token': API_KEY }
    res = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{JUGATU_PUUID}", headers=HEADER)
    try:
        res.raise_for_status()
        data = next((rank for rank in res.json() if rank["queueType"] == "RANKED_SOLO_5x5"), None)
        if (data == None):
            await interaction.response.send_message(f"JUGATU IS UNRANKED")
            return
        totalLp = TIER_LP[data["tier"]] + RANK_LP[data["rank"]] + data["leaguePoints"]
        await interaction.response.send_message(f"JUGATU IS {data['tier']} {data['rank']} {data['leaguePoints']} LP ({data['wins']}-{data['losses']})\n{JUGATU_LP_GOAL - totalLp} LP REMAINING")
    except requests.HTTPError as e:
        print("HTTP ERROR:", e, res.text)
        await interaction.response.send_message("JUGATU'S GONE")

# target chat
# @tree.command(name="wherejugatu", description="Relocates which channel Jugatu speaks in", guilds=GUILD_LIST)
# async def wherejugatu(interaction: discord.Interaction, channel: discord.TextChannel):
#     config["channelID"] = channel.id
#     save_config(config)
#     await interaction.response.send_message("Jugatu now breathes in {channel.mention}")

MESSAGE_TAUNT = [
    ["JUGATUPUNCH!! He survives yet another day in the swamp of saucelo!",
    "JUGATUPUNCH!! Our white warrior prevails against SaurusNA once again!",
    "JUGATUPUNCH!! Jugatu figured out how to pull back his axes! SaurusNA!"],
    ["JugatuPunching...... He is currently fighting against the boxes of juice right now",
    "JugatuPunching...... The EMERALDKING is in the midst of battle against those banished from the lands of emerald",
    "JugatuPunching...... Jugatu is mid-pulling back his axes right now... Please try again later "],
    ["jugatupunch...... The EMERALDKING has lost this round against the invaders of sauce but... he will rise again",
    "jugatupunch...... Caseygg's little juggy wuggy is down for the count but Serenity Snow will help him recover",
    "jugatupunch...... Fuck... Jungle diff... Supp dif... fucking retards"],
]

# periodically check if jugaking is in-game 
@tasks.loop(minutes=1)
async def jugatucheck():
    HEADER = { 'X-Riot-Token': API_KEY }
    channel = client.get_guild(MEOW_GUILD_ID).get_channel(MATCH_HISTORY_ID)
    
    async def updateTrackedMessage():
        res = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/NA1_{config['match_id']}", headers=HEADER)
        try:
            res.raise_for_status()
            elores = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{JUGATU_PUUID}", headers=HEADER)
            eloData = next((rank for rank in elores.json() if rank["queueType"] == "RANKED_SOLO_5x5"), None)
            eloResult = f"{eloData['tier']} {eloData['rank']} {eloData['leaguePoints']} LP ({eloData['wins']}-{eloData['losses']})"
            totalLp = TIER_LP[eloData["tier"]] + RANK_LP[eloData["rank"]] + eloData["leaguePoints"]
            data = res.json()
            totalTime = data["info"]["gameDuration"]
            strTotalTime = secondStringDisplay(totalTime)
            timeStart = math.floor(data["info"]["gameCreation"] / 1000)
            # strTimeStart = datetime.fromtimestamp(timeStart / 1000, tz=ZoneInfo("America/New_York")).strftime("%I:%M:%S %p")
            timeEnd = math.floor(data["info"]["gameEndTimestamp"] / 1000)
            # strTimeEnd = datetime.fromtimestamp(timeEnd / 1000, tz=ZoneInfo("America/New_York")).strftime("%I:%M:%S %p")
            participate = next((participant for participant in data["info"]["participants"] if participant["puuid"] == JUGATU_PUUID), None)
            # hope it doesn't result with None
            win = participate["win"]
            kda = f"{participate['kills']}/{participate['deaths']}/{participate['assists']}"
            champion = participate["championName"]
            embed = discord.Embed(
                title=f"MATCH {"WIN" if win else "LOSS"} {totalLp - config["jugatu_total_lp"]} LP",
                description=f"{eloResult}\n{strTotalTime}\n<t:{timeStart}:t> - <t:{timeEnd}:t>\n{kda}\n{MESSAGE_TAUNT[0 if win else 2][random.randint(0,2)]}", # this hardcode randint is bad but i cba
                # description=f"{eloResult}\n{strTotalTime}\n{strTimeStart} - {strTimeEnd}\n{kda}\n{MESSAGE_TAUNT[0 if win else 2][random.randint(0,2)]}", # this hardcode randint is bad but i cba
                colour=(3447003 if win else 15548997)
            )
            embed.set_thumbnail(url=f"{CHAMPION_THUMBNAIL_URL}{champion}.png")
            msg = await channel.fetch_message(config["tracked_message_id"])
            await msg.edit(embed=embed)
            config["tracked_message_id"] = None
            config["match_id"] = None
            config["jugatu_total_lp"] = totalLp
            save_config(config)
        except requests.HTTPError as e:
            print("HTTP ERROR:", e, res.text)

    res = requests.get(f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{JUGATU_PUUID}", headers=HEADER)

    if (res.status_code == 200):
        data = res.json()
        if (config["match_id"] == None):
            timeStart = math.floor(data["gameStartTime"] / 1000)
            participant = next((participant for participant in data["participants"] if participant["puuid"] == JUGATU_PUUID))
            champion = CHAMPION_ID[f"{participant['championId']}"]
            embed = discord.Embed(
                title="MATCH IN SESSION",
                description=f"<t:{timeStart}:t>\n{MESSAGE_TAUNT[1][random.randint(0,2)]}",
                colour=5763719
            )
            embed.set_thumbnail(url=f"{CHAMPION_THUMBNAIL_URL}{champion}.png")
            msg = await channel.send(embed=embed)
            config["tracked_message_id"] = msg.id
            config["match_id"] = data["gameId"]
            save_config(config)
        elif (config["match_id"] != data["gameId"]):
            await updateTrackedMessage()
    elif (res.status_code == 404):
        if (config["tracked_message_id"] != None):
            await updateTrackedMessage()
    else:
        res.raise_for_status()

@tree.command(name="jugatuhere", description="jugatuhere", guilds=GUILD_LIST)
@app_commands.describe(
    jugatupunch="jugatupunch",
    battlebus="battlebus",
    jungler="jungler",
    serenity="serenity",
    baobao="baobao"
)
async def jugatuhere(
    interaction: discord.Interaction, 
    jugatupunch: Optional[str] = "Jugatupunch", 
    battlebus: Optional[str] = "battle bus", 
    jungler: Optional[str] ="jungler", 
    serenity: Optional[str] = "Serenity", 
    baobao: Optional[str] = "Baobao"
):
    str = f"**{jugatupunch}:** {jugatupunch} here.\n\n        *You've got the wrong {battlebus}..*\n\n**{jugatupunch}:** I knew my {jungler} was retarded..\n\n        *Okay, so you're looking for a {jugatupunch}?*\n\n**{jugatupunch}:** No, I am {jugatupunch}. I'm here for uh.. **{serenity}**.\n\n        *Yeah, you've got the wrong {battlebus}.*\n\n**{jugatupunch}:** ...So you're not gonna have sex tonight.\n\n        *Uh sir, I've got a **{baobao}** in the living room with his penis out!*\n\n**{jugatupunch}:** Huh..Okay, understood."
    await interaction.response.send_message(str)

# ready
@client.event
async def on_ready():
    # await update_nickname()
    # update_nickname.start()
    await jugatucheck()
    jugatucheck.start()
    for g in client.guilds:
        await tree.sync(guild=g)
    print(f"Logged in as {client.user}")

# keep_alive()
client.run(BOT_TOKEN)
