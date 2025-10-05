from dotenv import load_dotenv
import os

from discord import app_commands
import discord
from discord.ext import tasks
from typing import Optional

import math
import random
import json
from PIL import Image

import io
import requests

load_dotenv(dotenv_path="key.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
HEADER = { 'X-Riot-Token': API_KEY }
MEOW_GUILD_ID = 415003906951610378
RAT_GUILD_ID = 909589494490087494
MY_ID = 334315992694128652
BAOBAO_ID = 760330889762308134
BEENAN_ID = 207672531585466369
JUGATU_ID = 1057114471983743057

# test variables
# COW_ID = 334315992694128652
# EMO_ID = 760609035346247710

# 白蟹翡翠王 #6 7
# JUGATU_PUUID = "_F146yiCz2CqL5rRj2KmPpOu6qHhOQX_URjHQsNEYPnYHyM0E1GcgnqZdN_lRI-2AsNjrCTH-o0UOA"
# JUGATU_NAME = "白蟹翡翠王"
# JUGATU_TAG = "6 7"
# BEENAN_BET = datetime(2025, 9, 12, 18, 38, tzinfo=ZoneInfo("America/New_York"))
# JUGATU_LP_GOAL = 3000

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

QUEUE_ID = {}
res = requests.get("https://static.developer.riotgames.com/docs/lol/queues.json")
try:
    res.raise_for_status()
    data = res.json()
    for queue in data:
        if (queue["description"] == None):
            QUEUE_ID[queue["queueId"]] = "Null"
        elif (queue["description"].lower().endswith(" games")):
            QUEUE_ID[queue["queueId"]] = queue["description"][:-6]
        else:
            QUEUE_ID[queue["queueId"]] = queue["description"]
except requests.HTTPError as e:
    print(f"ERROR:", e, res.text)

BINGO_SIZE = 200
BINGO_BACKGROUND = Image.open("yagatuback.png").convert("RGBA").resize((BINGO_SIZE * 5, BINGO_SIZE * 5), Image.Resampling.BILINEAR)
BINGO_IMG_ID = [f for f in os.listdir("bingoimg") if f.lower().endswith(".png")]
BINGO_IMAGES = [
    (lambda img: img.resize(
        (int(img.width * min(BINGO_SIZE / img.width, BINGO_SIZE / img.height)),
         int(img.height * min(BINGO_SIZE / img.width, BINGO_SIZE / img.height))),
        Image.Resampling.BILINEAR))(Image.open(f"bingoimg/{name}").convert("RGBA"))
    for name in BINGO_IMG_ID
]
BINGO_CROSS = Image.open("xmarksthespot.png").convert("RGBA").resize((BINGO_SIZE, BINGO_SIZE), Image.Resampling.BILINEAR)

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

RANK_NUMERICAL = {
    "I"   : 1,
    "II"  : 2,
    "III" : 3,
    "IV"  : 4
}

# useless test command
@tree.command(name="test", description="test random", guilds=GUILD_LIST)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("test")

# syncs commands
@tree.command(name="sync", description="syncs commands", guilds=GUILD_LIST)
async def sync(interaction: discord.Interaction):
    if (interaction.user.id != MY_ID):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
    else:
        for g in client.guilds:
            await tree.sync(guild=g)

# converts seconds to MM:SS
def secondStringDisplay(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02}:{s:02}"

# where's my money?
@tree.command(name="money", description="where's my money?", guilds=GUILD_LIST)
async def money(interaction: discord.Interaction):
    await interaction.response.send_message(f"<@{BEENAN_ID}> should've paid <t:1757716680:R>...")

# unnecessary bet explanation command
@tree.command(name="jugatbet", description="gat", guilds=GUILD_LIST)
async def jugatbet(interaction: discord.Interaction):
    await interaction.response.send_message("Jugatu has made a bet with his master and overlord drbaobaomd for $100 CAD that he will be able to reach the astounding lp measurements of master 200lp by the end of the 2025 league of legends rank season est. date december 9th. Therefore the young white warrior is on his way to sweat his ass off thru the depths of iron 4 lp(he chose to start there, hesRegarded) and the swamps of saucelo and he is forced to stream it for the young baobao and not deafen him hahaha...")

# command to change bot profile picture
@tree.context_menu(name="JUGATUPUNCH!", guilds=GUILD_LIST)
async def makepfp(interaction: discord.Interaction, message: discord.Message):
    if not message.attachments: 
        await interaction.response.send_message("who?", ephemeral=True)
        return
    file = message.attachments[0] 
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        await interaction.response.send_message("i can't", ephemeral=True) 
        return
    try: 
        img = await file.read()
        await client.user.edit(avatar=img) 
        await interaction.response.send_message("we are here", ephemeral=True) 
    except discord.HTTPException as e: 
        if e.status == 429:
            await interaction.response.send_message("outagas", ephemeral=True)
        else:
            await interaction.response.send_message("aw shit something blew up", ephemeral=True)
            print("HTTP ERROR:", e)

# JUGATU PUNCH!
# checks remaining lp of a player, temporary function, main function should display rank of a player
@tree.command(name="jugatupunch", description="Who is who?", guilds=GUILD_LIST)
@app_commands.describe(player="noob")
@app_commands.choices(player=[app_commands.Choice(name=k, value=k) for k in config["players"]])
async def jugatupunch(interaction: discord.Interaction, player: Optional[str] = "jugatu"):
    respondStr = ""
    for puuid in config["accounts"]:
        if (config["accounts"][puuid]["owner"] != player):
            continue
        res = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}", headers=HEADER)
        if (res.status_code == 200):
            data = next((rank for rank in res.json() if rank["queueType"] == "RANKED_SOLO_5x5"), None)
            if (data == None):
                respondStr += f"{player.upper()} IS UNRANKED"
                return
            totalLp = TIER_LP[data["tier"]] + RANK_LP[data["rank"]] + data["leaguePoints"]
            accName = f"{config['accounts'][puuid]['username']} #{config['accounts'][puuid]['tag']}"
            respondStr += f"{accName} IS {data['tier']} {data['rank']} {data['leaguePoints']} LP ({data['wins']}-{data['losses']})\n{config['players'][player]['lp_goal'] - totalLp} LP REMAINING\n"
            config["accounts"][puuid]["lp"] = totalLp
            save_config(config)
        else:
            print(f"RECEIVED STATUS CODE {res.status_code} IN jugatupunch")
            respondStr += f"{player.upper()}'S GONE"
    respondStr += f"<#{config['players'][player]['output_channel_id']}>"
    await interaction.response.send_message(respondStr)

