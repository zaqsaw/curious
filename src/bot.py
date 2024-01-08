import os
from random import choice
from itertools import cycle
import datetime, time

import discord
from discord.ext import commands, tasks

token = os.getenv('DISCORD_TOKEN')

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
          bot_status = cycle(f.readlines())
          await client.change_presence(activity=discord.Watching(next(name = bot_status)))
          

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
     await ctx.send("{0}ms. %s " % uptime .format(round(client.latency * 100)))

@client.listen('on_message') #if "curious" in chat, send "curious"
async def curious(message):
     if message.author == client.user:
        return
     if "curious" in message.content:
          await message.channel.send("curious")


     

client.run(token)

