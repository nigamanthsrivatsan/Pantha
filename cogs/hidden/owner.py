import discord
from discord.ext import commands
import DiscordUtils
import os
from discord_components import *

class Owner(commands.Cog):
    def __init__(self, panther):
        self.panther = panther
        self.ownerIds = [819395560837742643]
        self.patched = None
        self.patchId = 921696055630913566
        self.msg = None
    
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, extension):
        '''
        Loads a cog, some are loaded by default
        '''
        try:
            self.panther.load_extension(f'{extension}')
            await ctx.send(f'<:verified_bot:897416027007250442> Loaded `{extension}`, to unload this cog please type: `p.unload {extension}`')  
        except:
            await ctx.send(f':x: Failed to load `{extension}`, perhaps it is already loaded or doesn\'t exist at all!')
        
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, extension):
        '''
        Unloads a cog, some are loaded by default
        '''
        try:
            self.panther.unload_extension(f'{extension}')
            await ctx.send(f'<:verified_bot:897416027007250442> Unloaded `{extension}`, to load this cog please type: `p.load {extension}`')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send("Cog is already loaded")
        except commands.ExtensionNotFound:
            await ctx.send("Cog not found")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension):
        '''
        Reloads a cog
        '''
        try:
            self.panther.unload_extension(f'{extension}')
            self.panther.load_extension(f'{extension}')
            await ctx.send(f'<:verified_bot:897416027007250442> Reloaded `{extension}`')
        except:
            await ctx.send(f':x: Failed to unload `{extension}`, perhaps it is already unloaded or doesn\'t exist at all!')
    
    @commands.command()
    @commands.is_owner()
    async def listcogs(self, ctx):
        msg = '```diff\n'
        for i in os.listdir('./cogs'):
            if i.endswith('.py'):
                msg += f'+ {i[:-3]}\n'
        msg += '```'
        await ctx.send(msg)
        
    @commands.command()
    @commands.is_owner()
    async def cleartickets(self, ctx):
        counter = 0
        for channel in ctx.guild.channels:
            if "closed" in channel.name:
                await channel.delete(reason = 'Closed ticket') 
                counter += 1
        
        await ctx.send(f'Successfully deleted **{counter}** tickets')
        
    @commands.command()
    @commands.is_owner()
    async def osay(self, ctx, *, say):
        await ctx.message.delete()
        await ctx.channel.send(say)
    
    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        '''
        Enables/disables a command
        '''
        command = self.panther.get_command(command)

        if command is None:
            embed = discord.Embed(title="ERROR", description="I can't find a command with that name!", color=0xff0000)
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = discord.Embed(title="ERROR", description="You cannot disable this command.", color=0xff0000)
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = discord.Embed(title="Toggle", description=f"I have {ternary} {command.qualified_name} for you!", color=0xff00c8)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def panel(self, ctx):
        '''
        Creates a role panel with buttons
        '''
        if ctx.guild.id != 854238372464820224:
            return await ctx.send('This is only accessible in **The Jedi** that too only by Not Imp, and the admins!')
        
        if not ctx.author.guild_permissions.administrator:
             return await ctx.send('This is only accessible in **The Jedi** that too only by Not Imp, and the admins!')

        heists = 854279021801504778
        pheist = 854279724788219925
        gws = 854279061948989440
        unf = 860076204271075348
        events = 854279132346056704
        ngw = 866919110936231957
        cr = 855720035426631690
        prtnr = 854280253027516426


        body = f"<:tj_pandaheist:919577287760965642> <:tj_dot:872445988760068106> <@&{heists}>\n<:tj_PandaSip:908549399276306442> <:tj_dot:872445988760068106> <@&{pheist}>\n<:tj_PandaSwag:906348241883389972> <:tj_dot:872445988760068106> <@&{gws}>\n<a:tj_heist:854558527347359774> <:tj_dot:872445988760068106> <@&{unf}>\n<a:tj_duccvibing:863033429057601547> <:tj_dot:872445988760068106> <@&{events}>\n<:tj_nitro_classic_badge:877546642692259841> <:tj_dot:872445988760068106> <@&{ngw}>\n<:tj_chatrevive:910030249503358978> <:tj_dot:872445988760068106> <@&{cr}>\n<:tj_partner:867224237458587679> <:tj_dot:872445988760068106> <@&{prtnr}>"
        
        embed = discord.Embed(title = "<a:stars_anim:914434879670857768> Take some self roles!", color = discord.Color.from_rgb(0, 255, 187))
        embed.description = body

        async def gheist(interaction):
            r = ctx.guild.get_role(heists)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == heists:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{heists}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{heists}> role from you")
        
        async def ggaw(interaction):
            r = ctx.guild.get_role(gws)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == gws:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{gws}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{gws}> role from you")
        
        async def gpheist(interaction):
            r = ctx.guild.get_role(pheist)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == pheist:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{pheist}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{pheist}> role from you")
            
        async def gunf(interaction):
            r = ctx.guild.get_role(unf)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == unf:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{unf}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{unf}> role from you")

        async def gev(interaction):
            r = ctx.guild.get_role(events)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == events:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{events}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{events}> role from you")

        async def gng(interaction):
            r = ctx.guild.get_role(ngw)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == ngw:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{ngw}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{ngw}> role from you")
        
        async def gcr(interaction):
            r = ctx.guild.get_role(cr)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == cr:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{cr}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{cr}> role from you")
        
        async def gprtnr(interaction):
            r = ctx.guild.get_role(prtnr)
            hasRole = False
            for role in interaction.user.roles:
                if role.id == prtnr:
                    hasRole = True
            if not hasRole:
                await interaction.user.add_roles(r)
                await interaction.send(f"・added the <@&{prtnr}> role to you")
            else:
                await interaction.user.remove_roles(r)
                await interaction.send(f"・removed the <@&{prtnr}> role from you")

        await ctx.send(
            embed = embed,
            components = [
                [
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.green, emoji = self.panther.get_emoji(919577287760965642)), gheist
                    ),
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.red, emoji = self.panther.get_emoji(908549399276306442)), gpheist
                    ),
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.green, emoji = self.panther.get_emoji(906348241883389972)), ggaw
                    ),
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.red, emoji = self.panther.get_emoji(854558527347359774)), gunf
                    ),
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.green, emoji = self.panther.get_emoji(863033429057601547)), gev
                    )
                ],
                [
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.red, emoji = self.panther.get_emoji(877546642692259841)), gng
                    ),
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.green, emoji = self.panther.get_emoji(910030249503358978)), gcr
                    ),
                    self.panther.components_manager.        add_callback(
                        Button(style=ButtonStyle.red, emoji = self.panther.get_emoji(867224237458587679)), gprtnr
                    )
                ]
            ]
        )
    
    @commands.group(invoke_without_command = True)
    async def patch(self, ctx):
        '''
        Starts a new patch note
        '''
        if ctx.author.id not in self.ownerIds:
            return await ctx.send('Restricted access!')
        
        self.patched = discord.Embed(title = 'New Patch', color = discord.Color.random())
        self.patched.set_thumbnail(url = ctx.author.avatar_url)
        self.msg = "```diff\n"
        await ctx.send('Patch created!')
    
    @patch.command()
    async def add(self,ctx, *, message):
        '''
        Adds a new message to the patch note
        '''
        self.msg += f"{message}\n"
        await ctx.send('Added the message!')
    
    @patch.command()
    async def post(self, ctx):
        '''
        Posts the patch
        '''
        self.msg += '\n```'
        self.patched.description = self.msg
        channel = self.panther.get_channel(self.patchId)
        await channel.send(embed = self.patched)
        await ctx.send(f"Posted the patch in {channel.mention}")


def setup(panther):
    '''
    Sets up the cog by adding it to the bot
    '''
    panther.add_cog(Owner(panther))