# command to add accounts
@tree.command(name="addaccount", description="Add accounts to track", guilds=GUILD_LIST)
@app_commands.describe(username="Account username", tag="Account tag without '#'", owner="Account owner")
@app_commands.choices(owner=[app_commands.Choice(name=k, value=k) for k in config["players"]])
async def addaccount(interaction: discord.Interaction, username: str, tag: str, owner: str):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command")
        return
    res = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}", headers=HEADER)
    if (res.status_code == 200):
        data = res.json()
        puuid = data["puuid"]
        eloRes = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}", headers=HEADER)
        eloData = next((rank for rank in eloRes.json() if rank["queueType"] == "RANKED_SOLO_5x5"), None)
        totalLp = TIER_LP[eloData["tier"]] + RANK_LP[eloData["rank"]] + eloData["leaguePoints"]
        config["accounts"][puuid] = {
            "owner": owner,
            "lp": totalLp,
            "message_id": None,
            "match_id": None,
            "active": False,
            "username": username,
            "tag": tag
        }
        save_config(config)
        await interaction.response.send_message(f"Succesfully added account {username} #{tag}", ephemeral=True)
    elif (res.status_code == 404):
        await interaction.response.send_message("Invalid username or tag", ephemeral=True)
    else:
        res.raise_for_status()
        await interaction.response.send_message("Problem has occurred...", ephemeral=True)

