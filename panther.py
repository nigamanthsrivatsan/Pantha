import discord
from discord.ext import commands
from json import load
import os

with open('config.json', 'r') as f:
    config = load(f)

class PantherBot(commands.Bot):
    '''
    A private class which inherits the properties of a bot
    Mainly because we can have custom methods & interactions USING the client object

    Also because we have a much better way of using the client for getting arguments
    like emojis, channel ids, guild ids, and so on
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initializes the class just how the commands.Bot class is initialized
        '''
        super().__init__(*args, **kwargs)
        self.owner_id = int(config["owner"])
        self.invite_link = f'https://discord.com/api/oauth2/authorize?client_id={int(config["botId"])}&permissions=8&scope=bot'
        self.vote_link = 'https://top.gg/bot/856455153133027328/vote'   
        self.create_embeds()
        self.config = config
        self.syncban_guilds = config["syncban"]
    
    def create_embeds(self):
        self.vote_embed = discord.Embed(title = "<a:error:900013056850030592> We've got a problem buddy!", description = f"<:catheart:901699743288270878> We give you EVERYTHING for free, and we just want you to vote for us!\n:sob: Unfortunately we also want some growth around the community! Thus to access this feature you need to vote for us!\n\n:star: **Vote Link:** [click here to vote]({self.vote_link})\n**Join My Server:** [click here to join my server](https://discord.gg/thejedi)")
    
    def load_cogs(self):
        '''
        Has a predefined auto-loaded cogs to be loaded as the bot gets ready
        Other cogs can be loaded with [P]load <cog>
        '''
        extensions = [
            # utility cogs
            "cogs.utilities.dank",
            "cogs.utilities.giveaways",
            "cogs.utilities.utilities",

            # moderation cogs
            "cogs.moderation.moderation",

            # fun cogs
            "cogs.fun.fun",

            # the hidden cogs
            "cogs.hidden.errors",
            "cogs.hidden.GuildEvents",
            "cogs.hidden.owner",

            # the uncategorized cogs
            "cogs.info",
            "cogs.misc",
            "jishaku"
        ]

        for cog in extensions:
            self.load_extension(cog)
            print(f"{cog} has been loaded")

        self.hidden_cogs = ["Owner", "GuildEvents", "Errors", "Jishaku"]

    async def put_status(self, status):
        await self.change_presence(activity=discord.Game(name=status))
