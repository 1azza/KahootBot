import discord
from discord.ext import commands
from scripts.utils.configHandle import config, bot
import cv2
import numpy as np
import re
import requests
from discord.commands import slash_command, user_command
from discord.commands import Option
class spung_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.PATH = 'profilepicture.png'


    async def dlAvatar(self, ctx, user):
        user = await bot.fetch_user(user)
        print('Spunging:', user, '...')
        url = user.display_avatar.url
        img_data = requests.get(url).content
        with open(self.PATH, 'wb') as handler:
            handler.write(img_data)
        self.IMG = cv2.imread(self.PATH)
        await self.main_spung(ctx)
        print('Done!')

    async def main_spung(self, ctx):
        imgCanny =  cv2.Canny(self.IMG, 100, 100)
        cv2.imwrite(self.PATH, imgCanny)
        await ctx.respond(file=discord.File(self.PATH))

    @slash_command(guild_ids=config.GUILDS, description="Spung another user")
    async def spung(self, ctx, arg):
            user = re.sub("[^0-9]", "", arg)
            await self.dlAvatar(ctx, user)



    @slash_command(guild_ids=config.GUILDS, description="Spung any image")
    async def spunk(self, ctx):
        def check(message):
            return message.author == ctx.author and bool(message.attachments)
        await ctx.respond('**Waiting for an attachment...**')
        resp = await bot.wait_for('message', check=check)
        image = resp.attachments[0]
        await image.save(fp=self.PATH)
        self.IMG = cv2.imread(self.PATH)
        await self.main_spung(ctx)



def setup(bot):
    bot.add_cog(spung_commands(bot))
