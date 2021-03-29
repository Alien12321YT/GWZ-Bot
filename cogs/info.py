from discord.ext import commands
import discord
import requests
import datetime
import os
from discord.ext.commands.cooldowns import BucketType

class Server_Info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='member')
    async def member_get(self,ctx,id):
        member = ctx.guild.get_member(user_id=int(id))
        if member != None:
            await ctx.send(embed=discord.Embed(description='Member with ID: `{}` is {}'.format(member.id,member.mention)))
        else:
            await ctx.send(embed=discord.Embed(description='Member with ID: `{}` is not in {}!'.format(id,ctx.guild.name)))

    @commands.command(name='role')
    async def role_get(self,ctx,id):
        role = ctx.guild.get_role(role_id=int(id))
        if role != None:
            await ctx.send(embed=discord.Embed(description='Role with ID: `{}` is {}'.format(role.id,role.mention)))
        else:
            await ctx.send('Role with ID: `{}` is not a role in {}!'.format(id,ctx.guild.name))

    @commands.command(name='channel')
    async def channel_get(self,ctx,id):
        channel = ctx.guild.get_channel(id)
        if channel != None:
            await ctx.send(embed=discord.Embed(description='Channel with ID: `{}` is {}'.format(id,channel.mention)))
        else:
            await ctx.send('Channel with ID: `{}` is not a channel in {}!'.format(id,ctx.guild.name))

    @commands.command()
    async def memberinfo(self,ctx,member:discord.Member=None):
        if discord.Member != None:
            embed = discord.Embed(
                title='Member: **{}**'.format(member.display_name),
                color=ctx.author.color
            )
            embed.add_field(name='Real Username',value=member.name)
            embed.add_field(name='Account Creation Date',value=member.created_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='Guild Join Date',value=member.joined_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='ID',value=member.id)
            await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self,ctx,role:discord.Role=None):
            embed = discord.Embed(
                title='Role: **{}**'.format(role.name),
                color=ctx.author.color
            )
            embed.add_field(name='Name',value=role.mention)
            embed.add_field(name='Color',value='R: {}, G: {}, B: {}'.format(role.color.to_rgb()[0],role.color.to_rgb()[1],role.color.to_rgb()[2]))
            embed.add_field(name='Time Created',value=role.created_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='ID',value=str(role.id))
            await ctx.send(embed=embed)

    @commands.command(aliases=['serverinfo'])
    async def guildinfo(self,ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title='Server: **{}**'.format(guild.name),
            color=ctx.author.color
        )
        owner = guild.get_member(guild.owner_id)
        if owner != None:
            owner = owner.mention
        embed.add_field(name='Name',value=guild.name)
        embed.add_field(name='Owner',value=owner)
        embed.add_field(name='Members',value=str(guild.member_count))
        embed.add_field(name='Creation date',value=guild.created_at.strftime('%b %d, %Y | %I:%M %p'))
        embed.add_field(name='Number of channels',value=str(len(guild.channels)))
        if guild.rules_channel != None:
            embed.add_field(name='Rules Channel',value=guild.rules_channel.mention)
        embed.add_field(name='Large',value=str(guild.large))
        embed.add_field(name='ID',value=str(guild.id))
        await ctx.send(embed=embed)

    @commands.command()
    async def channelinfo(self,ctx,channel:discord.TextChannel=None):
            embed = discord.Embed(
                title='Channel: **{}**'.format(channel.name),
                color=ctx.author.color
            )
            embed.add_field(name='Name',value=channel.mention)
            embed.add_field(name='Time Created',value=channel.created_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='ID',value=str(channel.id))
            await ctx.send(embed=embed)

    @commands.cooldown(1,30,BucketType.guild)
    @commands.command(name='covid19',aliases=['covid','coronavirus','corona','covidinfo','covidi','cov','covinfo','covi'])
    async def covid_c(self,ctx):
        res_json = requests.get('https://covid19.mathdro.id/api').json()
        embed=discord.Embed(
            title='COVID-19 News <:covid:825411542223683645>',
            description='This is the latest COVID-19 statistics, brought to you by [mathdroid\'s covid-19-api](https://github.com/mathdroid/covid-19-api).',
            color=ctx.author.color
        )
        embed.add_field(name='Confirmed Cases',value=str(res_json['confirmed']['value']),inline=False)
        embed.add_field(name='Dead Cases',value=str(res_json['deaths']['value']),inline=False)
        tlupdtd = res_json['lastUpdate']
        embed.set_footer(text=f'Last updated: {tlupdtd}')
        await ctx.send(embed=embed)

    @commands.command(name='apod')
    @commands.cooldown(1,30,BucketType.guild)
    async def apod_c(self,ctx):
        apikey = os.getenv('NASA')
        date_ = datetime.datetime.now().strftime('%Y-%m-%d')
        parameters = {
            "api_key": apikey,
            "date": date_,
            "hd": True,
            "thumbs": True
        }
        res_json = requests.get('https://api.nasa.gov/planetary/apod',params=parameters).json()
        embed = discord.Embed(
            title=res_json['title'],
            description=res_json['explanation']+'\n\n[Go to the official APOD website to see!](https://apod.nasa.gov/apod/astropix.html)')
        embed.set_image(url=str(res_json['url']))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Server_Info(bot))