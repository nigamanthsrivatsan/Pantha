import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random
from discord_components import *

class Giveaways(commands.Cog):
    """Starts a giveaway that people can join by reacting!"""
    def __init__(self, panther):
        self.panther = panther

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaways are now ready!")

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

    @commands.command(aliases=['giveawaystart', 'gs'])
    @commands.has_permissions(administrator = True)
    async def gstart(self, ctx):
        """Starts a giveaway and asks you questions to host it!"""
        question1 = discord.Embed(title=  "<a:success:900010826495311873> Giveaway Question #1", color = ctx.author.color)
        question1.add_field(name = "Question:", value = f"Which channel would you like this giveaway in? Mention it properly!")
        question1.add_field(name = "Channel Mention Example:", value =f"Mention a channel like {ctx.channel.mention}")
        question1.set_footer(text = "Don't fail the questions!")
        question1.set_thumbnail(url = ctx.author.avatar_url)
        
        question2 = discord.Embed(title=  "<a:success:900010826495311873> Giveaway Question #2", color = ctx.author.color)
        question2.add_field(name = "Question:", value = f"How long would you like this giveaway to last? ")
        question2.add_field(name = "Time Example:", value =f"Mention your number first and then type a unit.\nUnits: (s|m|h|d)")
        question2.set_footer(text = "Don't fail the questions!")
        question2.set_thumbnail(url = ctx.author.avatar_url)

        question3 = discord.Embed(title=  "<a:success:900010826495311873> Giveaway Question #3", color = ctx.author.color)
        question3.add_field(name = "Last Question:", value = f"What is the prize of this giveaway?")
        question3.set_footer(text = "Don't fail the questions!")
        question3.set_thumbnail(url = ctx.author.avatar_url)

        errorEmbed1 = discord.Embed(title = '<a:error:900013056850030592> Giveaway Failed', color = ctx.author.color)
        errorEmbed1.add_field(name = "Reason:", value = "You did not mention a channel properly")
        errorEmbed1.add_field(name = "Channel:", value = f"{ctx.channel.mention}")

        errorEmbed2 = discord.Embed(title = '<a:error:900013056850030592> Giveaway Failed', color = ctx.author.color)
        errorEmbed2.add_field(name = "Reason:", value = "You did not mention the time properly!")
        errorEmbed2.add_field(name = "Channel:", value = f"Write a number and then units (s|m|h|d)")

        timeDelay = discord.Embed(title = '<a:error:900013056850030592> Giveaway Failed', color = ctx.author.color)
        timeDelay.add_field(name = "Reason:", value = "You did not answer in time!")
        timeDelay.add_field(name = "Next Steps:", value = "Make sure you answer in 45 seconds")

        questions = [question1, question2, question3]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(embed = i)

            try:
                msg = await self.panther.wait_for('message', timeout=45.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(embed = timeDelay)
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(embed = errorEmbed1)
            return

        channel = self.panther.get_channel(c_id)
        time = self.convert(answers[1])

        if time == -1:
            await ctx.send(embed = errorEmbed2)
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return

        prize = answers[2]
        
        # send a message for the user to know the giveaway started!
        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")
        # now send the embed in the channel!
        embed = discord.Embed(title = f"{prize}", description = f"Click the button below to join <a:tj_nyaHyperYay:916525067687563294>\nTime: **{answers[1]}**\nHosted by: {ctx.author.mention}", color = ctx.author.color)
        embed.set_footer(text = f"Winners: 1 | Thanks for using me!", icon_url = ctx.guild.icon_url)
        
        users = []

        async def callback(interaction):
            users.append(interaction.user)
            await interaction.send("You have successfully joined the giveaway!")
        
        msg = await channel.send(
            embed = embed,
            content = f"<a:nyaspin:910079597062799401> NEW GIVEAWAY FROM {ctx.guild.name} <a:nyaspin:910079597062799401>",
            components = [
                self.panther.components_manager.add_callback(
                    Button(style=ButtonStyle.green, label="Enter the giveaway!", emoji=self.panther.get_emoji(910079597062799401)), callback
                )
            ]
        )
        await asyncio.sleep(time)
        winner = random.choice(users)
        await channel.send(embed = discord.Embed(description = f'Congratulations {winner.mention} has won the giveaway for **{prize}** <a:tj_nyaBoba:916525010502422538>\nClick [here]({msg.jump_url}) to teleport to the giveaway!\n\nThere were **{len(users)}** entrants <:tj_stonks:913302396132794368>').set_author(name = winner.name, icon_url = winner.avatar_url).set_footer(text = "GGs | Thanks for using me!", icon_url = ctx.guild.icon_url))
        await winner.send(embed = discord.Embed(description = f'Congratulations you won the giveaway for **{prize}** in **{ctx.guild.name}** <a:tj_nyaBoba:916525010502422538>\nClick [here]({msg.jump_url}) to teleport to the giveaway!').set_author(name = winner.name, icon_url = winner.avatar_url).set_footer(text = "GGs | Thanks for using me!", icon_url = ctx.guild.icon_url))

    @commands.command(aliases=['greroll'])
    @has_permissions(manage_guild = True)
    async def reroll(self,ctx, channel : discord.TextChannel, messageid : int):
        """Rerolls a giveaway winner!"""
        try:
            new_msg = await channel.fetch_message(messageid)
        except:
            await ctx.send("The id was entered incorrectly.\nNext time mention a channel and then the id!")
            return

        if new_msg.author != self.panther.user:
            em = discord.Embed(title=  '<a:error:900013056850030592> Reroll Failed', color = ctx.author.color, description = f"<a:error:900013056850030592> This message ([Jump URL]({new_msg.jump_url})) is not a giveaway hosted by the empire!")
            em.add_field(name = "Reason:", value = "The message you tried to reroll isn't a giveaway hosted by me")
            em.add_field(name ="How to reroll then?", value = "Take the ID of a message that is hosted by me, not some other bots!")
            return await ctx.send(embed = em)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.panther.user))

        winner = random.choice(users)
        await channel.send(f"Congratulations! The new winner is {winner.mention}!")
        try:
            await channel.send(f"URL: {new_msg.jump_url}")
        except:
            pass

def setup(panther):
    panther.add_cog(Giveaways(panther))