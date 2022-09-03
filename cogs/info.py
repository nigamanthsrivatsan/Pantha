import discord
from discord.ext import commands
import random
from discord_components import * 

class Info(commands.Cog):
    '''
    Information commands about users, channels, guilds and the bot itself!
    '''
    def __init__(self, panther):
        self.panther = panther
        self.sniped_messages = {}
        self.edit_sniped_messages = {}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Info commads are loaded')

    @commands.command()
    async def ping(self, ctx):
        '''
        Pings the bot!
        '''
        emb = discord.Embed(title = ':ping_pong: Ping', color = discord.Color.random())
        emb.description = f':ping_pong: Trust me this number doesn\'t matter or make sense but uh-\nNumber: `{random.randint(50, 200)}`'
        emb.set_footer(text = 'Hosted by Not Imp', icon_url = self.panther.user.avatar_url)
        await ctx.send(embed = emb)
    
    @commands.command(aliases=['bs', 'stats'])
    async def botstats(self, ctx):
        '''
        Displays the stats of the bot
        '''
        em = discord.Embed(title=  "<:verified_bot:897416027007250442> panther Stats", color = self.panther.user.color, description = "My stats :partying_face:")
        em.add_field(name = "Users:", value = f"`{len(self.panther.users)}`")
        em.add_field(name = "Servers:", value = f"`{len(self.panther.guilds)}`")
        em.add_field(name = "Total Commands:", value = f"`{len(self.panther.commands)}`")
        await ctx.send(embed = em)
    
    @commands.command()
    async def userinfo(self, ctx, member : discord.Member = None):
        '''
        Displays the information about a user
        '''
        if member == None:
            member = ctx.author
        pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
        roles = [role for role in member.roles]
        embed = discord.Embed(title = "Info", color = discord.Color.random(), description = f"Information about: {member.name}")
        embed.add_field(name = "Nickname", value = member.nick or None)
        embed.add_field(name = "Verification Pending", value = member.pending)
        embed.add_field(name = "Status:", value = member.raw_status)
        if member.mobile_status:
            device = "Mobile"
        elif member.desktop_status:
            device = "Desktop"
        elif member.web_status:
            device=  "Web"
        embed.add_field(name = "Discord Device:", value = device)
        embed.add_field(name = "Color", value = member.color)
        embed.add_field(name = "Mention:", value = member.mention)
        embed.add_field(name = "Top Role:", value = member.top_role.mention)
        embed.add_field(name = "Voice State:", value = member.voice or None)
        embed.set_footer(icon_url=member.avatar_url, text=f'Requested By: {ctx.author.name}')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['support', 'inv'])
    async def invite(self, ctx):
        '''
        Shows the invite link
        '''
        await ctx.message.delete()
        em = discord.Embed(title=  "<:verified_bot:897416027007250442> Invite Me", color = self.panther.user.color, description = f"Panther is a bot with over **20** commands and a timer command that dms users, to good moderation commands\n\nInvite me by clicking [here]({self.panther.invite_link})")
        
        async def callback(interaction):
            return True

        await ctx.send(
            embed = em,
            components=[
                self.panther.components_manager.add_callback(
                    Button(style=ButtonStyle.URL, label="Invite Me", url = self.panther.invite_link, emoji = "🔗"), callback
                ),
            ]
        )
    
        
    @commands.command()
    async def vote(self, ctx):
        """Vote for Pantha!"""
        await ctx.message.delete()
        em = discord.Embed(title = 'Thanks for voting! <:catheart:901699743288270878>', color = discord.Color.random(), description = f'We appreciate you taking interest in voting for us!\n\nClick [here]({self.panther.vote_link}) to vote\nClick [here]({self.panther.jedi_link}) to join **The Jedi**')
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        em.set_footer(text = 'Thanks for voting! :3', icon_url = ctx.guild.icon_url)

        async def callback(interaction):
            return True

        await ctx.send(
            embed = em,
            components=[
                self.panther.components_manager.add_callback(
                    Button(style=ButtonStyle.URL, label="Vote For Me", url = self.panther.vote_link, emoji = "💎"), callback
                ),
                self.panther.components_manager.add_callback(
                    Button(style=ButtonStyle.URL, label="Join The Jedi", url = self.panther.jedi_link, emoji = "🏆"), callback
                ),
            ]
        )
    
    
    @commands.command(aliases = ["sc"])
    async def servercount(self, ctx):
        """Shows my server count"""
        sc = 0
        for i in self.panther.guilds:
            sc += 1
        embed = discord.Embed(title = "Server Count", color = ctx.author.color)
        embed.add_field(name = "Server Count:", value = f"`{sc}`")
        embed.add_field(name = "User Count:", value = f'`{len(self.panther.users)}`')
        embed.set_author(name = self.panther.user.name, icon_url = self.panther.user.avatar_url)        
        await ctx.send(embed = embed)
                    
    @commands.command(aliases=['whois'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def wi(self, ctx, userid : int):
        """Shows the user and what mutual servers they are in"""
        user = await self.panther.fetch_user(userid)
        if user is None:
            await ctx.send(embed = discord.Embed(description = 'Nope, not a real user ID, **enter a right user id next time**'))
        else:
            msg = ""
            for guild in self.panther.guilds:
                for member in guild.members:
                    if member.id == userid:
                        msg += f"**{guild.name}** (`{guild.id}`)\n"
            
            await ctx.send(embed = discord.Embed(description = f'**Mutual Servers:**\n\n{msg}').set_author(name = f'{user.name}#{user.discriminator} - {user.id}', icon_url = user.avatar_url))

    @wi.error
    async def wi_error(self, ctx, error):
        # For this error example we check to see where it came from...
        if isinstance(error, commands.BadArgument):
            await ctx.send(embed = discord.Embed(description = 'Nope, not a real user ID, **enter a right user id next time**'))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.sniped_messages[message.guild.id, message.channel.id] = (
            message.content, message.author, message.channel.name,
            message.created_at, message.attachments)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        self.edit_sniped_messages[before.guild.id, before.channel.id] = (
                                                before.content,
                                                after.content,
                                                before.author,
                                                before.channel.name
                                                )

    @commands.command(aliases=['s'])
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time, attachments = self.sniped_messages[
                ctx.guild.id, ctx.channel.id]
            
            files = ""
            for file in attachments:
                files += f"[{file.filename}]({file.proxy_url})" + "\n"
            embed = discord.Embed(
                description=contents, color=0x00FFFF, timestamp=time)
            embed.set_author(
                name=f"{author.name}#{author.discriminator}",
                icon_url=author.avatar_url)
            embed.add_field(
                name="Attachments",
                value=files[:-1] if len(attachments) != 0 else "None"
            )
            embed.set_footer(text=f"Deleted in #{channel_name}")

            await ctx.send(embed=embed)
        except:
            await ctx.send("No messages were deleted here.")

    @commands.command(aliases = ['es'])
    async def editsnipe(self, ctx):
        try:
            before_content, after_content, author, channel_name = self.panther.edit_sniped_messages[ctx.guild.id, ctx.channel.id]

            embed = discord.Embed(description = f"**Before:**\n{before_content}\n\n**After:**\n{after_content}", color=0x00FFFF)
            embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
            embed.set_footer(text=f"Edited in #{channel_name}")

            await ctx.send(embed=embed)
        except:
            await ctx.send("No messages were edited here.")
    
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def roleinfo(self, ctx, *, role_: discord.Role = None):
        '''
        Shows you various information about a particular role!
        '''
        role = role_
        if role is None:
            await ctx.send("Please provide a valid role")
        em = discord.Embed(title = f"Info about {role.name}", color = ctx.author.color, description = f"Here is an insight into {role.mention}")
        em.add_field(name = "ID:", value = f"`{role.id}`")
        em.add_field(name = "Name:", value = f"`{role.name}`")
        em.add_field(name = "Server it belongs to:", value = f"{role.guild.name}", inline = True)

        em.add_field(name = "Hoisted:", value = f"`{role.hoist}`")
        em.add_field(name = "Managed by extension:", value = f"`{role.managed}`", inline = True)
        em.add_field(name = "Boost Role:", value = f"`{role.is_premium_subscriber()}`", inline = True)

        em.add_field(name = "Mentionable:", value = f"`{role.mentionable}`" )
        em.add_field(name = "Is Default:", value = f"`{role.is_default()}`", inline = True)
        em.add_field(name = "Bot Role:", value = f"`{role.is_bot_managed()}`", inline = True)

        em.add_field(name = "Color:", value = f"{role.color}")
        em.add_field(name = "Created At:", value = f"{role.created_at}", inline = True)
        em.add_field(name = "People with it:", value =f"{len(role.members)}", inline = True)
        msg = "```diff\n"
        if role.permissions.administrator:
            msg += "+ Administrator\n"
        else:
            msg += "- Administrator\n"
        if role.permissions.manage_guild:
            msg += "+ Manage Server\n"
        else:
            msg += "- Manage Server\n"
        if role.permissions.mention_everyone:
            msg += "+ Ping Everyone\n"
        else:
            msg += "- Ping Everyone\n"
        if role.permissions.manage_roles:
            msg += "+ Manage Roles\n"
        else:
            msg += "- Manage Roles\n"
        if role.permissions.manage_channels:
            msg += "+ Manage Channels\n"
        else:
            msg += "- Manage Channels\n"
        if role.permissions.ban_members:
            msg += "+ Ban Members\n"
        else:
            msg += "- Ban Members\n"
        if role.permissions.kick_members:
            msg += "+ Kick Members\n"
        else:
            msg += "- Kick Members\n"
        if role.permissions.view_audit_log:
            msg += "+ View Audit Log\n"
        else:
            msg += "- View Audit Log\n"
        if role.permissions.manage_messages:
            msg += "+ Manage Messages\n"
        else:
            msg += "- Manage Messages\n"
        if role.permissions.add_reactions:
            msg += "+ Add Reactions\n"
        else:
            msg += "- Add Reactions\n"
        if role.permissions.view_channel:
            msg += "+ Read Messages\n"
        else:
            msg += "- Read Messages\n"
        if role.permissions.send_messages:
            msg += "+ Send Messages\n"
        else:
            msg += "- Send Messages\n"
        if role.permissions.embed_links:
            msg += "+ Embed Links\n"
        else:
            msg += "- Embed Links\n"
        if role.permissions.read_message_history:
            msg += "+ Read Message History\n"
        else:
            msg += "- Read Message History\n"
        if role.permissions.view_guild_insights:
            msg += "+ View Guild Insights\n"
        else:
            msg += "- View Guild Insights\n"
        if role.permissions.connect:
            msg += "+ Join VC\n"
        else:
            msg += "- Join VC\n"
        if role.permissions.speak:
            msg += "+ Speak in VC\n"
        else:
            msg += "- Speak in VC\n"
        
        if role.permissions.change_nickname:
            msg += "+ Change Nickname\n"
        else:
            msg += "- Change Nickname\n"
        
        if role.permissions.manage_nicknames:
            msg += "+ Manage Nicknames\n"
        else:
            msg += "- Manage Nicknames\n"
        
        if role.permissions.manage_webhooks:
            msg += "+ Manage Webhooks\n"
        else:
            msg += "- Manage Webhooks\n"
        
        if role.permissions.manage_emojis:
            msg += "+ Manage Emojis\n"
        else:
            msg += "- Manage Emojis\n"
        

        msg += "\n```"
        em.add_field(name = "Permissions:", value = msg, inline = False)

        em.set_footer(text = "invite me ;)", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = str(ctx.guild.icon_url))
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = em)

def setup(panther):
    '''
    Sets up the cog by adding it to the bot
    '''
    panther.add_cog(Info(panther))
