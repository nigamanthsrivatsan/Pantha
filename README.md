<h1 style="text-align: center;"> Pantha </h1>
<a href="https://github.com/nigamanthsrivatsan/Pantha/blob/main/LICENSE"><img style="display: inline-block;" alt="License for the project" src="https://img.shields.io/github/license/nigamanthsrivatsan/Pantha?style=for-the-badge"></a>
<a href="https://github.com/nigamanthsrivatsan/Pantha/stargazers"><img style="display: inline-block;" alt="GitHub stars" src="https://img.shields.io/github/stars/nigamanthsrivatsan/Pantha?style=for-the-badge"></a> 
<img style="display: inline-block;" alt="GitHub forks" src="https://img.shields.io/github/forks/nigamanthsrivatsan/Pantha?style=for-the-badge">

<p style="text-align: center;"> Welcome to Pantha, a moderation, fun, utility and <b> completely open source </b> discord bot for your server! <br>
  Emojis for the bot can be found at <a href="https://discord.gg/thejedi"> this link </a>. </p>

## Why do I self-host this bot?

Why Pantha? We have these features: (and over **100** commands in total)

📑 **Info:** `p.ping`, `p.snipe`, `p.wi` and **7** more informational commands. <br>
🎈 **Fun:** `p.randomfact`, `p.beer`, `p.rps`, `p.truthordare` and **10** more fun commands.  <br> 
⚙️ **Error Handling:** full fleged error handling for the bot, a big bot, big error handling. <br>
🛡️ **Anti-Spam Protection:** The bot doesn't join servers with below 50 members as many tasks are running for each server that the bot is in, thus to reduce the pressure on our hosting we don't like joining random servers.  <br> 
👑 **Owner:** `p.load`, `p.unload`, `p.cleartickets`, `p.toggle`: Disabling/enabling commands and **5+** more owner restricted commands. <br> 
📝 **Patch Notes:** Using the bot to post it's own updates? <br>
🔨 **Moderation** `p.slowmode`, `p.lock`, `p.unlock`, `p.kick`, `p.ban` and **5** more foolproof moderation commands. <br> 
🐸 **Dank Memer Assistant:** A perfect assistant for Dank Memer: banning people who leave your server after a giveaway/heist event, showing the rules of the bot.  <br> 
🎉 **Giveaways:** Giveaways for your discord server (with buttons). <br> 
⭐ **Utilities:** `p.poll`, `p.choose`, `p.embed`, `p.coinflip` and **5** more utility commands. <br>
📫 **Suggestions:** Users can suggest what they want to you.  <br>

## Self-Hosting 🚀

**You will require Python to do the following:** 

```bash
$ git clone https://github.com/nigamanthsrivatsan/Pantha.git
# or if you have the github cli
$ gh repo clone nigamanthsrivatsan/Pantha
$ cd Pantha

# now we install the modules
$ pip install -r requirements.txt 
```

Now we edit the "config.json" file in the main directory. 🤔

```json
{
    "token" : "yourTokenHere",
    "toptoken" : "",
    "owner" : "123456789",
    "botId" : "123456789",
    "syncban" : [12345678, 12345678] 
}
```

### Fields

The bot token should be there, the topToken is not required, only enter it if you want the bot to be on top.gg.
There can only be one owner of the bot and their id must be in a string, the bot's ID must also be put in. 

The field "syncban" is the servers that the bot should ban when the owner initiates a "syncban". 
The feature bans a user in all the servers that you put as long as:

* The bot is in the server.
* The bot has adequate permissions to do so. 

This is useful for banning someone across guilds (TOS breakers, scammers, etc).
And now that we have everything customized, we're ready to go! 🚀

```bash
# and start the bot 
$ python main.py
```

## :clap:  Supporters
[![Stargazers repo roster for @nigamanthsrivatsan/Pantha](https://reporoster.com/stars/nigamanthsrivatsan/Pantha)](https://github.com/nigamanthsrivatsan/Pantha/stargazers)
[![Forkers repo roster for @nigamanthsrivatsan/Pantha](https://reporoster.com/forks/nigamanthsrivatsan/Pantha)](https://github.com/nigamanthsrivatsan/Pantha/network/members)
<br/>

## Contributing

Feel free to open any Issues or Pull Requests that come along your way. 
I'm still learning discord.py and Python and would require help to make this project truly awesome!

