
from ast import Del
import time

import discord
from discord.ext import commands, tasks 

from Kahoot import client

client = client.client()


class KahootCog(commands.Cog, name="Kahoot"):
    def __init__(self, bot: commands.bot):
        self.bot = bot




    async def getStatus(self, FG='❌', PL='❌', GP='❌', WP='❌'):
            embed = discord.Embed(title=f"Status", color=0x431b93)
            embed.add_field(name="SessionInitialised", value=FG, inline=False)
            embed.add_field(name="GameLoaded", value=PL, inline=False)
            embed.add_field(name="GeneratedPin", value=GP, inline=False)
            embed.add_field(name="WaitingForPlayers", value=WP, inline=False)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            return embed


    @tasks.loop(seconds=1)
    async def PlayerCheckLoop(self, ctx):
            self.n_player = client.checkPlayerJoin()
            if self.n_player != self.l_player:
                    await ctx.send(f'Player joined! **{self.n_player.text}**')
            self.l_player = self.n_player




    @commands.command(name="Kahoot",
                    usage="",
                    description="Initiate a new kahoot game")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def initiate(self, ctx):
            self.embed = await self.getStatus('✅')
            print(client.driver)
            
            self.status = await ctx.send(embed=self.embed)
            client.Initiate(
                'https://play.kahoot.it/v2/?quizId=ff83588e-ccb6-498b-9986-3433a29c4dea')
            await self.status.edit(embed=await self.getStatus('✅', '✅'))
            client.fetchInfo()
            await self.status.edit(embed=await self.getStatus('✅', '✅', '✅'))
            self.embed.set_footer(
                 text=client.link)
            await self.status.edit(embed=await self.getStatus('✅', '✅', '✅', '✅'))
            self.embed = await self.getStatus('✅', '✅', '✅', '✅')
            file = discord.File("Assets\PIN.png", filename="PIN.png")
            self.embed.set_image(
                url="attachment://PIN.png")
            await self.status.edit(file=file, embed=self.embed)
            self.l_player = 0
            self.PlayerCheckLoop.start(ctx)




    @commands.command(name='Start',
                          usage="",
                          description="Skip player queue")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def Start(self, ctx):
        await ctx.send('Starting Game...')
        self.PlayerCheckLoop.cancel()
        client.startGame()
        client.getQuestion()
        await ctx.send(file=discord.File('.\Assets\Question.png'))
        await ctx.send(client.question)




def setup(bot:commands.Bot):    
    bot.add_cog(KahootCog(bot))
