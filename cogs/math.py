from discord.ext import commands
import discord
import random
import math

class Math(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def add(self,ctx,*args):
        num = 0
        for arg in args:
            num += float(arg)
        coolstr = f'{args[0]}'
        for arg in args[1:]:
            coolstr += f' + {arg} '
        coolstr += f'= {round(num,3)}'
        await ctx.send(coolstr)
    
    @commands.command(aliases=['sub'])
    async def subtract(self,ctx,*args):
        if len(args) >= 2:
            num = float(args[0])
            for i in args[1:]:
                num -= float(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' - {arg} '
            coolstr += f'= {round(num,3)}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(aliases=['mult'])
    async def multiply(self,ctx,*args):
        if len(args) >= 2:
            num = float(args[0])
            for i in args[1:]:
                num *= float(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' × {arg} '
            coolstr += f'= {round(num,3)}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))

    @commands.command(aliases=['div'])
    async def divide(self,ctx,*args):
        if len(args) >= 2:
            num = float(args[0])
            for i in args[1:]:
                num /= float(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' ÷ {arg} '
            coolstr += f'= {round(num,3)}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(aliases=['remainder','rem','modu'])
    async def modulo(self,ctx,*args):
        if len(args) == 2:
            num = float(args[0])
            for i in args[1:]:
                num %= float(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' % {arg} '
            coolstr += f'= {round(num,3)}'
            await ctx.send(coolstr)
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(aliases=['prime'])    
    async def isprime(self,ctx,num:int):
        if num > 1:
            for i in range(2,num):
                if (num % i) == 0:
                    await ctx.send(f"{num} is not a prime number")
                    await ctx.send(f'{i} times {num//i} is {num}')
                    break
            else:
                await ctx.send(f"{num} is a prime number")
    
    @commands.command(aliases=['randnum','randomnum','randnumber','rand']) 
    async def randomnumber(self, ctx, x:int, y:int,repr:str=None):
        res = 0
        if x < y:
            res = random.randint(x,y)
        elif x > y:
            res = random.randint(y,x)
        else:
            await ctx.send(f'Error! Don\'t make the range equal, or else your random number is just {x}...')
            res = 69420
            return
        if repr == 'b':
            res = str(bin(res))[1:]
        elif repr == 'o':
            res = str(oct(res))[1:]
        elif repr == 'd':
            res = str(int(res))
        elif repr == 'x' or repr == 'h':
            res = str(hex(res))[1:]
        else:
            pass
        await ctx.send(res)

    @commands.command(aliases=['sqrt'])
    async def squareroot(self,ctx,num:int=None):
        if num != None:
            await ctx.send(f'\u221A{num} = {str(round(math.sqrt(num),4))}')
        else:
            await ctx.send(f'You didn\'t give me a number?')


    @commands.command(aliases=['pow'])
    async def power(self,ctx,*args):
        if len(args) >= 2:
            if len(args) > 6:
                await ctx.send('Too many numbers to count! You should put less than 4 numbers to raise, or else you could crash the bot faster than the web server would.')
            num = float(args[0])
            for i in args[1:]:
                num **= float(i)
                if len(str(num)) > 1024:
                    await ctx.send('Number was too big! The expected result was more than 1024 digits, which would flood chat faster than <@!718109447825915946>\'s spambot would.')
                    break
                    return
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f'^{arg}'
            coolstr += f'= {round(num,4)}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(name='repr')
    async def repr_command_just_in_case_this_has_a_name_i_am_adding_more_words_so_it_doesnt_match_at_all_to_any_other_built_in_functions_like__init__like_tommy_innit_hahaha(self,ctx,num:int,repr:str='d',char:str='n'):
        res = num
        enc = ''
        char_ = ''
        if repr == 'b':
            res = str(bin(res))[1:]
            enc = 'binary'
        elif repr == 'o':
            res = str(oct(res))[1:]
            enc = 'octal'
        elif repr == 'd':
            res = str(int(res))
            enc = 'decimal'
        elif repr == 'x' or repr == 'h':
            res = str(hex(res))[1:]
            enc = 'hexadecimal'
        else:
            pass
        if char == 'n':
            await ctx.send(f'{num} encoded in {enc} = {res}')
        else:
            char_ = chr(num)
            await ctx.send(f'{num} encoded in {enc} = {res} = {char_}')
    

def setup(bot):
    bot.add_cog(Math(bot))
