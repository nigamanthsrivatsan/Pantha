import discord
from discord.ext import commands, tasks
import asyncio
import random
from random import choice
import os
import dbl
import aiosqlite
from discord_components import *


class Utilities(commands.Cog):
    '''
    Server Utilities and User Utilities
    '''
    def __init__(self, panther):
        self.panther = panther
        self.topToken = self.panther.config["toptoken"]
        self.dblpy = dbl.DBLClient(self.panther, self.topToken)
        self.sniped = {}
        self.sniped_author = None


    @commands.Cog.listener()
    async def on_ready(self):
        await self.panther.put_status(f"Playing in {len(self.panther.guilds)} servers with {len(self.panther.users)} users!")

    
    @commands.command()
    async def poll(self, ctx, *, args : str):
        '''
        A basic but effective poll command, identical to carl's command
        Deletes your message and quickly starts a poll
        '''
        await ctx.message.delete()
        m = await ctx.send(f'**{ctx.author.name}#{ctx.author.discriminator}** asks: {args}')
        await m.add_reaction('👍')
        await m.add_reaction('👎')

    def convert(self, time):
        pos = ["s","m","h","d"]

        time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]
    
    def get_readable(self, time):
        pos = ["s","m","h","d"]

        time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}
        readable_dict = {"s" : "seconds", "m" : "minutes", "h" : "hours", "d" : "days"}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return f"{val} {readable_dict[unit]}"
        
    @commands.command()
    async def choose(self, ctx, *choices : str):
        '''For when you want to set the score through a random bot :sweat_smile:'''
        await ctx.send(content = random.choice(choices), allowed_mentions = discord.AllowedMentions(everyone = False, users = True, roles = False, replied_user = True))
    
    @commands.command()
    async def line(self, ctx, *choices : str):
        '''Gives a kool line to create another message overlay!'''
        await ctx.message.delete()
        await ctx.send(embed = discord.Embed().set_image(url  ='https://images-ext-2.discordapp.net/external/rqqwXPOsPeEo2mWg1M2WERWb-zcH-Xo7Tll_NsKl2CM/https/media.discordapp.net/attachments/856872035762438144/859149396519813150/rgbline.gif'))
    
    @commands.command()
    @commands.has_permissions(manage_messages = True, kick_members = True)
    async def embed(self, ctx, *, content):
        """Create an interactive embed!"""
        try:
            title, desc = content.split("|")
        except:
            await ctx.send("Type an embed in this format: `p.embed {title} | {description}`")
            return
        else:
            await ctx.message.delete()
            em = discord.Embed(title = title, color = ctx.author.color, description= desc)
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            em.set_image(url = 'https://images-ext-2.discordapp.net/external/rqqwXPOsPeEo2mWg1M2WERWb-zcH-Xo7Tll_NsKl2CM/https/media.discordapp.net/attachments/856872035762438144/859149396519813150/rgbline.gif')
            await ctx.send(embed = em)
    
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def coinflip(self, ctx):
        em = discord.Embed(title = "👛 Coinflip", color = ctx.author.color)
        choices = ["Heads", "Tails"]
        em.add_field(name = "Roll:", value = f"`{choice(choices)}` :coin:")
        return await ctx.send(embed = em)

def setup(panther):
    '''
    Sets up the cog by adding it to the bot
    '''
    panther.add_cog(Utilities(panther))