import discord
from discord.ext import commands
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
from helpers.slash_util import *
from helpers import slash_util


class Misc(commands.Cog, name = "Miscellaneous"):
    """Miscellaneous commands uncategorized into any cog"""
    def __init__(self, panther):
        self.panther = panther

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        """
        Suggest something to the devs!
        """
        await ctx.send(':warning: Troll suggestions will get you and your server (if you own any) banned (with warnings of course)\n<a:heart_anim:911579838811353098> Your suggestion has been sent to the devs')
        owner = await self.panther.fetch_user(819395560837742643)
        await owner.send(f'<a:heart_anim:911579838811353098> **A new suggestion**\n\n<:bullet:911962148828225536> **Suggestion:** {suggestion}\n<:bullet:911962148828225536> **Author:** {ctx.author.name}#{ctx.author.discriminator} (`{ctx.author.id}`)')


def setup(panther):
    panther.add_cog(Misc(panther))
    