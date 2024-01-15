import datetime
import os
import time
import logging
import yaml
from argparse import ArgumentParser
from pathlib import Path
from random import choice
from itertools import cycle

import discord
from discord.ext import commands
from discord.ext import tasks


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='curious.log', encoding='utf-8', mode='w')
logger.addHandler(handler)
intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    bot_status = choice(ious)
    logger.info(f'changing status {bot_status}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f'you. | { bot_status }'))
    global startTime
    startTime = time.time()

@client.command(aliases=["gook","chink","asian"]) # reo was here :D
async def goon(ctx):
    logger.info(f'goon called by: { ctx.author }')
    await ctx.send("https://cdn.discordapp.com/attachments/1036455284874432515/1193332807674646578/c6d96599ceda4988b99b2d9fb75a64b6.mov?ex=65ac54c8&is=6599dfc8&hm=afe9862cd5311b9302254f92a8dca17fefb9f880c97e8b96777cec74bdbc0008&")

@client.command()
async def show(ctx):
    logger.info(f'show called by: { ctx.author }')

@client.command()
async def save(ctx):
    logger.info(f'save called by: { ctx.author }')

@client.command(aliases=["genz","slang","hoodspeak"])
async def cap(ctx):
    logger.info(f'cap called by: { ctx.author }')
    await ctx.send(choice(genz))

@client.command(aliases=["ms","latency"]) #ping latency cmd
async def ping(ctx):
    logger.info(f'ping called by: { ctx.author }')
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    await ctx.send("{0}ms, uptime %s." % uptime .format(round(client.latency * 100)))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="location of the config file",
    )
    args = parser.parse_args()

    with open(args.config / "token.yml", "r") as file:
        token = yaml.safe_load(file)["token"]
    with open(args.config / "genz.yml", "r") as file:
        genz = yaml.safe_load(file)["quotes"]
    with open(args.config / "ious.yml", "r") as file:
        ious = yaml.safe_load(file)["statuses"]

    client.run(token, log_handler=handler, log_level=logging.INFO)
