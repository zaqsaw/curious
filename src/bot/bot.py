import datetime
import os
import time
import logging
from argparse import ArgumentParser
from pathlib import Path
from random import choice
from itertools import cycle

import discord
from discord.ext import commands
from discord.ext import tasks

from .cfg import Config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if Path('curious.log').is_file():
    os.rename('curious.log', f'curious_{ datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") }.log')
handler = logging.FileHandler(filename='curious.log', encoding='utf-8', mode='w')
logger.addHandler(handler)
intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    bot_status = choice(cfg.ious)
    logger.info(f'changing status {bot_status}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f'you. | { bot_status }'))
    global startTime
    startTime = time.time()

@client.command()
async def list(ctx):
    logger.info('list called by: %s', ctx.author)
    show_map = await cfg.load_show_map()
    await ctx.send(', '.join(show_map.keys()), ephemeral=True)

@client.command()
async def show(ctx, *words):
    phrase = ' '.join(words)
    phrase = phrase.lower()
    logger.info('show %s called by: %s', phrase, ctx.author)
    show_map = await cfg.load_show_map()
    if phrase in show_map:
        await ctx.send(show_map[phrase])
    else:
        await ctx.send(f'{ phrase } not known')

@client.command()
async def save(ctx, *words):
    phrase = ' '.join(words)
    phrase = phrase.lower()
    logger.info('save %s called by: %s', phrase, ctx.author)
    attachments = ctx.message.attachments
    reference = ctx.message.reference
    if reference and len(attachments) == 0:
        ref_message = await ctx.fetch_message(reference.message_id)
        attachments = ref_message.attachments
    if phrase and len(attachments) == 1:
        attachment = attachments[0]
        url = attachment.url
        show_map = await cfg.load_show_map()
        if phrase in show_map and ctx.author == "zalles":
            await ctx.send("suck it zalles")
            return
        await cfg.save_to_show_map(phrase, url, show_map)
        await ctx.send(f"saved { phrase }!")
    else:
        await ctx.send('".save phrase" requires a phrase and one attachment')

@client.command(aliases=["genz","slang","hoodspeak"])
async def cap(ctx):
    logger.info(f'cap called by: { ctx.author }')
    await ctx.send(choice(cfg.genz))

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

    cfg = Config(args.config)
    client.run(cfg.token, log_handler=handler, log_level=logging.INFO)
