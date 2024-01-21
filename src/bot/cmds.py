import datetime
import os
import time
from random import choice

import discord

from .logger import get_logger


logger = get_logger()


private_id = 1171626913501036564
whitelist_roles = [
    "bishops",
    "ministers",
    "deacons",
]
blacklist_users = []

class Commands:
    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client
        self.startTime = time.time()

    async def on_startup(self):
        logger.info(f"{self.client.user} has connected to Discord!")
        await self.update_status()

    def has_whitelist_role(self, roles):
        for role in roles:
            if role.name in whitelist_roles:
                return True
        return False

    def validate(self, cmd, ctx):
        logger.info("%s called by %s in %s", cmd, ctx.author, ctx.guild)
        if ctx.guild.id == private_id and not self.has_whitelist_role(ctx.author.roles):
            logger.info("INVALID: User %s did not have whitelist roles", ctx.author)
            return False
        return True

    async def update_status(self):
        bot_status = choice(self.cfg.ious)
        logger.info(f"changing status {bot_status}")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f"you | { bot_status }"))

    async def list(self, ctx):
        if not self.validate("list", ctx):
            return
        show_map = await self.cfg.load_show_map()
        await ctx.send(", ".join(show_map.keys()), ephemeral=True)

    async def show(self, ctx, phrase):
        if not self.validate(f"show { phrase }", ctx):
            return
        show_map = await self.cfg.load_show_map()
        if phrase in show_map:
            await ctx.send(show_map[phrase])
        else:
            await ctx.send(f"{ phrase } not known")

    async def is_zalles_overwriting(self, phrase, show_map, author):
        if phrase in show_map and author.id == 180807596670713856:
            await ctx.send("suck it zalles")
            return True
        return False

    async def save(self, ctx, phrase):
        if not self.validate(f"save { phrase }", ctx):
            return
        attachments = ctx.message.attachments
        reference = ctx.message.reference
        if reference and len(attachments) == 0:
            ref_message = await ctx.fetch_message(reference.message_id)
            attachments = ref_message.attachments

        if phrase and len(attachments) == 1:
            attachment = attachments[0]
            url = attachment.url
            show_map = await self.cfg.load_show_map()
            if not await self.is_zalles_overwriting(phrase, show_map, ctx.author):
                await self.cfg.save_to_show_map(phrase, url, show_map)
                await ctx.send(f"saved { phrase }!")
        else:
            await ctx.send('".save phrase" requires a phrase and one attachment')

    async def cap(self, ctx):
        if not self.validate("cap", ctx):
            return
        await ctx.send(choice(self.cfg.genz))

    async def ping(self, ctx):
        if not self.validate("ping", ctx):
            return
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - self.startTime))))
        latency = round(self.client.latency * 100)
        await ctx.send(f"{ latency }ms, uptime { uptime }")