# command to remove accounts
@tree.command(name="removeaccount", description="Remove an account from tracked list", guilds=GUILD_LIST)
@app_commands.describe(account="Account name")
@app_commands.choices(account=[app_commands.Choice(name=f"{value['username']} #{value['tag']}", value=puuid) for puuid, value in config["accounts"].items()])
async def removeaccount(interaction: discord.Interaction, account: str):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["accounts"].pop(account)
    save_config(config)
    await interaction.response.send_message("Successfully removed account", ephemeral=True)

# command to change account owner
@tree.command(name="changeaccountowner", description="Change the owner of an account, manages which text channel tracked games output to", guilds=GUILD_LIST)
@app_commands.describe(account="Account name", owner="Owner name")
@app_commands.choices(
    account=[app_commands.Choice(name=f"{value['username']} #{value['tag']}", value=puuid) for puuid, value in config["accounts"].items()],
    owner=[app_commands.Choice(name=k, value=k) for k in config["players"]]
)
async def changeaccountowner(interaction: discord.Interaction, account: str, owner: str):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["accounts"][account]["owner"] = owner
    save_config(config)
    await interaction.response.send_message("Successfully changed owner", ephemeral=True)

# command to add players
@tree.command(name="addplayer", description="Add a player to listed owners", guilds=GUILD_LIST)
@app_commands.describe(player="Name of player", outputchannel="Channel whose accounts under this player's name outputs to")
async def addplayer(interaction: discord.Interaction, player: str, outputchannel: discord.TextChannel, lpgoal: Optional[int] = 0):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["players"][player] = {
        "lp_goal": lpgoal,
        "taunt_message": { "won": [], "in_session": [], "loss": [] },
        "output_channel_id": outputchannel.id
    }
    save_config(config)
    await interaction.response.send_message(f"Successfully added player {player}", ephemeral=True)

# command to remove player
@tree.command(name="removeplayer", description="Removes a player from owner list, impossible if an account is under this player's name", guilds=GUILD_LIST)
@app_commands.describe(player="Player")
@app_commands.choices(player=[app_commands.Choice(name=k, value=k) for k in config["players"]])
async def changeoutputchannel(interaction: discord.Interaction, player: str):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    accCheck = False
    for k, v in config["accounts"].items():
        if (v["owner"] == player):
            accCheck = True
    if accCheck:
        await interaction.response.send_message("This player has an account, remove the account from tracking first", ephemeral=True)
        return
    config["players"].pop(player)
    save_config(config)
    await interaction.response.send_message(f"Successfully changed output channel of {player}", ephemeral=True)

# command to change lp goal
@tree.command(name="changelpgoal", description="Changes lp goal of a player", guilds=GUILD_LIST)
@app_commands.describe(player="Player", lpgoal="New LP goal")
@app_commands.choices(player=[app_commands.Choice(name=k, value=k) for k in config["players"]])
async def changeoutputchannel(interaction: discord.Interaction, player: str, lpgoal: int):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["players"][player]["lp_goal"] = lpgoal
    save_config(config)
    await interaction.response.send_message(f"Successfully changed LP goal of {player}", ephemeral=True)

# command to change output channel of player
@tree.command(name="changeoutputchannel", description="Changes output channel of a player", guilds=GUILD_LIST)
@app_commands.describe(player="Player", channel="Channel")
@app_commands.choices(player=[app_commands.Choice(name=k, value=k) for k in config["players"]])
async def changeoutputchannel(interaction: discord.Interaction, player: str, channel: discord.TextChannel):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["players"][player]["output_channel_id"] = channel.id
    save_config(config)
    await interaction.response.send_message("Successfully changed output channel", ephemeral=True)

