import discord
import re
import asyncio

from discord.ext import commands
from helpers import permissions
from helpers import default

owners = [819395560837742643, 682527772610265098]

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f"reason is too long ({len(argument)}/{reason_max})")
        return ret

class Moderation(commands.Cog):
    '''
    The right set of moderation tools for any discord-community!
    '''
    def __init__(self, panther):
        self.panther = panther

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation commands are loaded, bam bam ban')
    
    @commands.command(aliases=['setdelay', 'sm', 'delay'])
    @commands.has_permissions(manage_messages = True)
    async def slowmode(self, ctx, seconds : int):
        '''
        Sets the slowmode in a particular channel, if no arguments are given it resets the slowmode
        '''
        if seconds is None:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send('<a:success:900010826495311873> Slowmode has been disabled!')
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f'<a:success:900010826495311873> Set the slowmode to `{seconds}` in this channel!')

    @commands.command(aliases=['l'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def lock(self, ctx, channel : discord.TextChannel = None):
        '''
        Locks a certain channel for the @everyone role
        '''
        if channel is None:
            channel = ctx.channel
        
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.message.delete()
        await ctx.send(embed = discord.Embed(description = f'<a:success:900010826495311873> Locked down {channel.mention}', color = discord.Color.from_rgb(255,8,0)).set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url))

    @commands.command(aliases=['ul'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def unlock(self, ctx, channel : discord.TextChannel = None):
        '''
        Unlocks a certain channel for the @everyone role
        '''
        if channel is None:
            channel = ctx.channel
        
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.message.delete()
        await ctx.send(embed = discord.Embed(description = f'<a:success:900010826495311873> `{ctx.channel.name}` has successfully been unlocked', color = discord.Color.from_rgb(0, 255, 4)).set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url))


    @commands.guild_only()
    @permissions.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kicks a user from the current server. """
        if await permissions.check_priv(ctx, member):
            return

        em = discord.Embed(title = '<:worrysip:897416916195504158> You were kicked', color =  discord.Color.from_rgb(255,8,0))
        em.description = f'<:tj_catgun:895964998000578570>  **Offender:** {member.name}#{member.discriminator} ({member.mention})\n<a:dj_announcement:876792230843650048> **Reason:** {reason}\n<:kool:901095271667232789> **Responsible Moderator:** {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention})\n**Server:** {ctx.guild.name}'
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        try:
            await member.send(embed = em)
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("kicked"))
        except Exception as e:
            await ctx.send(e)
        
    @commands.command(aliases=["nick", 'setnick', 'changenick'])
    @commands.guild_only()
    @permissions.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        """ Nicknames a user from the current server. """
        if await permissions.check_priv(ctx, member):
            return

        try:
            await member.edit(nick=name, reason=default.responsible(ctx.author, "<a:success:900010826495311873> Changed by command"))
            message = f"<a:success:900010826495311873> Changed **{member.name}'s** nickname to **{name}**"
            if name is None:
                message = f"<a:success:900010826495311873> Reset **{member.name}'s** nickname"
            await ctx.send(embed = discord.Embed(description = message, color = discord.Color.from_rgb(0, 255, 4)).set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """ Bans a user from the current server. """
        if member is not None and await permissions.check_priv(ctx, member):
            return

        em = discord.Embed(title = '<:worrysip:897416916195504158> You were banned', color = discord.Color.from_rgb(255,8,0))
        em.description = f'<:tj_catgun:895964998000578570> **Offender:** {member.name}#{member.discriminator} ({member.mention})\n<a:dj_announcement:876792230843650048> **Reason:** {reason}\n<:kool:901095271667232789> **Responsible Moderator:** {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention})\n**Server:** {ctx.guild.name}'
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        try:
            await member.send(embed = em)
            await ctx.guild.ban(member, reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("banned"))
        except Exception as e:
            await ctx.send(e)
            
    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID, *, reason: str = None):
        """ Unbans a user from the current server. """
        em = discord.Embed(title = '<:worrysip:897416916195504158> You were unbanned', color = discord.Color.from_rgb(0, 255, 4))
        em.description = f'**Reason:** {reason}\n**Responsible Moderator:** {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention})\n**Server:** {ctx.guild.name}'
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        try:
            await ctx.guild.unban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("unbanned"))
        except Exception as e:
            await ctx.send(e)

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx, *, amount:int = 1):
        """
        A command that bulk clears/deletes messages in a channel
        """
        if amount < 0 or amount == 0:
            await ctx.send('Amount has to be positive <:angrybaby:903972672491388928>')
        await ctx.channel.purge(limit = amount +1)
        embed = discord.Embed(title="Done!",
                          description=f"Purged `{amount}` messages in {ctx.channel.mention}", color = discord.Color.from_rgb(0, 255, 4))
        m = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await m.delete()
    
    @commands.command(aliases=['r'])
    @commands.has_permissions(manage_roles = True)
    async def role(self, ctx, member: discord.Member, *, role: discord.Role):
        action = None

        if ctx.author == member:
            await ctx.send('You can\'t give roles to your self nerd ;-;')
            return

        for _role in member.roles:
            if _role == role:
                action = "remove"
                break

        if action is None:
            action = "add"
        
        if int(ctx.author.top_role.position) < int(role.position):
            await ctx.send(f"The role you are trying to add/remove to a member is a higher role than you, so you can't {action} this role from them.")
            return

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to add/remove role from has a higher role than you, so you can't {action} this role from them.")
            return
        
        if action == "add":
            await member.add_roles(role)
            action = "added to"
        elif action == "remove":
            action = "removed from"
            await member.remove_roles(role)
        
        await ctx.send(embed = discord.Embed(title = "<a:stars_anim:914434879670857768> Roles Updated", color = 0xFF0000, description = f"<a:success:900010826495311873> {role.mention} has been {action} {member.mention}").set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url).set_footer(text = "Thanks for using me!", icon_url = ctx.guild.icon_url))
    
    @commands.command()
    @commands.is_owner()
    async def syncban(self, ctx, userid : int, *, reason : str):
        """Bans a user across servers which opt-in"""
        user = await self.panther.fetch_user(userid)
        if user is None:
            await ctx.send(embed = discord.Embed(description = 'Nope, not a real user ID, **enter a right user id next time**'))
        else:
            msg = f"I\'ve banned {user.name} in "
            await ctx.guild.ban(user, reason = reason)
            for i in self.panther.syncban_guilds:
                g = self.panther.get_guild(i)
                if g.id != ctx.guild.id:
                    await g.ban(user, reason = f"Ban from {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator}, reason: {reason}") 
                    msg += f"**{g.name}** (`{g.id}`), "
            await ctx.send(msg)

        

def setup(panther):
    '''
    Sets up the cog by adding it to the bot
    '''
    panther.add_cog(Moderation(panther))

