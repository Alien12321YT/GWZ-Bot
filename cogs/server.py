import discord
from discord.ext import commands

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nuke(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=2147483647)
            await ctx.send('Nuked this channel')
            await ctx.send('https://tenor.com/view/explosion-mushroom-cloud-atomic-bomb-bomb-boom-gif-4464831')
    
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def deletechannel(self, ctx, channel: discord.TextChannel):
        embed = discord.Embed(
            title = 'Success',
            description = f'Channel: {channel} has been deleted.',
            color=ctx.author.ccolor
        )
        await ctx.send(embed=embed)
        await channel.delete()

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def createchannel(self, ctx, channelName):
        guild = ctx.guild

        embed = discord.Embed(
            title = 'Success',
            description = "{} has been successfully created.".format(channelName),
            color=ctx.author.color
        )
        await guild.create_text_channel(name='{}'.format(channelName))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(server(bot))