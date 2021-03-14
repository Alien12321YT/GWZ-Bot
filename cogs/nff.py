from discord.ext import commands
import datetime
import asyncio
import discord
import json

def isnt_ff_server(ctx):
    with open('server.json','r') as f:
        checkifffmode = json.load(f)
    return not checkifffmode[str(ctx.guild.id)]['ff_mode']

class non_family_friendly(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.check(isnt_ff_server)
    @commands.command(name='cum',aliases=['jerkoff'])
    async def milk_command_for_bot(self, ctx):
        pp_message = await ctx.send("""** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **:slight_smile:
        :muscle: :briefcase: :muscle:
        ** ** ** ** ** ** ** ** ** **:orange_book:
        ** ** ** ** ** ** ** ** :eggplant:
        ** ** ** **:leg:   :leg:""")
        await asyncio.sleep(1)
        await pp_message.edit(content="""** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **:confounded:
        :muscle: :briefcase: :muscle:
        ** ** ** ** ** ** ** ** ** **:orange_book:
        ** ** ** ** ** ** ** ** :eggplant:
        ** ** ** **:leg:   :leg:""")
        await asyncio.sleep(1)
        await pp_message.edit(content="""** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **:confounded:
        :muscle: :briefcase: :muscle:
        ** ** ** ** ** ** ** ** ** **:orange_book:
        ** ** ** ** ** ** ** ** :eggplant:
        ** ** ** **:leg:   :leg:""")
        await asyncio.sleep(1)
        await pp_message.edit(content="""** ** ** ** ** ** ** ** ** ** ** ** **rubs**
        ** ** ** ** ** ** ** **:confounded:
        :muscle: :briefcase: :muscle:
        ** ** ** ** ** ** ** ** ** **:orange_book:
        ** ** ** ** ** ** ** ** :eggplant:
        ** ** ** **:leg:   :leg:""")
        await asyncio.sleep(3)
        await pp_message.edit(content="""
        ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **:confounded:
        :muscle: :briefcase: :muscle:
        ** ** ** ** ** ** ** ** ** **:orange_book:
        ** ** ** ** ** ** ** ** :eggplant: <a:slatt_whalecum1:817745814453354547>
        ** ** ** **:leg:   :leg:"""
        )
        await asyncio.sleep(2)
        await pp_message.edit(content="""
        ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **:slight_smile:
        :muscle: :briefcase: :muscle:
        ** ** ** ** ** ** ** ** ** **:orange_book:
        ** ** ** ** ** ** ** ** :eggplant: <a:slatt_whalecum1:817745814453354547>
        ** ** ** **:leg:   :leg:"""
        )


def setup(bot):
    bot.add_cog(non_family_friendly(bot))

