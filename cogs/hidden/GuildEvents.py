import discord
from discord.ext import commands

class GuildEvents(commands.Cog):
    def __init__(self, sirius):
        self.sirius = sirius
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.member_count < 50:
            await guild.owner.send(f"Your server has {guild.member_count} members whereas the minimum to invite Pantha is 50 members!")
            await guild.leave()
            return
        embed = discord.Embed(title = f"୨୧︰Joined Server {str(guild.name)}", color = discord.Color.from_rgb(0, 255, 4))
        embed.description = f"<:pinkarrow:912294860495663134> <:ownercrown:908672648526037002> **Owner:** {guild.owner.name}#{guild.owner.discriminator} (`{guild.owner.id}`)\n<:pinkarrow:912294860495663134> **Member Count:** `{guild.member_count}`\n<:pinkarrow:912294860495663134> **Name:** {guild.name}\n<:pinkarrow:912294860495663134> Guild ID: `{guild.id}`"

        sguild = self.sirius.get_guild(857875406317551617)
        for channel in sguild.channels:
            if channel.id == 912293245692821514:
                await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title = f"୨୧︰Left Server {str(guild.name)}", color = discord.Color.from_rgb(255,8,0))
        embed.description = f"<:pinkarrow:912294860495663134> <:ownercrown:908672648526037002> **Owner:** {guild.owner.name}#{guild.owner.discriminator} (`{guild.owner.id}`)\n<:pinkarrow:912294860495663134> **Member Count:** `{guild.member_count}`\n<:pinkarrow:912294860495663134> **Name:** {guild.name}\n<:pinkarrow:912294860495663134> Guild ID: `{guild.id}`"

        sguild = self.sirius.get_guild(857875406317551617)
        for channel in sguild.channels:
            if channel.id == 912293246485528616:
                await channel.send(embed = embed)

    
    

def setup(sirius):
    sirius.add_cog(GuildEvents(sirius))