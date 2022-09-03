import discord
from discord.ext import commands
import asyncio
import random
from random import choice
import os
import dbl
import aiosqlite
from discord_components import *

class Dank(commands.Cog, name = "Dank Memer"):
    """Commands which can help Dank Memer users / servers!"""
    def __init__(self, panther):
        self.panther = panther
        self.topToken = self.panther.config["toptoken"]
        self.dblpy = dbl.DBLClient(self.panther, self.topToken)
    
    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("./data/freeload.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS freeload (guildid INTEGER, heistmode INTEGER, logid INTEGER, duration STRING);")
                await connection.commit()
                
    
    @commands.command(aliases=['dr', 'dankmemerrules', 'dmorules', 'danktos', 'dankmemertos'])
    async def dankrules(self, ctx, rule: int = None):
        """Shows the official dank-memer rules"""
        rules = """
By using Dank Memer, you agree to the following rules. If you break any rules we reserve the right to remove your access to any and all Dank Memer services.

**[Rule One](https://dankmemer.lol/rules) - User-bots, Spamming and Macros**
Usage of user-bots, macros, scripts, auto-typers or anything else enabling automation of commands is strictly forbidden. In addition to this, massive amounts of spam is not allowed and will be punished with equal severity.

**[Rule Two](https://dankmemer.lol/rules) - Sharing Exploits**
Sharing exploits or exploitative bugs with other users is forbidden. Please report all exploits and bugs to staff on the [Dank Memer Support Server](https://discord.gg/meme) so that we can fix it as soon as possible.

**[Rule Three](https://dankmemer.lol/rules) - Giveaway Requirements or Bot Usage Requirements in Your Server**
You should not lock the bot, or giveaways for the bot, behind paywalls. This means stuff like patreon roles, donor roles (with irl money), etc, is forbidden for giveaway requirements or role locks. The only exception to this is boosters, we will allow you to lock things behind being a booster for your server. Things like level locks using external bots is perfectly fine.

**[Rule Four](https://dankmemer.lol/rules) - Racism, Homophobia, Sexism or Slurs**
None of the above will be tolerated through usage of Dank Memer. We will not punish you for what you say outside of the usage of our commands. Evidence found of this done through our commands will result in punishment.

**[Rule Five](https://dankmemer.lol/rules) - Advertisement**
Usage of Dank Memer to advertise or promote anything will result in a punishment. This includes other Discord servers. Giving our currency in exchange for invites to your server is also forbidden.

**[Rule Six](https://dankmemer.lol/rules) - Real Money Trading**
Dank Memer's currency is not to be traded for real money or discord nitro. Buying anything with real money outside of our patreon and website, will get you a ban.

**[Rule Seven](https://dankmemer.lol/rules) - Etiquette**
Starting harmful rumors about the bot, causing unnecessary drama within our servers about the bot, or witch hunting staff members are all ban worthy behaviors.

**[Rule Eight](https://dankmemer.lol/rules) - Discord Terms of Service and Usage Guidelines**
Through usage of Dank Memer, you accept [Dank Memer's Terms of Service](https://dankmemer.lol/terms) and [Privacy Policy](https://dankmemer.lol/privacy). Additionally, you accept Discord's [Terms of Service](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines), these of which are enforceable through Dank Memer
        """
        rule1 = """
**[Rule One](https://dankmemer.lol/rules) - User-bots, Spamming and Macros**
Usage of user-bots, macros, scripts, auto-typers or anything else enabling automation of commands is strictly forbidden. In addition to this, massive amounts of spam is not allowed and will be punished with equal severity.
        """
        rule2 = """
**[Rule Two](https://dankmemer.lol/rules) - Sharing Exploits**
Sharing exploits or exploitative bugs with other users is forbidden. Please report all exploits and bugs to staff on the [Dank Memer Support Server](https://discord.gg/meme) so that we can fix it as soon as possible.
        """

        rule3 = """
**[Rule Three](https://dankmemer.lol/rules) - Giveaway Requirements or Bot Usage Requirements in Your Server**
You should not lock the bot, or giveaways for the bot, behind paywalls. This means stuff like patreon roles, donor roles (with irl money), etc, is forbidden for giveaway requirements or role locks. The only exception to this is boosters, we will allow you to lock things behind being a booster for your server. Things like level locks using external bots is perfectly fine.
        """

        rule4 = """
**[Rule Four](https://dankmemer.lol/rules) - Racism, Homophobia, Sexism or Slurs**
None of the above will be tolerated through usage of Dank Memer. We will not punish you for what you say outside of the usage of our commands. Evidence found of this done through our commands will result in punishment.
        """

        rule5 = """
**[Rule Five](https://dankmemer.lol/rules) - Advertisement**
Usage of Dank Memer to advertise or promote anything will result in a punishment. This includes other Discord servers. Giving our currency in exchange for invites to your server is also forbidden.
        """

        rule6 = """
**[Rule Six](https://dankmemer.lol/rules) - Real Money Trading**
Dank Memer's currency is not to be traded for real money or discord nitro. Buying anything with real money outside of our patreon and website, will get you a ban.
        """

        rule7 = """
**[Rule Seven](https://dankmemer.lol/rules) - Etiquette**
Starting harmful rumors about the bot, causing unnecessary drama within our servers about the bot, or witch hunting staff members are all ban worthy behaviors.
"""
        
        rule8 = """
**[Rule Eight](https://dankmemer.lol/rules) - Discord Terms of Service and Usage Guidelines**
Through usage of Dank Memer, you accept [Dank Memer's Terms of Service](https://dankmemer.lol/terms) and [Privacy Policy](https://dankmemer.lol/privacy). Additionally, you accept Discord's [Terms of Service](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines), these of which are enforceable through Dank Memer
"""
        if rule is None:
            await ctx.message.delete()
            await ctx.send(embed = discord.Embed(title = 'Dank Memer Rules', description = rules).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
        else:
            if rule < 1 or rule > 8:
                await ctx.send('That isn\'t a valid rule dumbhead!')
                return
            if rule == 1:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule1).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 2:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule2).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 3:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule3).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 4:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule4).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 5:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule5).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 6:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule6).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 7:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule7).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))
            elif rule == 8:
                await ctx.message.delete()
                await ctx.send(embed = discord.Embed(title = f'Dank Memer Rule #{rule}', description = rule8).set_image(url = 'https://images-ext-2.discordapp.net/external/RBCjBFMVUT2as_WJKRmujIIFNq8oiHCTNw3dfRlRkKU/https/media.discordapp.net/attachments/851130302465835058/859883918932574248/Screen_Shot_2021-06-30_at_3.51.36_PM.png?width=1440&height=24'))

    @commands.group(aliases=["freeloaders", "fl", "anti-freeloader", "auto-freeloader"])
    @commands.guild_only()
    async def freeloader(self, ctx):
        """Auto-bans people who leave after an event!"""
        if ctx.invoked_subcommand is None:
            return await ctx.send_help("freeloader")

    @freeloader.command(aliases=['information'])
    @commands.guild_only()
    async def info(self, ctx):
        '''
        Displays information about the freeloader banning system
        '''
        await ctx.message.delete()
        em = discord.Embed(title = '<a:heart_anim:911579838811353098> Explanation of Auto Freeloader Banning', color = discord.Color.from_rgb(25, 250, 0))
        em.set_image(url = 'https://images-ext-2.discordapp.net/external/Z8QX8YcUI8LAOpY4Bm-088TBEIxkk_Cm2murt_wC9T8/https/media.discordapp.net/attachments/851130302465835058/859178210028421171/Screen_Shot_2021-06-28_at_5.07.24_PM.png?width=1440&height=16')
        em.set_thumbnail(url = ctx.guild.icon_url)
        em.description = '<:pt_one:909031465117950003> How does it work?\n<:tj_yellowBow:885824362836549665> When heistmode is enabled by an admin or above, anyone who leaves the server will be banned!\n<:tj_yellowBow:885824362836549665> This is because when people leave after the heist our system catches them leaving and bans them for the duration you have set (if none then it is permanent)\n\n<:pt_two:909031505060311041> What exactly is a "freeloader"?\n<:tj_blueBow:879220868499243058> To understand what a "freeloader" is exactly you can do `p.freeloader freeload`'
        await ctx.send(embed = em)
    
    @freeloader.command(aliases=['freeloads'])
    @commands.guild_only()
    async def freeload(self, ctx):
        '''Tells you how to NOT be banned from servers'''
        content = """
        <:pt_one:909031465117950003> **What is a freeloader?**\n<:bullet:911962148828225536> A freeloader is someone who leaves a server after they do a heist or a big event.\n<:bullet:911962148828225536> We detect freeloaders using our commands!\n\n<:pt_two:909031505060311041> **How to avoid freeloading**\n<:bullet:911962148828225536> Naturally you would wonder why you should stay in a server rather than leaving now since you have your money.\n<:bullet:911962148828225536> Imagine putting a lot of effort onto a server, or anything and then seeing people leave just when you want your server to grow\n\n<:pt_three:909031538979647529> **What can I do if I was a freeloader but I don't freeload anymore?**\n<:bullet:911962148828225536> Make sure you don't do it again since that will just make you banned in more servers\n<:bullet:911962148828225536> Make sure you go to server's "**Ban Appeal**" server and say that you were a freeloader and you won't freeload again.\n\n\n:warning: **Warning: We are not responsible for any actions that happen to you while freeloading or not, the bot is meant for server owners who want to auto-ban freeloaders!**
        """
        await ctx.send(embed = discord.Embed(description = content, title = '<a:heart_anim:911579838811353098> What are freeloaders?', color = discord.Color.from_rgb(255,8,0)))

    @freeloader.command(aliases=['setdura', 'durationset'])
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    async def setduration(self,ctx, dura : str):
        '''
        Sets the duration of the ban that freeloaders get!
        '''
        vote = await self.dblpy.get_user_vote(ctx.author.id)
        if not vote:
            await ctx.send(embed = self.panther.vote_embed)

        if dura[-1] != "d":
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply('<a:ducksmh:897394414891196446> Please mention the time properly, minimum time is 7 days! `p.setduration 7d` or whatever you want to ban freeloaders for!')
            return
        try:
            amount = int(dura[:-1])
        except:
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply('<a:ducksmh:897394414891196446> Please mention the time properly, minimum time is 7 days! `p.setduration 7d` or whatever you want to ban freeloaders for!')
            return
        if amount < 7:
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply('<a:ducksmh:897394414891196446> The minimum duration is **7 days**')
            return
        
        async with aiosqlite.connect("./data/freeload.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM freeload WHERE guildid = ?",(ctx.guild.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO freeload (guildid, heistmode, logid, duration) VALUES (?,?,?,?)",(ctx.guild.id, 0,0, f"{amount} days"))
                else:
                    await cursor.execute("UPDATE freeload SET duration = ? WHERE guildid = ?", (f"{amount} days", ctx.guild.id))
                await connection.commit()
                

        await ctx.send(embed = discord.Embed(description = f'<a:success:900010826495311873> I will now ban freeloaders for **{amount} days**', color = discord.Color.from_rgb(25, 250, 0)))

    @freeloader.command()
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    @commands.cooldown(1, 300 ,commands.BucketType.guild)
    async def heistmode(self, ctx):
        '''
        Toggles whether freeeloaders get banned for your duration!
        '''
        emb = discord.Embed(title = 'Are you sure you want to do this?', color = discord.Color.red())
        emb.description = '<a:uhoh:912561508779716628> **Are you certain you want to do this?**\n<:bullet:911962148828225536> This action is irreversible for **5 minutes**\n<:bullet:911962148828225536> This will ban all freeloaders until 5 minutes after your heist ends\n<:bullet:911962148828225536> **DO NOT forget to toggle heistmode after your heist, to do so you can do `p.freeloader heistmode`**\n\n<:bow:912325550838804550> **To Confirm:**\nTo confirm this action, please react with <a:success:900010826495311873>!'
        emb.set_thumbnail(url = ctx.guild.icon_url)
        emb.set_image(url = 'https://images-ext-2.discordapp.net/external/Z8QX8YcUI8LAOpY4Bm-088TBEIxkk_Cm2murt_wC9T8/https/media.discordapp.net/attachments/851130302465835058/859178210028421171/Screen_Shot_2021-06-28_at_5.07.24_PM.png?width=1440&height=16')
        m = await ctx.send(embed = emb)
        await m.add_reaction('<a:success:900010826495311873>')
        await m.add_reaction('❌')

        emojis = ['<a:success:900010826495311873>', '❌']

        def check(reaction, user):
            if user == ctx.author:
                if str(reaction.emoji) in emojis:
                    return True

        
        try:
            reaction, user = await self.panther.wait_for('reaction_add', timeout=30.0, check=check)

        except asyncio.TimeoutError:
            ctx.command.reset_cooldown(ctx)
            await ctx.send('Hmm, seems like we\'re not turning on heist mode today!')

        else:
            if str(reaction.emoji) != "<a:success:900010826495311873>":
                return
            
            async with aiosqlite.connect("./data/freeload.db") as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute("SELECT * FROM freeload WHERE guildid = ?",(ctx.guild.id,))
                    rows = await cursor.fetchone()
                    if not rows:
                        await cursor.execute("INSERT INTO freeload (guildid, heistmode, logid, duration) VALUES (?,?,?,?)",(ctx.guild.id, 0,0, "permanent"))
                        await cursor.execute("UPDATE freeload SET heistmode = ? WHERE guildid = ?", (1, ctx.guild.id))
                        await cursor.execute("SELECT * FROM freeload WHERE guildid = ?",(ctx.guild.id,))
                        rows = await cursor.fetchone()
                        dura = rows[3]
                        emb = discord.Embed(title = '<a:heart_anim:911579838811353098> Heist Mode Enabled', color = discord.Color.from_rgb(0, 255, 4))
                        emb.description = '<:bullet:911962148828225536> <a:nyaHyper:910079649302867968> **Heist Mode** has been enabled!\n<:bullet:911962148828225536> <a:nyaFlowers:910082026365919244> Freeloaders are now permanently banned (to change the duration please use `p.duration <duration>`)'
                        emb.add_field(name = '<a:nyaNerd:910081561892888606> Logs:', value = '<:bullet:911962148828225536> To setup a logging channel you need to do: `p.setfreeloaderlogs <channel>`')
                        emb.add_field(name = '<a:nyaLove:911846406250201108> Invite Me', value = f'<:tj_duckpog:863033465968132136> Make sure to invite me, I can **auto-ban freeloaders for your server as well**\n\n[Click Here]({self.panther.invite_link}) to do so')
                        emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                        emb.set_footer(text = 'Thanks for using me!', icon_url = ctx.guild.icon_url)
                        await ctx.send(embed = emb)
                        
                    else:
                        if rows[1] == 0:
                            dura = rows[3]
                            await cursor.execute("UPDATE freeload SET heistmode = ? WHERE guildid = ?", (1, ctx.guild.id))
                            emb = discord.Embed(title = '<a:heart_anim:911579838811353098> Heist Mode Enabled', color = discord.Color.from_rgb(0, 255, 4))
                            emb.description = '<:bullet:911962148828225536> <a:nyaHyper:910079649302867968> **Heist Mode** has been enabled!\n<:bullet:911962148828225536> <a:nyaFlowers:910082026365919244> Freeloaders are now permanently banned (to change the duration please use `p.duration <duration>`)'
                            emb.add_field(name = '<a:nyaNerd:910081561892888606> Logs:', value = '<:bullet:911962148828225536> To setup a logging channel you need to do: `p.setfreeloaderlogs <channel>`')
                            emb.add_field(name = '<a:nyaLove:911846406250201108> Invite Me', value = f'<:tj_duckpog:863033465968132136> Make sure to invite me, I can **auto-ban freeloaders for your server as well**\n\n[Click Here]({self.panther.invite_link}) to do so')
                            emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                            emb.set_footer(text = 'Thanks for using me!', icon_url = ctx.guild.icon_url)
                            await ctx.send(embed = emb)
                        else:
                            await cursor.execute("UPDATE freeload SET heistmode = ? WHERE guildid = ?", (0, ctx.guild.id))
                            emb = discord.Embed(title = '<a:heart_anim:911579838811353098> Heist Mode Disabled', color = discord.Color.from_rgb(0, 255, 4))
                            emb.description = '<a:waiting:911968094942023710> Heist mode has been disabled\n<a:dj_yesyes:859406412656410674> People who leave won\'t be banned now, you can change this setting with `p.heistmode` anytime!'
                            emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                            emb.set_footer(text = 'Thanks for using me!', icon_url = ctx.guild.icon_url)
                            await ctx.send(embed = emb)

                    await connection.commit()
                    

    @freeloader.command(aliases=['setfreeloaderlogs', 'freeloaderslogs', 'freeloaderlogs'])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    @commands.cooldown(1, 100, commands.BucketType.guild)
    async def freeloaderlog(self, ctx, channel: discord.TextChannel = None):
        '''
        Sets a channels where you get logs of who gets banned!
        '''
        if channel is None:
            channel = ctx.channel
        
        async with aiosqlite.connect("./data/freeload.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM freeload WHERE guildid = ?",(ctx.guild.id,))
                rows = await cursor.fetchone()

                if not rows:
                    await cursor.execute("INSERT INTO freeload (guildid, heistmode, logid, duration) VALUES (?,?,?,?)",(ctx.guild.id,channel.id ,0, "permanent"))
                else:
                    await cursor.execute("UPDATE freeload SET logid = ? WHERE guildid = ?", (channel.id, ctx.guild.id))
        

        em = discord.Embed(description = f'<:kool:901095271667232789> The freeloader logging channel has been set to {channel.mention}', color = discord.Color.from_rgb(0, 255, 4))
        await ctx.send(embed = em)

        

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        async with aiosqlite.connect("./data/freeload.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM freeload WHERE guildid = ?",(guild.id,))
                rows = await cursor.fetchone()
                if not rows:
                    return
                else:
                    if rows[1] == 0:
                        return

                    dura = rows[3]
                    logid = int(rows[2])

                    for channel in guild.channels:
                        if int(channel.id) == logid:
                            em = discord.Embed(title = 'Freeloader Caught', color = discord.Color.random())
                            em.add_field(name = 'ID:', value = member.id)
                            em.add_field(name = 'Tag:', value = f'{member.name}#{member.discriminator}')
                            em.set_footer(text = 'Thanks for using me!', icon_url = guild.icon_url)
                            em.set_author(name = member.name, icon_url = member.avatar_url)
                            await channel.send(embed = em)
                    
                    if dura == "permanent":
                        await member.send(f'You were banned from **{guild.name}** for freeloading **permanently**')
                    else:
                        await member.send(f'You were banned from **{guild.name}** for freeloading for **{dura}**')

                    try:
                        await member.ban(reason = 'Stinky Freeloader! Left the server while heist mode was on')
                    except:
                        pass

def setup(panther):
    """
    Sets up the cog by adding it to the bots extensions!
    """
    panther.add_cog(Dank(panther))