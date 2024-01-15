import datetime
import os
import time
import yaml
from argparse import ArgumentParser
from pathlib import Path
from random import choice
from itertools import cycle

import discord
from discord.ext import commands
from discord.ext import tasks


intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    global startTime
    startTime = time.time()

@tasks.loop(seconds=60) #status, check ious.txt
async def change_status():
     with open("ious.txt", "r") as f:
          bot_status = choice(f.readlines())
          await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = bot_status))
          

@client.command(aliases=["gook","chink","asian"]) # reo was here :D
async def goon(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1036455284874432515/1193332807674646578/c6d96599ceda4988b99b2d9fb75a64b6.mov?ex=65ac54c8&is=6599dfc8&hm=afe9862cd5311b9302254f92a8dca17fefb9f880c97e8b96777cec74bdbc0008&")

@client.command(aliases=["genz","slang","hoodspeak"])
async def cap(ctx):
        print(f'called by: { ctx.author }')
        with open('genz_quotes.txt', 'r') as f:
            lines = list(f.readlines())
        await ctx.send(choice(lines))

@client.command(aliases=["ms","latency"]) #ping latency cmd
async def ping(self, ctx):
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

    client.run(token)
