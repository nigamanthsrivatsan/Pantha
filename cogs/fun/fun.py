import discord
from discord.ext import commands
import random
import aiohttp
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
import dbl
import os 
import asyncio


def convert_list_to_string(org_list, seperator=" "):
    """Convert list to string, by joining all item in list with given separator.
    Returns the concatenated string"""
    return seperator.join(org_list)

class Fun(commands.Cog):
    '''
    Fun... For a change maybe?
    '''
    def __init__(self, panther):
        self.panther = panther
        topToken = self.panther.config["toptoken"]
        self.dblpy = dbl.DBLClient(self.panther, topToken)
    
    @commands.command()
    async def shoot(self, ctx, member: discord.Member):
        """Shoots a member."""
        await ctx.message.delete()
        embed = discord.Embed(title = f'{member.name} was shot! :fire:', description = f"{member.mention} shot by {ctx.author.mention}  :gun: :boom:")
        embed.set_image(url="https://i.gifer.com/XdhK.gif")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question):
        """Use a magic eight ball for tough decisions ;)"""
        ballresponse = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;"
        ]

        answer = random.choice(ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")
    
    @commands.command()
    async def bless(self, ctx, member: discord.Member):
        """Blesses someone 💘 (always works in fights)"""
        await ctx.message.delete()
        await ctx.send(f'**{ctx.author.tag}** blesses **{member.tag}** may luck be on their side <:dj_prayge:857442289290969098>')
        
    @commands.command()
    async def randomfact(self, ctx):
        """
        Get a random fact :wink:
        """
        await ctx.message.delete()
        await ctx.send('This command is unavaible for now!')
        return

        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                    await ctx.send(embed=embed)
    
    @commands.command()
    async def reverse(self, ctx, *, msg:str):
        """ffuts esreveR"""
        await ctx.send(embed = discord.Embed(description = msg[::-1]).set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url))
    
    @commands.command(aliases=["roll"])
    async def rolldice(self, ctx):
        """Roll some die 🎲"""
        embed = discord.Embed(title = "<a:DH_dice:916644881038966794> Dice Roll", color = discord.Color.random())
        embed.set_author(name = f"{ctx.author.name}'s dice roll", icon_url = ctx.author.avatar_url)
        roll = random.randint(1, 6)
        if roll > 3:
            emoji = "<:tj_PandaSwag:906348241883389972>"
        elif roll < 4:
            emoji = "<a:tj_sipSpin:916514476306604103>"
        
        embed.description = f"{emoji} You rolled a **{roll}**!"
        await ctx.send(embed = embed)
    
    @commands.command(aliases=["epicgamerrate"])
    async def epikgamerrate(self, ctx):
        """
        <:tj_DiamondSword:916648979415060480> See how much of an epic gamer you are!
        """
        embed = discord.Embed(title = "<:tj_wicked:916514500788752385> Epic Gamer Rate", color = discord.Color.random())
        embed.set_author(name = f"{ctx.author.name}", icon_url = ctx.author.avatar_url)
        roll = random.randint(1, 100)
        if roll > 90:
            emoji = "<:tj_DiamondSword:916648979415060480>"
        elif roll < 90:
            emoji = "<:tj_tfShrug:916649124764463114>"
        
        embed.description = f"{emoji} You're a **{roll}%** epic gamer!"
        await ctx.send(embed = embed)
    
    @commands.command(aliases=["cheers", "drink"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beer(self, ctx, member: discord.Member = None):
        """
        :beers: Drink some alcohol with your friends!
        """
        vote = await self.dblpy.get_user_vote(ctx.author.id)
        if not vote:
            await ctx.send(embed = self.panther.vote_embed)
            return
        if member == self.panther.user:
            await ctx.send('yes I drink beer with you :beer:')
            return
        if member == ctx.author:
            await ctx.send('you can\'t have beer with ur self idiot ;-;')
            return
        
        components = [
            Button(emoji = "🍺", custom_id = "beer", style = ButtonStyle.green)
        ]
        
        m = await ctx.send(
            f"{member.mention} {ctx.author.name}#{ctx.author.discriminator} has invited you to have beer!\nClick the green button to accept the invitation!",
            components = components
        )
        
        while True:
            try:
                interaction = await self.panther.wait_for("button_click", check = lambda inter: inter.user == member and inter.custom_id == "beer", timeout = 45.0)
            except asyncio.TimeoutError:
                for row in components:
                    row.disable_components()

                await m.edit(components=components)

                await ctx.send('I guess you didn\'t want to drink a beer ;-;')
                return
            else:
                await ctx.send(f"<a:cheers:916703398680748052> {member.mention} and {ctx.author.mention} are enjoying a lovely beer!")
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def exit(self, ctx):
        """
        Exit the chat when you're exposed <:tj_Exit:855735159549984808>
        """
        em = discord.Embed(description = f"{ctx.author.mention} has left the chat... <:tj_Exit:855735159549984808>", color = discord.Color.from_rgb(255,0,0))
        await ctx.message.delete()
        await ctx.send(embed = em)
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def enter(self, ctx):
        """
        Want to enter the chat? :eyes:
        """
        em = discord.Embed(description = f"{ctx.author.mention} has entered the chat <:tj_enter:912555956028702741>", color = discord.Color.from_rgb(10,245,0))
        await ctx.message.delete()
        await ctx.send(embed = em)
    
    @commands.command(aliases=['rockpaperscissors'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.default,wait=False)
    async def rps(self, ctx):
        """Go old school and play some rock paper scissors :sunglasses:"""
        def check_win(p, b):
            if p == '🌑':
                return False if b == '📄' else True
            if p == '📄':
                return False if b == '✂' else True
            # p=='✂'
            return False if b == '🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors!**:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.panther.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
        try:
            reaction, _ = await self.panther.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**Your Choice:\t{reaction.emoji}\nMy Choice:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**You win :sparkles:**")
            else:
                await ctx.send("**I win :robot:**")

    @commands.command(help="Check your brain size!", aliases=['brain', 'iq'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def brainsize(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        iq = random.randint(-200, 110)
        embed = discord.Embed(
            title="🧠 Your IQ",
            description=f"**{user.name}#{user.discriminator}** has an IQ of **{iq}**",
            color=discord.Color.random()
        )

        m = await ctx.reply("Calculating IQ...")
        await asyncio.sleep(0.5)
        await m.edit(content="", embed=embed)

    @commands.command(aliases=["tod"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def truthordare(self, ctx):
        s = random.choice(["truth", "dare"])
        if s == "truth":
            truth_is_always_painful = random.choice([
                "When was the last time you lied?",
                "When was the last time you cried?",
                "What's your biggest fear?",
                "What's your biggest fantasy?",
                "Do you have any fetishes?",
                "What's something you're glad your mum doesn't know about you?",
                "Have you ever cheated on someone?",
                "What's the worst thing you've ever done?",
                "What's a secret you've never told anyone?",
                "Do you have a hidden talent?",
                "Who was your first celebrity crush?",
                "What are your thoughts on polyamory?",
                "What's the worst intimate experience you've ever had?",
                "Have you ever cheated in an exam?",
                "What's the most drunk you've ever been?",
                "Have you ever broken the law?",
                "What's the most embarrassing thing you've ever done?",
                "What's your biggest insecurity?",
                "What's the biggest mistake you've ever made?",
                "What's the most disgusting thing you've ever done?",
                "Who would you like to kiss in this room?",
                "What's the worst thing anyone's ever done to you?",
                "Have you ever had a run in with the law?",
                "What's your worst habit?",
                "What's the worst thing you've ever said to anyone?",
                "Have you ever peed in the shower?",
                "What's the strangest dream you've had?",
                "Have you ever been caught doing something you shouldn't have?",
                "What's the worst date you've been on?",
                "What's your biggest regret?",
                "What's the biggest misconception about you?",
                "Where's the weirdest place you've had sex?",
                "Why did your last relationship break down?",
                "Have you ever lied to get out of a bad date?",
                "What's the most trouble you've been in?"
            ])
        
            await ctx.send(embed = discord.Embed(title = "<a:tj_sussy:916525525357441094> Truth", description = truth_is_always_painful, color = discord.Color.blurple()).set_footer(text = "The truth is often painful 😔", icon_url = ctx.author.avatar_url))
        
        else:
            dare_is_more_and_always_painful = random.choice([
                "Show the most embarrassing photo on your phone",
                "Show the last five people you texted and what the messages said",
                "Let the rest of the group DM someone from your Instagram account",
                "Eat a raw piece of garlic",
                "Do 100 squats",
                "Keep three ice cubes in your mouth until they melt",
                "Say something dirty to the person on your left",
                "Give a foot massage to the person on your right",
                "Put 10 different available liquids into a cup and drink it",
                "Yell out the first word that comes to your mind",
                "Give a lap dance to someone of your choice",
                "Remove four items of clothing",
                "Like the first 15 posts on your Facebook newsfeed",
                "Eat a spoonful of mustard",
                "Keep your eyes closed until it's your go again",
                "Send a sext to the last person in your phonebook",
                "Show off your orgasm face",
                "Seductively eat a banana",
                "Empty out your wallet/purse and show everyone what's inside",
                "Do your best sexy crawl",
                "Pretend to be the person to your right for 10 minutes",
                "Eat a snack without using your hands",
                "Say two honest things about everyone else in the group",
                "Twerk for a minute",
                "Try and make the group laugh as quickly as possible",
                "Try to put your whole fist in your mouth",
                "Tell everyone an embarrassing story about yourself",
                "Try to lick your elbow",
                "Post the oldest selfie on your phone on Instagram Stories",
                "Tell the saddest story you know",
                "Howl like a wolf for two minutes",
                "Dance without music for two minutes",
                "Pole dance with an imaginary pole",
                "Let someone else tickle you and try not to laugh",
                "Put as many snacks into your mouth at once as you can"
            ])

            await ctx.send(embed = discord.Embed(title = "<:evilrondo:920185315182903326> Dare", description = dare_is_more_and_always_painful, color = discord.Color.blurple()).set_footer(text = "The dare is often more painful 💀", icon_url = ctx.author.avatar_url))

    @commands.command(description="Convert text to binary00101001")
    @commands.guild_only()
    async def binary(self, ctx, *, text):
        res = "".join(format(i, "b") for i in bytearray(text, encoding="utf-8"))
        embed = discord.Embed(title="Text To Binary", color=self.bot.main_color)
        embed.add_field(name="Normal Text:", value=text, inline=False)
        embed.add_field(name="Binary Text:", value=f"`{str(res)}`", inline=False)
        embed.set_footer(
            text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)

def setup(panther):
    panther.add_cog(Fun(panther))