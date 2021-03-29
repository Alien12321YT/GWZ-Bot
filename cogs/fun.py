import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
import datetime
import json
import os

def convert_unix_timestamp(time):
    return datetime.datetime.fromtimestamp(int(time//1000)).strftime('%b %d, %Y | %I:%M %p')

def true_rank(rank):
    if rank == "NORMAL":
        return 'No rank'
    elif rank == "VIP":
        return 'VIP'
    elif rank == "VIP_PLUS":
        return 'VIP+'
    elif rank == "MVP":
        return 'MVP'
    elif rank == "MVP_PLUS":
        return 'MVP+'
    elif rank == "MVP_PLUS_PLUS" or rank == "SUPERSTAR":
        return 'MVP++'
    else:
        return 'No rank'

def isnt_ff_server(ctx):
    with open('server.json','r') as f:
        checkifffmode = json.load(f)
    return not checkifffmode[str(ctx.guild.id)]['ff_mode']

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def eightball(self, ctx,*,question=None):
        if question != None:
            result = random.choice(['Yes.','No.','Probably','Probably no','Never'])
            await ctx.send(result)
        else:
            await ctx.send('Try again, but this time ask a question for me to reply with stuff like yes or no')

    @commands.command(name='pp')
    @commands.check(isnt_ff_server)
    async def pee_pee(self, ctx,member: discord.Member=None):
        if member == None:
            member = ctx.author
        pp_size = random.randint(0,30)
        pp_middle_part = '=' * pp_size
        full_pp = str('8{}D'.format(pp_middle_part))
        embed = discord.Embed(
            title = '{}\'s pp'.format(member.name),
            description = full_pp,
            color =0xfefefe
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 2, BucketType.user)
    async def kill(self, ctx, member: discord.Member=None):
        if member == None:
            await ctx.send("Mention someone to kill.")
            return
        if member == ctx.author:
            await ctx.send("Why would you kill yourself?")
            return

        kill_messages = [f'{member.name} died but nobody knows how',f'{member.name} died because God wanted them to die',f'{member.name} got killed by {ctx.author.name}',f'{member.name} died because {ctx.author.name} used the kill command',f'{member.name} drowned',f'{member.name} died because of smoking. Imagine smoking, that noob',f'{member.name} drank alcohol in dank memer, but instead of dying in the currency system, they somehow died irl',f'{member.name} died by std',f'{member.name} faps 69 times',f'{member.name} tried to swim in lava',f'{member.name} fell from a high place',f'{member.name} got killed by a llama','Killing someone is not good, and i\'m a good person so i won\'t kill anyone',f'{member.name} is a good person. I won\'t let anyone kill them',f'{member.name} got hit by a car',f'{member.name} got shooted by {ctx.author.name}',f'{member.name} lives in a hot place. They went to Oymyakon and died because of the cold',f'{member.name} tries to kill {ctx.author.name} but {ctx.author.name} pulls the reverse card',f'A bee kills {member.name}',f'ok i killed {member.name}',f'{member.name} found the nearest rope']

        if isnt_ff_server(ctx):
            kill_messages += [f'{member.name}\'s :eggplant: became so hard that they literally died',f'{member.name} got cock and ball tortured which is a sexual activity involving application of pain or constriction to the male genitals. This may involve directly painful activities, such as wax play, genital spanking, squeezing, ball-busting, genital flogging, urethral play, tickle torture, erotic electrostimulation or even kicking.[1] The recipient of such activities may receive direct physical pleasure via masochism, or emotional pleasure through erotic humiliation, or knowledge that the play is pleasing to a sadistic dominant. Many of these practices carry significant health risks',f'{ctx.author.name} punches {member.name} very hard in the :eggplant:',f'{member.name} saw a very hot woman she was so hot that {member.name} burned to death',f'{member.name} cummed so much he drowned in it']
        if ctx.author.guild_permissions.ban_members:
            kill_messages.append(f'{member.name} got banned by {ctx.author.name}')
            kill_messages.append('A player has been banned for hacking or abuse. **Thanks for reporting it!**')
        if member.guild_permissions.ban_members:
            kill_messages.append(f'{member.name} tried to ban {ctx.author.name}, but {ctx.author.name} had an uno-reverse-card')
        if member.is_on_mobile():
            kill_messages.append(f'{member.name} was hacked by {ctx.author.name} due to his stoopid phone security. Just use a computer man')

        random_choice = random.choice(kill_messages)

        await ctx.send(random_choice)

    @commands.command(name='emojify')
    async def emojify_command(self,ctx,*,msg:str=None):
        result = ''
        if msg != None:
            for letter in list(msg):
                use_emojis = True
                code_bracket_for_emoji = False
                letter = letter.lower()
                if letter == 'a' and use_emojis:
                    result += ':regional_indicator_a: '
                elif letter == 'b' and use_emojis == True:
                    result += ':regional_indicator_b: '
                elif letter == 'c' and use_emojis == True:
                    result += ':regional_indicator_c: '
                elif letter == 'd' and use_emojis == True:
                    result += ':regional_indicator_d: '
                elif letter == 'e' and use_emojis == True:
                    result += ':regional_indicator_e: '
                elif letter == 'f' and use_emojis == True:
                    result += ':regional_indicator_f: '
                elif letter == 'g' and use_emojis == True:
                    result += ':regional_indicator_g: '
                elif letter == 'h' and use_emojis == True:
                    result += ':regional_indicator_h: '
                elif letter == 'i' and use_emojis == True:
                    result += ':regional_indicator_i: '
                elif letter == 'j' and use_emojis == True:
                    result += ':regional_indicator_j: '
                elif letter == 'k' and use_emojis == True:
                    result += ':regional_indicator_k: '
                elif letter == 'l' and use_emojis == True:
                    result += ':regional_indicator_l: '
                elif letter == 'm' and use_emojis == True:
                    result += ':regional_indicator_m: '
                elif letter == 'n' and use_emojis == True:
                    result += ':regional_indicator_n: '
                elif letter == 'o' and use_emojis == True:
                    result += ':regional_indicator_o: '
                elif letter == 'p' and use_emojis == True:
                    result += ':regional_indicator_p: '
                elif letter == 'q' and use_emojis == True:
                    result += ':regional_indicator_q: '
                elif letter == 'r' and use_emojis == True:
                    result += ':regional_indicator_r: '
                elif letter == 's' and use_emojis == True:
                    result += ':regional_indicator_s: '
                elif letter == 't' and use_emojis == True:
                    result += ':regional_indicator_t: '
                elif letter == 'u' and use_emojis == True:
                    result += ':regional_indicator_u: '
                elif letter == 'v' and use_emojis == True:
                    result += ':regional_indicator_v: '
                elif letter == 'w' and use_emojis == True:
                    result += ':regional_indicator_w: '
                elif letter == 'x' and use_emojis == True:
                    result += ':regional_indicator_x: '
                elif letter == 'y' and use_emojis == True:
                    result += ':regional_indicator_y: '
                elif letter == 'z' and use_emojis == True:
                    result += ':regional_indicator_z: '
                elif letter == '1' and use_emojis == True:
                    result += ':one:'
                elif letter == '2' and use_emojis == True:
                    result += ':two:'
                elif letter == '3' and use_emojis == True:
                    result += ':three:'
                elif letter == '4' and use_emojis == True:
                    result += ':four:'
                elif letter == '5' and use_emojis == True:
                    result += ':five:'
                elif letter == '6' and use_emojis == True:
                    result += ':six:'
                elif letter == '7' and use_emojis == True:
                    result += ':seven:'
                elif letter == '8' and use_emojis == True:
                    result += ':eight:'
                elif letter == '9' and use_emojis == True:
                    result += ':nine:'
                elif letter == '0' and use_emojis == True:
                    result += ':zero:'
                elif letter == ' ' and use_emojis == True:
                    result += '    '
                elif (letter == '<') and use_emojis == True:
                    result += '<'
                    code_bracket_for_emoji = True
                    use_emojis = False
                elif letter == '>' and use_emojis == False:
                    result += '>'
                    code_bracket_for_emoji = False
                    use_emojis = True
                elif letter == '`' or letter == ':':
                    result += letter
                    if use_emojis == True:
                        if code_bracket_for_emoji:
                            pass
                        else:
                            use_emojis = False
                    else:
                        use_emojis = False
                elif letter == '\\':
                    result += '\\'
                else:
                    result += str(letter)
            await ctx.send(result)
        else:
            await ctx.send('You didn\'t give me a valid string for `msg`!')
    
    @commands.command(name='powerof2',aliases=['po2'])
    async def po2_command(self,ctx):
        await ctx.send(str(2**random.randint(0,63)))
    
    @commands.command(name='reverse')
    async def reverse_c(self,ctx,*,msg:str=None):
        if msg == None:
            await ctx.send('​')
        else:
            await ctx.send(str(msg[::-1]))

    @commands.command()
    async def tim(self,ctx):
        await ctx.send('t i m')
    
    @commands.command(aliases=['urbandictionary'])
    async def urban(self, ctx, word=None):
        if word == None:
            await ctx.send(
                "Mention a word. If you want to mention two or more words then don't give any space between the words"
            )
            return
        else:
            await ctx.send(f"https://urbandictionary.com/{word}")


def setup(bot):
    bot.add_cog(fun(bot))