import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
import praw

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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def kill(self, ctx, member: discord.Member=None):
        if member == None:
            await ctx.send("Mention someone to kill.")
            return
        if member == ctx.author:
            await ctx.send("Why would you kill yourself?")
            return

        kill_messages = [f'{member.name} died but nobody knows how',f'{member.name} died because God wanted them to die',f'{member.name} got killed by {ctx.author.name}',f'{member.name} died because {ctx.author.name} used the kill command',f'{member.name} drowned',f'{member.name}\'s :eggplant: became so hard that they literally died',f'{member.name} died because of smoking. Imagine smoking, that noob',f'{member.name} drank alcohol in dank memer, but instead of dying in the currency system, they somehow died irl',f'{member.name} died by std',f'{member.name} faps 69 times',f'{member.name} tried to swim in lava',f'{member.name} fell from a high place',f'{member.name} got cock and ball tortured which is a sexual activity involving application of pain or constriction to the male genitals. This may involve directly painful activities, such as wax play, genital spanking, squeezing, ball-busting, genital flogging, urethral play, tickle torture, erotic electrostimulation or even kicking.[1] The recipient of such activities may receive direct physical pleasure via masochism, or emotional pleasure through erotic humiliation, or knowledge that the play is pleasing to a sadistic dominant. Many of these practices carry significant health risks',f'{member.name} got killed by a llama','Killing someone is not good, and i\'m a good person so i won\'t kill anyone',f'{member.name} is a good person. I won\'t let anyone kill them',f'{member.name} got hit by a car',f'{member.name} got shooted by {ctx.author.name}',f'{member.name} lives in a hot place. They went to Oymyakon and died because of the cold',f'{ctx.author.name} punches {member.name} very hard in the :eggplant:',f'{member.name} tries to kill {ctx.author.name} but {ctx.author.name} pulls the reverse card',f'A bee kills {ctx.author.name}'f'{member.name} gets killed by uh... idk i ran out ofdeath messages so i\'m adding these random stuff',f'{member.name} saw a very hot woman she was so hot that {member.name} burned to death',f'ok i killed {member.name}']

        random_choice = random.choice(kill_messages)

        await ctx.send(random_choice)

    @commands.command(name='emojify')
    async def emojify_command(self,ctx,*,msg:str=None):
        result = ''
        if msg != None:
            for letter in list(msg):
                letter = letter.lower()
                if letter == 'a':
                    result += ':regional_indicator_a: '
                elif letter == 'b':
                    result += ':regional_indicator_b: '
                elif letter == 'c':
                    result += ':regional_indicator_c: '
                elif letter == 'd':
                    result += ':regional_indicator_d: '
                elif letter == 'e':
                    result += ':regional_indicator_e: '
                elif letter == 'f':
                    result += ':regional_indicator_f: '
                elif letter == 'g':
                    result += ':regional_indicator_g: '
                elif letter == 'h':
                    result += ':regional_indicator_h: '
                elif letter == 'i':
                    result += ':regional_indicator_i: '
                elif letter == 'j':
                    result += ':regional_indicator_j: '
                elif letter == 'k':
                    result += ':regional_indicator_k: '
                elif letter == 'l':
                    result += ':regional_indicator_l: '
                elif letter == 'm':
                    result += ':regional_indicator_m: '
                elif letter == 'n':
                    result += ':regional_indicator_n: '
                elif letter == 'o':
                    result += ':regional_indicator_o: '
                elif letter == 'p':
                    result += ':regional_indicator_p: '
                elif letter == 'q':
                    result += ':regional_indicator_q: '
                elif letter == 'r':
                    result += ':regional_indicator_r: '
                elif letter == 's':
                    result += ':regional_indicator_s: '
                elif letter == 't':
                    result += ':regional_indicator_t: '
                elif letter == 'u':
                    result += ':regional_indicator_u: '
                elif letter == 'v':
                    result += ':regional_indicator_v: '
                elif letter == 'w':
                    result += ':regional_indicator_w: '
                elif letter == 'x':
                    result += ':regional_indicator_x: '
                elif letter == 'y':
                    result += ':regional_indicator_y: '
                elif letter == 'z':
                    result += ':regional_indicator_z: '
                elif letter == ' ':
                    result += '    '
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

def setup(bot):
    bot.add_cog(fun(bot))