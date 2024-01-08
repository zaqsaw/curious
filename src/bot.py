import os
from random import choice

import discord
from discord.ext import commands, tasks

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def goon(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1036455284874432515/1193332807674646578/c6d96599ceda4988b99b2d9fb75a64b6.mov?ex=65ac54c8&is=6599dfc8&hm=afe9862cd5311b9302254f92a8dca17fefb9f880c97e8b96777cec74bdbc0008&")

@client.command()
async def cap(ctx):
        print(f'called by: { ctx.author }')
        with open('genz_quotes.txt', 'r') as f:
            lines = list(f.readlines())
        await ctx.send(choice(lines))

client.run(token)

