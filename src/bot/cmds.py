import datetime
import os
import time
from random import choice

from .logger import get_logger

logger = get_logger()


class Commands:
    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client
        self.startTime = time.time()

    async def on_startup(self):
        logger.info(f"{self.client.user} has connected to Discord!")
        self.update_status()

    def validate(self, cmd, ctx):
        logger.info("%s called by: %s", cmd, ctx.author)

    async def update_status(self):
        bot_status = choice(cfg.ious)
        logger.info(f"changing status {bot_status}")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f"you | { bot_status }"))

    async def list(self, ctx):
        self.validate("list", ctx)
        show_map = await cfg.load_show_map()
        await ctx.send(", ".join(show_map.keys()), ephemeral=True)

    async def show(self, ctx, phrase):
        self.validate(f"show { phrase }", ctx)
        show_map = await cfg.load_show_map()
        if phrase in show_map:
            await ctx.send(show_map[phrase])
        else:
            await ctx.send(f"{ phrase } not known")

    async def is_zalles_overwriting(self, phrase, show_map, author):
        if phrase in show_map and author == "zalles":
            await ctx.send("suck it zalles")
            return True
        return False

    async def save(self, ctx, phrase):
        self.validate(f"save { phrase }", ctx)
        attachments = ctx.message.attachments
        reference = ctx.message.reference
        if reference and len(attachments) == 0:
            ref_message = await ctx.fetch_message(reference.message_id)
            attachments = ref_message.attachments

        if phrase and len(attachments) == 1:
            attachment = attachments[0]
            url = attachment.url
            show_map = await cfg.load_show_map()
            if not await self.is_zalles_overwriting(phrase, show_map, ctx.author):
                await cfg.save_to_show_map(phrase, url, show_map)
                await ctx.send(f"saved { phrase }!")
        else:
            await ctx.send('".save phrase" requires a phrase and one attachment')

    async def cap(self, ctx):
        self.validate("cap", ctx)
        await ctx.send(choice(cfg.genz))

    async def ping(self, ctx):
        self.validate("ping", ctx)
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - self.startTime))))
        latency = round(self.client.latency * 100)
        await ctx.send(f"{ latency }ms, uptime { uptime }.")
