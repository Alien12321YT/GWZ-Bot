from discord.ext import commands
import discord

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

    @commands.command(help='Shows information about the member.')
    async def memberinfo(self,ctx,member:discord.Member=None):
        if member != None:
            embed = discord.Embed(
                title='Member: **{}**'.format(member.display_name),
                color=ctx.author.color
            )
            embed.add_field(name='Real Username',value=member.name)
            embed.add_field(name='Account Creation Date',value=member.created_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='Guild Join Date',value=member.joined_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='ID',value=member.id)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Ummm, how do I check stats on `/DisPixel/ForkAndKnifeDiscordBot#main.py.NoneType.null:0`?')

    @commands.command()
    async def roleinfo(self,ctx,role:discord.Role=None):
        if role != None:
            embed = discord.Embed(
                title='Role: **{}**'.format(role.name),
                color=ctx.author.color
            )
            embed.add_field(name='Name',value=role.mention)
            embed.add_field(name='Color',value='R: {}, G: {}, B: {}'.format(role.color.to_rgb()[0],role.color.to_rgb()[1],role.color.to_rgb()[2]))
            embed.add_field(name='Time Created',value=role.created_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='ID',value=str(role.id))
            await ctx.send(embed=embed)
        else:
            await ctx.send('An error has occured.')

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
        if channel != None:
            embed = discord.Embed(
                title='Channel: **{}**'.format(channel.name),
                color=ctx.author.color
            )
            embed.add_field(name='Name',value=channel.mention)
            embed.add_field(name='Time Created',value=channel.created_at.strftime('%b %d, %Y | %I:%M %p'))
            embed.add_field(name='ID',value=str(channel.id))
            await ctx.send(embed=embed)
            embed.add_field(name='Last Message',value=str(channel.last_message.content))
        else:
            await ctx.send('An error has occured.')

def setup(bot):
    bot.add_cog(Server_Info(bot))