import logging
from argparse import ArgumentParser
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext import tasks

from .cfg import Config
from .cmds import Commands
from .logger import get_logger
from .logger import setup_logger


logger = get_logger()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="location of the config file",
    )
    parser.add_argument(
        "--logdir",
        default="/tmp",
        type=Path,
        help="location of the config file",
    )
    args = parser.parse_args()

    cfg = Config(args.config)
    handler = setup_logger(args.logdir)

    intents = discord.Intents.all()
    client = commands.Bot(command_prefix='.', intents=intents)
    cmds = Commands(cfg, client)

    @client.event
    async def on_ready():
        await cmds.on_startup()
    
    @client.command()
    async def list(ctx):
        await cmds.list(ctx)
    
    @client.command()
    async def show(ctx, *words):
        phrase = ' '.join(words)
        phrase = phrase.lower()
        await cmds.show(ctx, phrase)

    @client.command()
    async def save(ctx, *words):
        phrase = ' '.join(words)
        phrase = phrase.lower()
        await cmds.save(ctx, phrase)

    @client.command(aliases=["genz","slang","hoodspeak"])
    async def cap(ctx):
        await cmds.cap(ctx)

    @client.command()
    async def steal(ctx, emoji: discord.PartialEmoji):
        await cmds.steal(ctx, emoji: discord.PartialEmoji)
    
    @client.command(aliases=["ms","latency"]) #ping latency cmd
    async def ping(ctx):
        await cmds.ping(ctx)

    client.run(cfg.token, log_handler=handler, log_level=logging.INFO)
