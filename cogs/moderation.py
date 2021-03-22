import discord
from discord.ext import commands
import datetime
import json

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx,num=1):
            channel = ctx.channel
            num += 1
            await channel.purge(limit=int(num))
    
    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='changeprefix')
    async def change_the_poggers_prefix_to_something_stoopid(self,ctx,*,prefix:str='^'):
        with open('server.json','r') as f:
            p_d = json.load(f)
        old_prefix = p_d[str(ctx.guild.id)]
        p_d[str(ctx.guild.id)]['prefix'] = prefix
        await ctx.send(f'Your prefix changed from `{old_prefix}` to `{prefix}`!')
        with open('prefixes.json','w') as f:
            json.dump(p_d,f,indent=4)

    @commands.command(name='utc',aliases=['clock','utctime'])
    async def currenttime(self,ctx):
        await ctx.send(datetime.datetime.now().strftime('**%b %d, %Y** | %I:%M:%S %p GMT'))

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def slowmode(self,ctx,delay_in_sec,channel:discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        if delay_in_sec == 'off' or delay_in_sec == 'none':
            delay_in_sec = 0
        await channel.edit(slowmode_delay=delay_in_sec)
        await ctx.channel.send(f'{channel.mention} now has {delay_in_sec} seconds of slowmode.')

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='toggle',aliases=['settings','setting','tset'])
    async def toggle_command(self,ctx,setting:str=None):
        with open('server.json','r') as f:
            sdata = json.load(f)
        prefix = sdata[str(ctx.guild.id)]['prefix']
        if setting != None:
            if setting in sdata['defserver']:
                if sdata[str(ctx.guild.id)][str(setting)]:
                    sdata[str(ctx.guild.id)][str(setting)] = False
                    await ctx.send(f'`{setting}` is now off.')
                else:
                    sdata[str(ctx.guild.id)][str(setting)] = True
                    await ctx.send(f'`{setting}` is now on.')
                with open('server.json','w') as f:
                    json.dump(sdata,f,indent=4)
            elif setting == 'list':
                coolstr = ''
                for setting in sdata['defserver']:
                    coolstr += f'`{setting}`, '
                coolstr = coolstr[:-2]
                await ctx.send(coolstr)
            else:
                await ctx.send('That setting does not exist!')
        else:
            await ctx.send(f'What setting do you want to change?\nExample: `{prefix}toggle ff_mode`\n*Do* `{prefix}toggle list` *to see the options available')
    

def setup(bot):
    bot.add_cog(moderation(bot))