import discord
from discord.ext import commands
import datetime
import os
from pingsux import up
import discord_slash as sdiscord

client = commands.Bot(command_prefix = '^')
slashclient = sdiscord.SlashCommand(client)
@client.remove_command("help")

@client.event
async def on_ready():
    print(f"Bot is ready. {client.user}")
    await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(
        type=discord.ActivityType.playing, name=f"^help | {len(client.guilds)} servers and {sum(guild.member_count for guild in client.guilds)} users"
    ))

@slashclient.slash(name='pingslash')
async def ping_c_slash(ctx:sdiscord.SlashContext):
    await ctx.send(f'Pong! {round(client.latency*1000,1)} ms')

@client.event
async def on_connect():
    print('Bot has connected to Discord poggggg!')

@client.event
async def on_disconnect():
    print('Bot has disconnected from Discord not-so poggggg!')

@client.event
async def on_command_error(ctx,exception):
  await ctx.send(str(exception))
  raise exception

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = "Help", description = "Use ^help <command> for extended information on a **command**.", color = ctx.author.color)

    embed.add_field(name = "Currency", value = "^help currency", inline = False)
    embed.add_field(name = "Fun", value = "^help fun", inline = False)
    embed.add_field(name = "Moderation", value = "^help moderation", inline = False)
    embed.add_field(name = "Math", value = "^help math", inline = False)
    embed.add_field(name = "Server", value = "^help server", inline = False)
    embed.add_field(name = "Other", value = "^help other", inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/797693868652363827/32ada26d274dc9cf8795e2b485a2785e.png?size=256")

    await ctx.send(embed=embed)
  
@client.command()
async def invite(ctx):
    link = ''
    if datetime.datetime.now().day == 1 and datetime.datetime.now().month == 4:
        link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    else:
        link = 'https://discord.com/api/oauth2/authorize?client_id=797693868652363827&permissions=2146959222&scope=bot'
    description = f'Click [here]({link}) to invite me to your server!'
    embed = discord.Embed(
        title='Invite me!',
        description=description,
        color=0xfefefe
    ) 
    await ctx.send(embed=embed)

@client.command(name='ping')
async def ping_c(ctx,brrr:str='false'):
    if str(brrr).lower() == 'true':
        await ctx.send(f'haha, ping go brrrrrrr! {round(client.latency*1000,1)} ms.')
    else:
        await ctx.send(f'Pong! {round(client.latency*1000,1)} ms')

def only_authors(ctx):
    return ctx.author.id == 718109447825915946 or ctx.author.id == 692250820741300266

@commands.check(only_authors)
@client.command()
async def servers(ctx):
        activeservers = client.guilds
        for guild in activeservers:
            await ctx.send(f"{guild.name}")

@commands.check(only_authors)
@client.command(name='copy')
async def copyme(ctx,*,thing:str):
    print(thing)
    print(ctx)
    await ctx.send(thing)

@client.command()
async def vote(ctx):
    embed = discord.Embed(
        title='Vote for this bot!',
        description='[Discord Boats](https://discord.boats/bot/797693868652363827/vote)\n[Discord Bot List](https://discordbotlist.com/bots/gwz-bot/upvote)\n[top.gg](https://top.gg/bot/797693868652363827/vote)',
        color=0xfefefe
    )
    await ctx.send(embed=embed)

@help.command()
async def currency(ctx):

    embed = discord.Embed(title = "Currency", description = "The currency system of this bot", color = ctx.author.color)

    embed.add_field(name = "Currency commands", value = "balance, inventory, withdraw, deposit, beg, give, shop, buy, sell, slots, guessnumber, countup")

    await ctx.send(embed=embed)

@help.command()
async def fun(ctx):
    embed = discord.Embed(title = "Fun", description = "Commands which are kinda fun", color = ctx.author.color)

    embed.add_field(name = "Fun commands", value = "8ball, pp, kill")

    await ctx.send(embed=embed)

@help.command()
async def moderation(ctx):
    embed = discord.Embed(title = "Moderation", description = "The moderation system", color = ctx.author.color)

    embed.add_field(name = "Moderation commands", value = "purge")

    await ctx.send(embed=embed)

@help.command()
async def math(ctx):
    embed = discord.Embed(title = "Math", description = "Basically a calculator", color = ctx.author.color)

    embed.add_field(name = "Math commands", value = "addition, subtract, multiply, divide, power, randomnumber, squareroot")

    await ctx.send(embed=embed)

@help.command()
async def server(ctx):
    embed = discord.Embed(title = "Server", description = "Manage your server", color = ctx.author.color)

    embed.add_field(name = "Server commands", value = "nuke, createchannel, deletechannel")

    await ctx.send(embed=embed)

@help.command()
async def other(ctx):
    embed = discord.Embed(title = "No Category", description = "Commands which don't really have a category.", color = ctx.author.color)

    embed.add_field(name = "No category commands", value = "invite, ping, vote")

    await ctx.send(embed=embed)

@help.command()
async def invite(ctx):
    embed = discord.Embed(title = "Invite", description = "Get the invite link of this bot.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^invite")

    await ctx.send(embed=embed)

@help.command()
async def ping(ctx):
    embed = discord.Embed(title = "Ping", description = "Shows the ping of the bot.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^ping")

    await ctx.send(embed=embed)

@help.command()
async def vote(ctx):
    embed = discord.Embed(title = "Vote", description = "Shows the vote links of the bot.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^vote")

    await ctx.send(embed=embed)

@help.command()
async def guessnumber(ctx):
    embed = discord.Embed(title = "Guessnumber", description = "Guess the number between 1 to 10. If your guess is wrong, you lose your bet and if your guess is correct, you win 7.5x your bet, you get a lot of money since it's not easy to win.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^guessnumber <amount to bet>")

    await ctx.send(embed=embed)

@help.command()
async def countup(ctx):
    embed = discord.Embed(title = "Countup", description = "Countup to 100 and you win 10k coins. You must be the one who counted up to 100. I actually can't explain correctly cuz my friend made this command not the real owner aka me.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^countup")

    await ctx.send(embed=embed)

@help.command()
async def kill(ctx):
    embed = discord.Embed(title = "Kill", description = "Kill someone with this command.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^kill <member>")

    await ctx.send(embed=embed)

@help.command(aliases=['bal'])
async def balance(ctx):
    embed = discord.Embed(title = "Balance", description = "Check your balance/how much money you have in the currency system.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^balance")
    embed.add_field(name = "**Aliases**", value = "bal")

    await ctx.send(embed=embed)

@help.command()
async def beg(ctx):
    embed = discord.Embed(title = "Beg", description = "Beg and earn some coins.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^beg")

    await ctx.send(embed=embed)

@help.command()
async def buy(ctx):
    embed = discord.Embed(title = "Buy", description = "Buy something from the shop if it's buyable.")

    embed.add_field(name = "**Syntax**", value = "^buy <item>")

    await ctx.send(embed=embed)

@help.command()
async def sell(ctx):
    embed = discord.Embed(title = "Sell", description = "Sell stuff and earn coins if the item is sellable.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^sell <item>")

    await ctx.send(embed=embed)

@help.command(aliases=['with'])
async def withdraw(ctx):
    embed = discord.Embed(title = "Withdraw", description = "Withdraw some coins from your bank.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^withdraw <amount>")
    embed.add_field(name = "**Aliases**", value = "with")

    await ctx.send(embed=embed)

@help.command(aliases=['dep'])
async def deposit(ctx):
    embed = discord.Embed(title = "Deposit", description = "Deposit some coins to your bank.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^deposit <amount>")
    embed.add_field(name = "**Aliases**", value = "dep")

    await ctx.send(embed=embed)

@help.command(aliases=['send'])
async def give(ctx):
    embed = discord.Embed(title = "Give", description = "Give some coins to someone else.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^give <member> <amount>")
    embed.add_field(name = "**Aliases**", value = "send")

    await ctx.send(embed=embed)

@help.command()
async def shop(ctx):
    embed = discord.Embed(title = "Shop", description = "See what items are there in the shop.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^shop")

    await ctx.send(embed=embed)

@help.command(aliases=['slot'])
async def slots(ctx):
    embed = discord.Embed(title = "Slots", description = "A slots system where you can win money. If all the three emojis are not same then you lose your bet. If all the three emojis are same then you win 2.5x your bet. Note: It's not that easy to win.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^slots <amount>")
    embed.add_field(name = "**Aliases**", value = "slot")

    await ctx.send(embed=embed)

@help.command(aliases=['8all'])
async def eightball(ctx):
    embed = discord.Embed(title = "8ball", description = "Ask a question and the bot will answer your question with stuff like yes or no.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^8ball <question>")

    await ctx.send(embed=embed)

@help.command()
async def pp(ctx):
    embed = discord.Embed(title = "PP", description = "Your imaginary pp size.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^pp")

    await ctx.send(embed=embed)

@help.command(aliases=['add'])
async def addition(ctx):
    embed = discord.Embed(title = "Addition", description = "Add two numbers e.g 2+2.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^addition <num1> <num2>")
    embed.add_field(name = "**Aliases**", value = "add")

    await ctx.send(embed=embed)

@help.command(aliases=['sub'])
async def subtract(ctx):
    embed = discord.Embed(title = "Subtract", description = "Subtract two numbers e.g 420-69.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^subtract <num1> <num2>")
    embed.add_field(name = "**Aliases**", value = "sub")

    await ctx.send(embed=embed)

@help.command(aliases=['mult'])
async def multiply(ctx):
    embed = discord.Embed(title = "Multiply", description = "Multiply two numbers e.g 5*69.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^multiply <num1> <num2>")
    embed.add_field(name = "**Aliases**", value = "mult")

    await ctx.send(embed=embed)

@help.command(aliases=['div'])
async def divide(ctx):
    embed = discord.Embed(title = "Divide", description = "Divide two numbers e.g 666/33.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^divide <num1> <num2>")
    embed.add_field(name = "**Aliases**", value = "div")

    await ctx.send(embed=embed)

@help.command(aliases=['pow'])
async def power(ctx):
    embed = discord.Embed(title = "Power", description = "Just a math command which my English is too weak to explain e.g 5^5.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^power <num1> <num2>")
    embed.add_field(name = "**Aliases**", value = "pow")

    await ctx.send(embed=embed)

@help.command(aliases=['rand'])
async def randomnumber(ctx):
    embed = discord.Embed(title = "Randomnumber", description = "Find a random number between num1 and num2.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^randomnumber <num1> <num2>")
    embed.add_field(name = "**Aliases**", value = "rand")

    await ctx.send(embed=embed)

@help.command(aliases=['sqrt'])
async def squareroot(ctx):
    embed = discord.Embed(title = "Squareroot", description = "Squareroot a number.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^squareroot <num>")
    embed.add_field(name = "**Aliases**", value = "sqrt")

    await ctx.send(embed=embed)

@help.command()
async def purge(ctx):
    embed = discord.Embed(title = "Purge", description = "Delete messages in bulk.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^purge <amount of messages>")

    await ctx.send(embed=embed)

@help.command()
async def nuke(ctx):
    embed = discord.Embed(title = "Nuke", description = "Nuke a channel (May take a lot of time if there are a lot of messages or there are messages older than 14 days).", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^nuke")

    await ctx.send(embed=embed)

@help.command()
async def createchannel(ctx):
    embed = discord.Embed(title = "Createchanel", description = "Creates a text channel.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^createchannel <channel name>")

    await ctx.send(embed=embed)

@help.command()
async def deletechannel(ctx):
    embed = discord.Embed(title = "Deletechanel", description = "Deletes a text channel.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^deletechannel <channel name>")

    await ctx.send(embed=embed)

@help.command(aliases=['inv'])
async def inventory(ctx):
    embed = discord.Embed(title = "Inventory", description = "Check what items you have in your inventory.", color = ctx.author.color)

    embed.add_field(name = "**Syntax**", value = "^inventory <amount>")
    embed.add_field(name = "**Aliases**", value = "inv")

    await ctx.send(embed=embed)

extensions = ['cogs.currency','cogs.fun', 'cogs.math', 'cogs.moderation', 'cogs.server']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

up()
client.run(os.getenv('SUPER_SECRET_CODE')) 