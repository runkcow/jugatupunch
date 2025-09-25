from dotenv import load_dotenv
import os

from discord import app_commands
import discord
from discord.ext import tasks

# from flask import Flask
# from threading import Thread

from datetime import datetime
import random
from enum import Enum
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
JUGATU_PUUID = "_F146yiCz2CqL5rRj2KmPpOu6qHhOQX_URjHQsNEYPnYHyM0E1GcgnqZdN_lRI-2AsNjrCTH-o0UOA"
JUGATU_NAME = "白蟹翡翠王"
JUGATU_TAG = "6 7"
BEENAN_BET = datetime(2025, 9, 12, 18, 38)
JUGATU_LP_GOAL = 3000

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

GUILD_LIST = [discord.Object(id=RAT_GUILD_ID), discord.Object(id=MEOW_GUILD_ID)]

# app = Flask('')

# @app.route('/')
# def home():
#     return "Bot is running!"

# def run():
#     app.run(host='0.0.0.0', port=8080)

# def keep_alive():
#     t = Thread(target=run)
#     t.start()

CONFIG_FILE = "config.json"

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

# useless test command
@tree.command(name="test", description="test random", guilds=GUILD_LIST)
async def test(interaction: discord.Interaction):
    str = f"test: {random.randint(0, 9)}"
    await interaction.response.send_message(str)

# irrelevant nickname updating function that might get removed in the future
# @tasks.loop(hours=24)
# async def update_nickname():
#     g = client.get_guild(RAT_GUILD_ID)
#     if not g:
#         return
#     m = g.get_member(EMO_ID)
#     if not m:
#         return
#     daysPast = (datetime.now() - BEENAN_BET).days
#     nickname = f"WHERES MY MONEY? ({daysPast} days)"
#     await m.edit(nick=nickname)

@tree.command(name="money", description="where's my money?", guilds=GUILD_LIST)
async def money(interaction: discord.Interaction):
    await interaction.response.send_message(f"<@{BEENAN_ID}> hasn't paid for {(datetime.now() - BEENAN_BET).days} days...")

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
        data = res.json()[0]
        totalLp = TIER_LP[data["tier"]] + RANK_LP[data["rank"]] + data["leaguePoints"]
        await interaction.response.send_message(f"JUGATU IS {data["tier"]} {data["rank"]} {data["leaguePoints"]} LP ({data["wins"]}-{data["losses"]})\n{JUGATU_LP_GOAL - totalLp} LP REMAINING")
    except requests.HTTPError as e:
        print("HTTP ERROR:", e, res.text)
        await interaction.response.send_message("JUGATU'S GONE")

# target chat
# @tree.command(name="wherejugatu", description="Relocates which channel Jugatu speaks in", guilds=GUILD_LIST)
# async def wherejugatu(interaction: discord.Interaction, channel: discord.TextChannel):
#     config["channelID"] = channel.id
#     save_config(config)
#     await interaction.response.send_message("Jugatu now breathes in {channel.mention}")

# ready
@client.event
async def on_ready():
    # await update_nickname()
    # update_nickname.start()
    # await tree.sync()
    for g in client.guilds:
        await tree.sync(guild=g)
    print(f"Logged in as {client.user}")

# keep_alive()
client.run(BOT_TOKEN)
