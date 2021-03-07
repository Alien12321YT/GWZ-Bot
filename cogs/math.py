from discord.ext import commands
import discord
import random
import json
import os

class Math(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def add(self,ctx,*args):
        num = 0
        for arg in args:
            num += int(arg)
        coolstr = f'{args[0]}'
        for arg in args[1:]:
            coolstr += f' + {arg} '
        coolstr += f'= {num}'
        await ctx.send(coolstr)
    
    @commands.command(aliases=['sub'])
    async def subtract(self,ctx,*args):
        if len(args) >= 2:
            num = int(args[0])
            for i in args[1:]:
                num -= int(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' - {arg} '
            coolstr += f'= {num}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(aliases=['mult'])
    async def multiply(self,ctx,*args):
        if len(args) >= 2:
            num = int(args[0])
            for i in args[1:]:
                num *= int(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' × {arg} '
            coolstr += f'= {num}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))

    @commands.command(aliases=['div'])
    async def divide(self,ctx,*args):
        if len(args) >= 2:
            num = int(args[0])
            for i in args[1:]:
                num /= int(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' ÷ {arg} '
            coolstr += f'= {num}'
            await ctx.send(coolstr)
        elif len(args) == 1:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(aliases=['modu'])
    async def modulo(self,ctx,*args):
        if len(args) == 2:
            num = int(args[0])
            for i in args[1:]:
                num %= int(i)
            coolstr = f'{args[0]}'
            for arg in args[1:]:
                coolstr += f' % {arg} '
            coolstr += f'= {num}'
            await ctx.send(coolstr)
        else:
            ctx.send(embed=discord.Embed(title='Error!',color=0xff0000))
    
    @commands.command(aliases=['prime'])    
    async def isprime(self,ctx,num):
        if num > 1:
            for i in range(2,num):
                if (num % i) == 0:
                    await ctx.send(f"{num} is not a prime number")
                    await ctx.send(f'{i} times {num//i} is {num}')
                    break
            else:
                await ctx.send(f"{num} is a prime number")
    
    @commands.command(aliases=['rand'])
    async def random(self,ctx,min:int=1,max:int=100):
        await ctx.send(str(random.randint(min,max)))

def setup(bot):
    bot.add_cog(Math(bot))