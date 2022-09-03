import discord
from discord.ext import commands

class Errors(commands.Cog):
    '''
    Handles the errors that can be made in discord.py
    '''
    def __init__(self, panther):
        self.panther = panther
        self.reply = '<:reply:897416849266987078>'
        self.replyCont = '<:replyCont:897416881038848040>'
        self.worrysip = '<:worrysip:897416916195504158>'
        self.verified_bot = '<:verified_bot:897416027007250442>'
        self.ducksmh = '<a:ducksmh:897394414891196446>'

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if isinstance(error, commands.MissingRequiredArgument):
            '''
            Checks whether they missed an argument without a default value
            If yes, it raises this error and tells them that they missed one
            '''
            emb = discord.Embed(title = f'{self.worrysip} Missing Required Argument', color = discord.Color.random())
            emb.description = f'{self.verified_bot} You didn\'t provide the right type of arguments!'
            emb.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
            emb.set_footer(text = 'Nab', icon_url = ctx.guild.icon_url)
            await ctx.send(embed = emb)
        
        if isinstance(error, commands.CommandNotFound):
            '''
            If a command is found in no "loaded cog" or does not exist in the main bot file
            If the cog isn't loaded it will still raise this error
            '''
            try:
                await ctx.author.send(f'{self.ducksmh} Invalid command, to view my commands please do `p.help`!\n**Important Notice:** If this is a command related to freeloading, please do `p.freeloader` to get more information, thanks!')
            except:
                await ctx.send(f'{self.ducksmh} Invalid command, to view my commands please do `p.help`!\n**Important Notice:** If this is a command related to freeloading, please do `p.freeloader` to get more information, thanks!')
            
        
        if isinstance(error, commands.CommandInvokeError):
            '''
            If an error is found in the command's code which is unable to let the command work 
            it raises this error
            '''
            emb = discord.Embed(title = f'{self.worrysip} Command Failed', color = discord.Color.random())
            emb.description = f'{self.replyCont}Ah crap- notify my dev about this ASAP\n{self.reply}'
            emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = emb)
        
        if isinstance(error, commands.CommandOnCooldown):
            '''
            If a command is still on cooldown for a guild / channel / user it will
            raise this error    
            '''

            if int(error.retry_after) >= 3600:
                await ctx.send(
                    f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after / 3600:,.2f} hours.**"
                )
                return

            elif len(str(int(error.retry_after))) >= 3:
                await ctx.send(
                    f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after / 60:,.2f} minutes.**"
                )
                return

            elif int(error.retry_after) <= 99:
                await ctx.send(
                    f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after:,.2f} seconds.**"
                )
                return

        if isinstance(error, commands.MissingPermissions):
            '''
            If a user doesn't have the correct permissions in the channel / guild
            it will raise this error and tell them they don't have the correct permissions
            '''
            emb = discord.Embed(title = f'{self.worrysip} Missing Permissions', color = discord.Color.random())
            emb.description = f'This isn\'t meant for you, you clearly need more permissions (mod / admin) for this command, if you think this is an issue, please join the support server for more information.'
            emb.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
            emb.set_footer(text = 'Nab', icon_url = ctx.guild.icon_url)
            await ctx.send(embed = emb)

        if isinstance(error, commands.BotMissingPermissions):
            '''
            If a user doesn't have the correct permissions in the channel / guild
            it will raise this error and tell them they don't have the correct permissions
            '''
            emb = discord.Embed(title = f'{self.worrysip} Bot Missing Permissions', color = discord.Color.random())
            emb.description = f'I do not have the right perms to execute that command, make sure to give me perms'
            emb.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon_url)
            emb.set_footer(text = 'Nab', icon_url = ctx.guild.icon_url)
            await ctx.send(embed = emb)
        
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
        
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        
        if isinstance(error, commands.TooManyArguments):
            await ctx.send('Too many arguments provided!')
        
        if isinstance(error, commands.NotOwner):
            await ctx.send('Do you think you own me by any chance?')
        
        if isinstance(error, commands.UserInputError):
            await ctx.send('Wrong user input type')
        
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('Sorry that member isn\'t in my cache!')
        
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send('Sorry for the trouble but it seems that someone else is using this command right now!\nPlease try in a minute (I have reset the cooldown for this command)')
            ctx.command.reset_cooldown(ctx)
        

        print(error)

def setup(panther):
    '''
    Sets up the cog by adding it to the bot
    '''
    panther.add_cog(Errors(panther))