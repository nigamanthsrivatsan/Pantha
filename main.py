import os
import discord
from discord.ext import commands
from panther import PantherBot
import random
from discord_components import DiscordComponents

class PanthaHelp(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title = 'Bot Commands', color = discord.Color.from_rgb(25, 250, 0))
        embed.set_author(name = panther.user.name, icon_url = panther.user.avatar_url)
        embed.description = '💘 Type `p.help <category>` for more information on a category!'
        for cog in mapping:
            if cog is not None:
                if cog.qualified_name not in panther.hidden_cogs:
                    embed.add_field(name = f'`-` {cog.qualified_name}', value = f'`—>` {cog.description}')

        await self.get_destination().send(embed = embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title = f'{cog.qualified_name} Commands', color = discord.Color.from_rgb(25, 250, 0))
        embed.set_author(name = panther.user.name, icon_url = panther.user.avatar_url)
        msg = ""
        for command in cog.get_commands():
            msg += f"`—>` `{command.name}`: {command.help}\n"
            
        embed.description = f':heart: Type `p.help <command>` for more help on a command!\n\n{msg}'
        
        # integrating trough uncategorized commands
        commands_desc = ''
        for command in panther.walk_commands():
            # if cog not in a cog
            # listing command if cog name is None and command isn't hidden
            if not command.cog_name and not command.hidden:
                commands_desc += f'`—>` {cog.description}\n'

        # adding those commands to embed
        if commands_desc:
            # if a cog is in the main file?
            embed.add_field(name='`—>` Miscellaneous', value=commands_desc, inline=False)
        await self.get_destination().send(embed = embed)
        
    
    async def send_group_help(self, group):
        embed = discord.Embed(title = f'{group.name} Help', color = discord.Color.from_rgb(25, 250, 0))
        embed.set_author(name = panther.user.name, icon_url = panther.user.avatar_url)
        msg = '<a:heart_anim:911579838811353098> Type `p.help <subcommand>` for more information on a subcommand!\n\n<:bow:912325550838804550> **Sub-Commands List:**\n'
        for index, command in enumerate(group.commands):
            msg += f"<a:pinkarrow_anim:912631167700840488>  **p.{group.name} {command.name}**: {command.help}.\n"
        embed.description = msg
        await self.get_destination().send(embed = embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(title = f'{command.qualified_name} Command', color = discord.Color.from_rgb(25, 250, 0))
        embed.set_author(name = panther.user.name, icon_url = panther.user.avatar_url)
        if command.signature == " " or command.signature == "":
            embed.description = f"```yml\nSyntax: p.{command.qualified_name}\n```"
        else:
            embed.description = f"```yml\nSyntax: p.{command.qualified_name} {command.signature}\n```"
        if command.enabled:
            embed.add_field(name = '<a:success:900010826495311873> Enable/Disable Status:', value = 'Enabled')
        else:
            embed.add_field(name = '<a:error:900013056850030592> Enable/Disable Status:', value = 'Disabled')
        if command.aliases is not None:
            aliases = ""
            for a in command.aliases:
                if a == command.aliases[:-1]:
                    aliases += f"{a}"
                else:
                    aliases += f"{a}, "
            if aliases == "":
                aliases = "<a:error:900013056850030592> No Aliases Found"
            embed.add_field(name = '<:tj_PandaSip:908549399276306442> Aliases:', value = aliases)

        embed.add_field(name = '📂 Category', value = command.cog.qualified_name)
        embed.add_field(name = "<:verified_bot:897416027007250442> Command Description", value = command.help)
        await self.get_destination().send(embed = embed)


panther = PantherBot(command_prefix=commands.when_mentioned_or('p.'), intents = discord.Intents.all(), allowed_mentions = discord.AllowedMentions(everyone = False, users = True, roles = True, replied_user = True), help_command=PanthaHelp())
config = panther.get_config()
DiscordComponents(panther)

@panther.event
async def on_message(message):
    '''
    For every message sent in every server that it is there in
    '''
    if message.author == panther.user:
        return
    
    if 'donate me' in message.content:
        emb = discord.Embed(title = '<a:announce:897394481320575016> DO NOT BEG', color = discord.Color.random())
        emb.description = '• Do not beg here, it could lead to a mute or a ban **without appeal**\n\n• We do sufficient heists, giveaways, events to make sure YOU don\'t have the need to beg for virtual currency\n\n• If you aren\'t happy with it, there\'s always a button called `Leave Server`'
        emb.set_author(name = message.guild.name, icon_url = message.guild.icon_url)
        await message.reply(embed = emb)

    if ' hiest ' in message.content or ' hesit ' in message.content or message.content == "hesit" or message.content == "hiest":  
        await message.reply('I think you mean heist <:dj_YouTried:854569341683761162>')

    await panther.process_commands(message)

panther.load_cogs()
token = panther.config["token"]
panther.run(token)
