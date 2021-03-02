import discord
from discord.ext import commands

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx,num=1):
            channel = ctx.channel
            num += 1
            await channel.purge(limit=int(num))

def setup(bot):
    bot.add_cog(moderation(bot))