# command to add taunt messages
@tree.command(name="addtauntmessage", description="Adds a taunt message", guilds=GUILD_LIST)
@app_commands.describe(player="Player", category="Category", tauntmessage="New taunt message")
@app_commands.choices(
    player=[app_commands.Choice(name=k, value=k) for k in config["players"]],
    category=[
        app_commands.Choice(name="won", value="won"),
        app_commands.Choice(name="in_session", value="in_session"),
        app_commands.Choice(name="loss", value="loss")
    ]
)
async def addtauntmessage(interaction: discord.Interaction, player: str, category: str, tauntmessage: str):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["players"][player]["taunt_message"][category].append(tauntmessage)
    save_config(config)
    await interaction.response.send_message(f"Successfully added taunt message to {player}", ephemeral=True)

# command to remove taunt messages
@tree.command(name="removetauntmessage", description="Removes a taunt message", guilds=GUILD_LIST)
@app_commands.describe(player="Specified player", category="Specified category", index="Specified index")
@app_commands.choices(
    player=[app_commands.Choice(name=k, value=k) for k in config["players"]],
    category=[app_commands.Choice(name=k, value=k) for k in ["won", "in_session", "loss"]]
)
async def removetauntmessage(interaction: discord.Interaction, player: str, category: str, index: int):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    length = len(config["players"][player]["taunt_message"][category])
    if (index < 0 or index >= length):
        await interaction.response.send_message(f"Index not within range (0 - {length})", ephemeral=True)
        return
    taunt = config["players"][player]["taunt_message"][category].pop(index)
    await interaction.response.send_message(f"Removed taunt message: {taunt}", ephemeral=True)

# command to display all taunt messages
@tree.command(name="displaytauntmessages", description="Displays all taunt messages", guilds=GUILD_LIST)
@app_commands.describe(player="Specified player's taunt messages")
@app_commands.choices(player=[app_commands.Choice(name=k, value=k) for k in config["players"]])
async def displaytauntmessages(interaction: discord.Interaction, player: str):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    responseStr = ""
    for category in config["players"][player]["taunt_message"]:
        responseStr += f"{category.upper()}\n"
        i = 0
        for taunt in config["players"][player]["taunt_message"][category]:
            responseStr += f"`{i}:` {taunt}\n"
            i = i + 1
    await interaction.response.send_message(responseStr, ephemeral=True)

