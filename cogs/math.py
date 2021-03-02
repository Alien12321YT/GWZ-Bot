import discord
from discord.ext import commands
import math
import random

class math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['add'])
    async def addition(self, ctx, x: float, y: float):
        res = x + y
        if str(res).endswith('.0'):
            res = round(res)
        await ctx.send(res)

    @commands.command(aliases=['sub'])
    async def subtract(self, ctx, x: float, y: float):
        res = x - y
        if str(res).endswith('.0'):
            res = round(res)
        await ctx.send(res)

    @commands.command(aliases=['mult'])
    async def multiply(self, ctx, x: float, y: float):
        res = round(x * y, 6)
        if str(res).endswith('.0'):
            res = round(res)
        await ctx.send(res)

    @commands.command(aliases=['div'])
    async def divide(self, ctx, x: float, y: float):
        res = round(x / y, 6)
        if str(res).endswith('.0'):
           res = round(res)
        await ctx.send(res)

    @commands.command(aliases=['rand'])
    async def randomnumber(self, ctx, x:int, y:int):
        await ctx.send(random.randint(x,y))

    @commands.command(aliases=['sqrt']) 
    async def squareroot(self, ctx, x: int):
        res = math.sqrt(x)
        if str(res).endswith('.0'):
            res = round(res)
        await ctx.send(res)
    
    @commands.command(aliases=['pow'])
    async def power(self, ctx,x:int,y:int):
        await ctx.send(x**y)

def setup(bot):
    bot.add_cog(math(bot))