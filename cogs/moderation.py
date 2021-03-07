import discord
from discord.ext import commands
import datetime

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx,num=1):
            channel = ctx.channel
            num += 1
            await channel.purge(limit=int(num))
    
    @commands.command(aliases=['time','clock'])
    async def currenttime(self,ctx):
        await ctx.send(datetime.datetime.now().strftime('**%b %d, %Y** | *%I:%M:%S %p GMT* | Day #%j/365'))

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def slowmode(self,ctx,delay_in_sec,channel:discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        if delay_in_sec == 'off' or delay_in_sec == 'none':
            delay_in_sec = 0
        await channel.edit(slowmode_delay=delay_in_sec)
        await ctx.channel.send(f'{channel.mention} now has {delay_in_sec} seconds of slowmode.')
    

def setup(bot):
    bot.add_cog(moderation(bot))