# build image
def buildBingoImg():
    img = Image.new("RGB", (BINGO_SIZE * 5, BINGO_SIZE * 5), color="white")
    img.paste(BINGO_BACKGROUND)
    for y in range(5):
        for x in range(5):
            new = BINGO_IMAGES[config["bingo"][y][x]["imgId"]]
            img.paste(new, (BINGO_SIZE * x + (BINGO_SIZE - new.width) // 2, BINGO_SIZE * y + (BINGO_SIZE - new.height) // 2), mask=new)
            if (config["bingo"][y][x]["cross"]):
                img.paste(BINGO_CROSS, (BINGO_SIZE * x, BINGO_SIZE * y), mask=BINGO_CROSS)
    return img

# command to create a bingo card, for the sake of simplicity, there can only be one active bingo card
@tree.command(name="generatebingo", description="Generates new bingo", guilds=GUILD_LIST)
async def generatebingo(interaction: discord.Interaction):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    rand = random.sample(range(len(BINGO_IMAGES)), 25)
    for y in range(5):
        for x in range(5):
            config["bingo"][y][x]["imgId"] = rand[y * 5 + x]
            config["bingo"][y][x]["cross"] = False
    save_config(config)
    img = buildBingoImg()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    file = discord.File(buffer, filename="throw.png")
    await interaction.response.send_message(file=file)

@tree.command(name="crossbingo", description="Crosses a bingo tile", guilds=GUILD_LIST)
@app_commands.choices(
    row=[app_commands.Choice(name=i+1, value=i) for i in range(5)],
    column=[app_commands.Choice(name=i+1, value=i) for i in range(5)]
)
async def crossbingo(interaction: discord.Interaction, row: int, column: int, cross: bool = True):
    if (interaction.user.id not in [MY_ID, BAOBAO_ID, JUGATU_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
        return
    config["bingo"][row][column]["cross"] = cross
    msg = ""
    if cross:
        checkV = True
        checkH = True
        for i in range(5):
            if not config["bingo"][i][column]["cross"]:
                checkV = False
            if not config["bingo"][row][i]["cross"]:
                checkH = False
        checkD = True
        if row == column:
            for i in range(5):
                if not config["bingo"][i][i]["cross"]:
                    checkD = False
        if max(row, column) - min(row, column) == 4:
            for i in range(5):
                if not config["bingo"][i][4-i]["cross"]:
                    checkD = False
        if checkV or checkH or checkD:
            msg = "JUGATU PUNCH!"
    save_config(config)
    img = buildBingoImg()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    file = discord.File(buffer, filename="throw.png")
    await interaction.response.send_message(msg, file=file)

@tree.command(name="displaybingo", description="Displays the current bingo", guilds=GUILD_LIST)
async def displaybingo(interaction: discord.Interaction):
    img = buildBingoImg()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    file = discord.File(buffer, filename="throw.png")
    await interaction.response.send_message(file=file)

# command to display config contents
@tree.command(name="printconfig", description="Prints config.json", guilds=GUILD_LIST)
async def printconfig(interaction: discord.Interaction):
    if (interaction.user.id not in [MY_ID]):
        await interaction.response.send_message("Unauthorized use of command", ephemeral=True)
    else:
        await interaction.response.send_message(f"Sending config.json", ephemeral=True, file=discord.File("config.json"))

# infrequently update username and tags
@tasks.loop(hours=24)
async def updateAccountDetails():
    for puuid in config["accounts"]:
        res = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}", headers=HEADER)
        if (res.status_code == 200):
            data = res.json()
            if (config["accounts"][puuid]["username"] != data["gameName"] or config["accounts"][puuid]["tag"] != data["tagLine"]):
                config["accounts"][puuid]["username"] = data["gameName"]
                config["accounts"][puuid]["tag"] = data["tagLine"]
                save_config(config)
        else:
            res.raise_for_status()

# Builds embeds with given information
# result is None if game is not finished, otherwise, states whether the player's associated team won or lost
# riotId is simply the riot id, i.e. W31RDCH0MP#smile
# championId is the associated player's champion ID
# time contains the start and end time of the game
# queueId contains the id of the queue type
# postGameData contains various other information like kda, largest crit strike, damage per kill
# teamData contains the elo data of the player's teammates, however, it will be None, if the game is not ranked
# tauntMessage contains a random taunt message from config
def gameEmbedBuilder(result: bool, riotId: str, championId: int, time: dict, queueId: int, postGameData: dict, teamData: list, tauntMessage: str):
    titleStr = "MATCH IN SESSION" if result == None else "MATCH WON" if result else "MATCH LOSS"
    descStr = f"{riotId}"
    if (time["end"] != None):
        descStr += f"\n{secondStringDisplay((time['end']-time['start']))}"
        descStr += f"\n<t:{time['start']}:t> - <t:{time['end']}:t>"
    else:
        descStr += f"\n<t:{time['start']}:t>"
    if (result != None):
        descStr += f"\nKDA: {postGameData['kills']}/{postGameData['deaths']}/{postGameData['assists']}"
        if (postGameData["kills"] > 0):
            descStr += f"\nDPK: {postGameData['totalDamageDealtToChampions'] // postGameData['kills']}"
        else:
            descStr += f"\nDPK: infinity"
        descStr += f"\nLCS: {postGameData['largestCriticalStrike']}"
    descStr += f"\n{QUEUE_ID[queueId]}\n"
    if (queueId == 420): # if the queue is 5v5 ranked
        if (result != None):
            titleStr += f" {postGameData['lpDiff']} LP"
        strLen = [0, 0, 0]
        for t in range(len(teamData)):
            for p in teamData[t]:
                if (p["championId"] == championId):
                    descStr += f"\n{p['tier']} {p['rank']} {p['lp']} LP"
                    strLen[0] = max(strLen[0], len(CHAMPION_ID[str(p["championId"])])+1)
                else:
                    strLen[0] = max(strLen[0], len(CHAMPION_ID[str(p["championId"])]))
                strLen[1] = max(strLen[1], len(str(p["wins"])))
                strLen[2] = max(strLen[2], len(str(p["losses"])))
        descStr += f"```"
        for t in range(len(teamData)):
            descStr += f"\n{'BLUE' if t == 0 else 'RED'}"
            for p in teamData[t]:
                championStr = CHAMPION_ID[str(p["championId"])] + ("*" if p["championId"] == championId else "")
                if (p['tier'] != None):
                    descStr += f"\n{championStr:{strLen[0]}} {p['tier'][0]}{RANK_NUMERICAL[p['rank']]} {p['lp']:>2}LP - {(100 * p['wins']) // (p['wins'] + p['losses'])}% / {p['wins']:>{strLen[1]}}W {p['losses']:>{strLen[2]}}L"
                else:
                    descStr += f"\n{championStr:{strLen[0]}} No Data"
        descStr += f"\n```"
    if (tauntMessage != None):
        descStr += f"{tauntMessage}"
    embed = discord.Embed(
        title=titleStr,
        description=descStr,
        colour=5763719 if result == None else 3447003 if result else 15548997
    )
    embed.set_thumbnail(url=f"{CHAMPION_THUMBNAIL_URL}{CHAMPION_ID[str(championId)]}.png")
    return embed

# periodically checks for players in-game
@tasks.loop(minutes=1)
async def checkplayers():
    async def updateTrackedMessage(puuid):
        owner = config["accounts"][puuid]["owner"]
        res = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/NA1_{config['accounts'][puuid]['match_id']}", headers=HEADER)
        try:
            res.raise_for_status()
            data = res.json()
            player = next((p for p in data["info"]["participants"] if p["puuid"] == puuid), None)
            lpDiff = None
            if (data["info"]["queueId"] == 420):
                teamData = [[], []]
                for p in range(len(data["info"]["participants"])):
                    pDict = data["info"]["participants"][p]
                    team = 0 if pDict["teamId"] == 100 else 1
                    eloRes = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{pDict['puuid']}", headers=HEADER)
                    eloData = next((rank for rank in eloRes.json() if rank["queueType"] == "RANKED_SOLO_5x5"), None)
                    if (eloData != None):
                        teamData[team].append({
                            "championId" : pDict["championId"],
                            "tier"       : eloData["tier"],
                            "rank"       : eloData["rank"],
                            "lp"         : eloData["leaguePoints"],
                            "wins"       : eloData["wins"],
                            "losses"     : eloData["losses"]
                        })
                    else:
                        teamData[team].append({
                            "championId" : pDict["championId"],
                            "tier"       : None,
                            "rank"       : None,
                            "lp"         : None,
                            "wins"       : 0,
                            "losses"     : 0
                        })
                    if (pDict["puuid"] == puuid):
                        newLp = TIER_LP[eloData["tier"]] + RANK_LP[eloData["rank"]] + eloData["leaguePoints"]
                        lpDiff = newLp - config["accounts"][puuid]["lp"]
                        config["accounts"][puuid]["lp"] = newLp
            else:
                teamData = None
            tauntArr = config["players"][owner]["taunt_message"]["won" if player["win"] else "loss"]
            tauntMessage = None
            if (len(tauntArr) > 0):
                tauntMessage = tauntArr[random.randint(0,len(tauntArr)-1)]
            embed = gameEmbedBuilder(
                player["win"], 
                f"{player['riotIdGameName']}#{player['riotIdTagline']}", 
                player["championId"], 
                { "start": data["info"]["gameStartTimestamp"] // 1000, "end": data["info"]["gameEndTimestamp"] // 1000 },
                data["info"]["queueId"],
                { 
                    "lpDiff": lpDiff, 
                    "kills": player["kills"], 
                    "deaths": player["deaths"], 
                    "assists": player["assists"], 
                    "totalDamageDealtToChampions": player["totalDamageDealtToChampions"], 
                    "largestCriticalStrike": player["largestCriticalStrike"] 
                },
                teamData,
                tauntMessage
            )
            msg = await client.get_guild(MEOW_GUILD_ID).get_channel(config["players"][owner]["output_channel_id"]).fetch_message(config["accounts"][puuid]["message_id"])
            await msg.edit(embed=embed)
            
            config["accounts"][puuid]["message_id"] = None
            config["accounts"][puuid]["match_id"] = None
            config["accounts"][puuid]["active"] = False
            save_config(config)
            
        except requests.HTTPError as e:
            print("HTTP ERROR:", e, res.text)

    for puuid in config["accounts"]:
        owner = config["accounts"][puuid]["owner"]
        res = requests.get(f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}", headers=HEADER)
        if (res.status_code == 200):
            data = res.json()
            if (config["accounts"][puuid]["active"] and config["accounts"][puuid]["match_id"] != data["gameId"]):
                await updateTrackedMessage(puuid)
            if (config["accounts"][puuid]["match_id"] == None):
                player = next((p for p in data["participants"] if p["puuid"] == puuid))
                # duplicate code from updateTrackedMessage()
                if (data["gameQueueConfigId"] == 420):
                    teamData = [[], []]
                    for p in range(len(data["participants"])):
                        pDict = data["participants"][p]
                        team = 0 if pDict["teamId"] == 100 else 1
                        eloRes = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{pDict['puuid']}", headers=HEADER)
                        eloData = next((rank for rank in eloRes.json() if rank["queueType"] == "RANKED_SOLO_5x5"), None)
                        if (eloData != None):
                            teamData[team].append({
                                "championId" : pDict["championId"],
                                "tier"       : eloData["tier"],
                                "rank"       : eloData["rank"],
                                "lp"         : eloData["leaguePoints"],
                                "wins"       : eloData["wins"],
                                "losses"     : eloData["losses"]
                            })
                        else:
                            teamData[team].append({
                                "championId" : pDict["championId"],
                                "tier"       : None,
                                "rank"       : None,
                                "lp"         : None,
                                "wins"       : 0,
                                "losses"     : 0
                            })
                else:
                    teamData = None
                # end of duplicate code
                tauntArr = config["players"][owner]["taunt_message"]["in_session"]
                tauntMessage = None
                if (len(tauntArr) > 0):
                    tauntMessage = f"\n{tauntArr[random.randint(0,len(tauntArr)-1)]}"
                embed = gameEmbedBuilder(
                    None, 
                    player["riotId"], 
                    player["championId"], 
                    { "start": data["gameStartTime"] // 1000, "end": None },
                    data["gameQueueConfigId"],
                    None,
                    teamData,
                    tauntMessage
                )
                msg = await client.get_guild(MEOW_GUILD_ID).get_channel(config["players"][owner]["output_channel_id"]).send(embed=embed)
                
                config["accounts"][puuid]["message_id"] = msg.id
                config["accounts"][puuid]["match_id"] = data["gameId"]
                config["accounts"][puuid]["active"] = True
                save_config(config)
        # update tracked message if there is no active game and tracked message exists
        elif (res.status_code == 404):
            if (config["accounts"][puuid]["active"]):
                await updateTrackedMessage(puuid)
        else:
            res.raise_for_status()

# unnecessary copypasta command
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
    await checkplayers()
    checkplayers.start()
    updateAccountDetails.start()
    for g in client.guilds:
        await tree.sync(guild=g)
    print(f"Logged in as {client.user}")

# keep_alive()
client.run(BOT_TOKEN)
