
from ast import Del
import time

import discord
from discord.ext import commands, tasks 
from discord.ui import Button, View
from Kahoot import client

client = client.client()


class KahootCog(commands.Cog, name="Kahoot"):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @tasks.loop(seconds=1)
    async def PlayerCheckLoop(self, ctx):
            self.n_player = client.checkPlayerJoin()
            if self.n_player != self.l_player:
                    await ctx.send(f'Player joined! **{self.n_player.text}**')
                    self.startBtn.disabled = False
                    await self.UpdateView()
            self.l_player = self.n_player

    async def UpdateView(self):
            self.view.clear_items()
            self.view.add_item(self.startBtn)
            self.view.add_item(self.stopBtn)
            await self.status.edit(view=self.view)



    @commands.command(name="Kahoot",
                    usage="",
                    description="Initiate a new kahoot game")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def initiate(self, ctx):

            self.startBtn = Button(label='Start', style=discord.ButtonStyle.green, emoji="✔", disabled=True)
            self.stopBtn = Button(
                label='StopGame', style=discord.ButtonStyle.green, emoji="✔", disabled=False)
            self.view = View()


            self.embed = discord.Embed(title=f"Status", color=0xFF00BB)
            self.embed.add_field(name="Init", value='❌', inline=True)
            self.embed.add_field(name="pin", value='❌', inline=True)
            self.embed.add_field(name="ready", value='❌', inline=True)
            self.embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            self.status = await ctx.send(embed=self.embed)
            await self.UpdateView()
            client.Initiate(
                'https://play.kahoot.it/v2/?quizId=ff83588e-ccb6-498b-9986-3433a29c4dea')
            self.embed.set_field_at(index=0, name='Init', value='✅')
            await self.status.edit(embed=self.embed)
            client.fetchInfo()
            self.embed.set_field_at(index=0, name='Ready', value='✅')
            self.embed.add_field(name="Players", value='None', inline=True)

            self.embed.add_field(name = 'link', value=client.link, inline=False)
            file = discord.File("Assets\PIN.png", filename="PIN.png")
            self.embed.set_image(
                url="attachment://PIN.png")
            await self.status.edit(file=file, embed=self.embed)
            #Now ready
            await self.status.edit(embed=self.embed, view=self.view)
            
            self.l_player = 0
            self.PlayerCheckLoop.start(ctx)




    async def Start(self, ctx):
        await ctx.send('Starting Game...')
        self.PlayerCheckLoop.cancel()
        client.startGame()
        client.getQuestion()
        await ctx.send(file=discord.File('.\Assets\Question.png'))
        await ctx.send(client.question)




def setup(bot:commands.Bot):    
    bot.add_cog(KahootCog(bot))
