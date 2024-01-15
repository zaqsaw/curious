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

def load_show_map():
    global show_file
    global show_map
    show_map = {}
    if show_file.is_file():
        with open(show_file, "r") as file:
            loaded = yaml.safe_load(file)
        if loaded:
            show_map = loaded
    return show_map

def save_to_show_map(key, value):
    global show_file
    logger.info("saving to %s %s: %s", show_file, key, value)
    show_map = load_show_map()
    show_map[key] = value
    with open(show_file, "w") as file:
        yaml.dump(show_map, file)

@client.command()
async def show(ctx, *words):
    phrase = ' '.join(words)
    logger.info('show %s called by: %s', phrase, ctx.author)
    show_map = load_show_map()
    if phrase in show_map:
        await ctx.send(show_map[phrase])

@client.command()
async def save(ctx, *words):
    phrase = ' '.join(words)
    logger.info('save %s called by: %s', phrase, ctx.author)
    attachments = ctx.message.attachments
    if phrase and len(attachments) == 1:
        attachment = attachments[0]
        url = attachment.url
        save_to_show_map(phrase, url)
        await ctx.send(f"saved { phrase }!")
    else:
        await ctx.send('".save phrase" requires a phrase and one attachment')

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
    show_file = args.config / "show.yml"

    client.run(token, log_handler=handler, log_level=logging.INFO)
