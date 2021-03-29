import discord
from discord.ext import commands,tasks
import asyncio
from discord.ext.commands.cooldowns import BucketType
import random
import json

five_over_six = 5/6
w = asyncio.sleep

def only_authors(ctx):
    return ctx.author.id == 718109447825915946 or ctx.author.id == 692250820741300266

@tasks.loop(seconds=five_over_six)
async def update_time(bot):
    with open('mainbank.json','r') as f:
        time_ = json.load(f)
    time_['time']['minute'] += 1
    if time_['time']['minute'] >= 60:
        time_['time']['hour'] += 1
        time_['time']['minute'] = 0
    if time_['time']['hour'] >= 24:
        time_['time']['day'] += 1
        time_['time']['hour'] = 0
    if time_['time']['day'] > 12: 
        time_['time']['season'] += 1
        time_['time']['day'] = 0
    if time_['time']['season'] >= 4:
        time_['time']['year'] += 1 
        time_['time']['season'] = 1
    with open('mainbank.json','w') as f:
        json.dump(time_,f,indent=4)
    timer = time_['time']
    min = str(timer['minute'])
    if len(min) == 1:
        min = '0' + str(min)
    hour = timer['hour']
    day = timer['day']
    season = timer['season'] 
    seastr = None
    if season == 1:
        seastr = 'Spring'
    elif season == 2:
        seastr = 'Summer'
    elif season == 3:
        seastr = 'Autumn'
    elif season == 4:
        seastr = 'Winter'
    else:
        seastr = 'Unknown'
    year = timer['year']
    if season == 1:
        seastr_ = 'Spring <:seasn_spring:820335313472978954>'
    elif season == 2:
        seastr_ = 'Summer <:seasn_summer:820335372914917376>'
    elif season == 3:
        seastr_ = 'Autumn <:seasn_autumn:820335409820991528>'
    elif season == 4:
        seastr_ = 'Winter <:seasn_winter:820335445069135953>'
    else:
        seastr_ = 'Unknown'
    if int(min) == 0:
        print(f'Day {day} {hour}:{min} | {seastr} of Year {year}')
    

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users['players']:
        return False
    else:
        users['players'][str(user.id)] = {}
        users['players'][str(user.id)]["wallet"] = 69
        users['players'][str(user.id)]["bank"] = 0
        users['players'][str(user.id)]['inv'] = []

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()
    
    users['players'][str(user.id)][mode] = round(users['players'][str(user.id)][mode]) + round(change)

    with open("mainbank.json","w") as f:
        json.dump(users,f,indent=4)


        bal = [users['players'][str(user.id)][mode],users['players'][str(user.id)]["bank"]]
        return bal

class currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        update_time.start(bot)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        await open_account(member)
        users = await get_bank_data()
        wallet_amt = users['players'][str(member.id)]["wallet"]
        bank_amt = users['players'][str(member.id)]["bank"]
        total_amt = wallet_amt + bank_amt

        embed = discord.Embed(
            title=f"{member.name}'s balance",description = f"**Wallet balance**: ⏣{wallet_amt}\n**Bank balance**: ⏣{bank_amt}\n**Total**: ⏣{total_amt}",
            color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx,member:discord.Member=None):        
        if member == None:
            member = ctx.author
        users = await get_bank_data()
        blnk=''
        if len(users['players'][str(member.id)]['inv']) <= 0:
            blnk = 'This person has nothing, so broke bruh'
        embed = discord.Embed(title='Inventory',description=blnk,color=discord.Color.red())
        for item in users['shop']:
            if item['id'] in users['players'][str(member.id)]['inv']:
                embed.add_field(name=item['name'],value=users['players'][str(member.id)]['inv'].count(item['id']))
        await ctx.send(embed=embed) 

    @commands.command() 
    async def shop(self, ctx,item=None):
        if item == None:
            embed = discord.Embed(title = "GWZ Shop", color=ctx.author.color)
            with open('mainbank.json','r') as f:
                bank = json.load(f)
            mainshop = bank['shop']
            for item in mainshop:
                if item['viewable']:
                    name = item["name"]
                    if type(item['price']) == int:
                        price = item["price"]
                    else:
                        price = '∞'
                    id = item["id"]
                    description = item["description"]
                    sellable = str(item['sellable'])
                    embed.add_field(name = name, value = f"**⏣{price}** | `{id}`: {description} | Sellable: {sellable}")

        await ctx.send(embed = embed)

    @commands.command()
    async def buy(self, ctx,item:str='',amount:int=1):
        await open_account(ctx.author)
        overexceed = False
        littler = False
        pre_amount = amount
        if amount > 269:
            overexceed = True
            amount = 269
        if amount < 0:
            amount = 0
            littler = True
        bankdata = await get_bank_data()
        if bankdata['time']['hour'] >= 7 and bankdata['time']['hour'] < 17:
            user = bankdata['players'][str(ctx.author.id)]
            items = bankdata['shop']
            itemids = []
            itemfound = None
            for i in items:
                itemids.append(i['id'])
            
            if item.lower() in itemids:
                if overexceed:
                    await ctx.send(f'`Whoops! You asked for {pre_amount} items, but the store only has 269. Looks like we\'ll have to roll with that! It will restock automatically.`')
                if littler:
                    await ctx.send(f'`Whoops! You can\'t buy {pre_amount} items, use the sell command to get less {item}!`')
                item = item.lower()
                for i in items:
                    if i['id'] == item:
                        itemfound = i
                itemname = itemfound['name_s']
                if itemfound['price'] == None or itemfound['buyable'] == False:
                    await ctx.send(f'You can\'t buy {itemname}!')
                    return
                cost = itemfound['price'] * amount
                itemid = itemfound['id']
                if user['wallet'] >= cost:
                    if not(len(user['inv']) >= 2048 or (len(user['inv']) + amount) >= 2048):
                        user['wallet'] -= cost
                        await ctx.send(f'You\'ve bought {amount} {itemname}(s) for ⏣{cost}')
                        await ctx.bot.get_guild(811547367979221042).get_channel(811583394033958943).send(f'{ctx.author.mention} has bought {amount} {itemname} for ⏣{cost}')
                        for i in range(amount):
                            user['inv'].append(itemid)
                    else:
                        await ctx.send('You have too much items! Maybe try selling some?')
                else:
                    await ctx.send('You don\'t have enough money!')
            else:
                await ctx.send('Bruh that item isn\'t even in the shop ;-; Do `^shop` to see items')
                return False
            bankdata['players'][str(ctx.author.id)] = user
            
            
            with open('mainbank.json','w') as f:
                json.dump(bankdata,f,indent=4)
        else:
            await ctx.send('GWZ Shop is closed! It is open from 7:00 - 17:00 in a day of a season in the currency system. Do `^time` to see the time. Come back soon!')

    @commands.command()
    async def sell(self, ctx,item:str='',amount:int=1):
        await open_account(ctx.author)
        bankdata = await get_bank_data()
        if bankdata['time']['hour'] >= 7 and bankdata['time']['hour'] < 17:
            
            items = bankdata['shop']
            itemids = []
            itemfound = None
            for i in items:
                itemids.append(i['id'])
            
            if item.lower() in itemids:
                item = item.lower()
                for i in items:
                    if i['id'] == item:
                        itemfound = i
                cost = round((itemfound['price'] * amount) * (2/3))
                itemid = itemfound['id']
                itemname = itemfound['name_s']
                if bankdata['players'][str(ctx.author.id)]['inv'].count(itemfound['id']) <= amount:
                    if itemfound['sellable'] == True:
                        bankdata['players'][str(ctx.author.id)]['wallet'] += cost
                        await ctx.send(f'You\'ve sold {amount} {itemname}(s) for ⏣{cost}')
                        await ctx.bot.get_guild(811547367979221042).get_channel(811583394033958943).send(f'{ctx.author.mention} has sold {amount} {itemname} for ⏣{cost}')
                        for i in range(amount):
                            bankdata['players'][str(ctx.author.id)]['inv'].append(itemid)
                    else:
                        await ctx.send(f'Sorry, you can\'t sell {itemname}s.')
                else:
                    await ctx.send(f'You don\'t have enough {itemname.lower()}s!')
            else:
                await ctx.send('Bruh that item isn\'t even in the shop ;-;')
                return False
            
            with open('mainbank.json','w') as f:
                json.dump(bankdata,f,indent=4)
        else:
            await ctx.send('GWZ Shop is closed! It is open from 7:00 am - 5:00 pm in a day of a season in the currency system. Do `^time` to see the time. Come back soon!')

    @commands.command()
    @commands.cooldown(1,30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)
 
        users = await get_bank_data()

        user = ctx.author


        earnings = random.randrange(690)

        await ctx.send(f"{ctx.author.mention} Someone gave you **⏣{earnings}**!")


 
        users['players'][str(user.id)]["wallet"] += earnings

        with open("mainbank.json","w") as f:
            json.dump(users,f,indent=4)

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx,amount = None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount you want to withdraw ;-;")
            return

        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[1]

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("You don't even have that much money bruh ;-;")
            return
        if amount<0:
            await ctx.send("Amount must be positive...")
            return

        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,"bank")

        await ctx.send(f"**⏣{amount}** withdrawn!")

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx,amount = None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount you want to deposit ;-;")
            return

        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("You don't even have that much money bruh ;-;")
            return
        if amount<0:
            await ctx.send("Amount must be positive...")
            return

        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author,amount,"bank")

        await ctx.send(f"**⏣{amount}** deposited!")

    @commands.command(aliases=['send'])
    @commands.cooldown(1,10, commands.BucketType.user)
    async def give(self, ctx,member:discord.Member,amount = None):
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter the amount you want to send ;-;")
            return
            
        if member == ctx.author:
            await ctx.send("How can you give yourself coins?")
            return

        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("You don't even have that much money bruh ;-;.")
            return
            
        if amount<0:
            await ctx.send("Amount must be positive...")
            return

        await update_bank(ctx.author,-1*amount,"wallet")
        await update_bank(member,amount,"wallet")

        await ctx.send(f"You gave {member.name} **⏣{amount}!**")
        await ctx.bot.get_guild(811547367979221042).get_channel(811583394033958943).send(f'{ctx.author.mention} has given {member.mention} **⏣{amount}**')

    @commands.command()
    @commands.cooldown(1,4, commands.BucketType.user)
    async def use(self, ctx,item=None):
        await open_account(ctx.author)
        item = item.lower()
        with open('mainbank.json','r') as f:
            bank = json.load(f)
        if item == None:
            await ctx.send('Actually mention an item lmao')
            return
        else:
            if not (item in bank['players'][str(ctx.author.id)]['inv']):
                await ctx.send('You don\'t have this item ????!?!?!')
                return
            if item == 'alien':
                bank['players'][str(ctx.author.id)]['inv'].append('alien')
                await ctx.send('They\'re multiplying! You now have another Alien.')
            elif item == 'bread':
                bank['players'][str(ctx.author.id)]['inv'].remove('bread')
                await ctx.send("Yum! This bread is extremely yummy! It must have perks, right? ||Well no if it\'s yummy af doesn't mean that it must have perks. But they are coming soon!||")
            elif item == 'cookie':
                bank['players'][str(ctx.author.id)]['inv'].remove('cookie')
                await ctx.send("You ate a cookie and it actually tastes good.")
            else:
                await ctx.send('mention a useable item')
                return
        with open('mainbank.json','w') as f:
            json.dump(bank, f, indent=4)

    """@commands.command(name='look',aliases=['search'])
    async def look_c(self,ctx):
        areas = ['Hurb Mall','bushes','your mom','source code','somewhere over the rainbow','GWZ Bot official server','the english dictionary','up your butt']
        await ctx.send(f'Where will you go?\n`{random.choice(areas)}` | `{random.choice(areas)}`')"""

    @commands.command()
    async def rakeleaves(self,ctx):
        bank = await get_bank_data()
        if bank['time']['season'] == 3:
            paid_mon = random.randint(200,569)
            leaves = random.randint(5,14)
            await ctx.send(f'You earned **\u23E3{paid_mon}**! You also earned {leaves} Dorito Leaves <:item_doritoleaf:820570720031211593>.')
            for i in range(leaves):
                bank['players'][str(ctx.author.id)]['inv'].append('dorito_leaf')
            bank['players'][str(ctx.author.id)]['bank'] += paid_mon
            with open('mainbank.json','w') as f:
                json.dump(bank,f,indent=4)
        else:
            await ctx.send('This command can only be used during Autumn season of the currency system!')
            
    @commands.command()
    async def shovelsnow(self,ctx):
        bank = await get_bank_data()
        if bank['time']['season'] == 4:
            paid_mon = random.randint(200,569)
            snowcubes = random.randint(5,14)
            await ctx.send(f'You earned **\u23E3{paid_mon}**! You also earned {snowcubes} Snowcubes.')
            for i in range(snowcubes):
                bank['players'][str(ctx.author.id)]['inv'].append('snow_cube')
            bank['players'][str(ctx.author.id)]['bank'] += paid_mon
            with open('mainbank.json','w') as f:
                json.dump(bank,f,indent=4)
        else:
            await ctx.send('This command can only be used during Winter season of the currency system!')

    @commands.command(name='wheel')
    @commands.cooldown(1,7.5,BucketType.channel)
    async def wheel(self,ctx,forcevalue:int=None):
        await open_account(ctx.author)
        with open('mainbank.json') as f:
            bank_data = json.load(f)
        await ctx.send(f'{ctx.author.mention} is spinning the wheel!',delete_after=7)
        await w(1)
        await ctx.send('.',delete_after=6)
        await w(0.5)
        await ctx.send('..',delete_after=5.5)
        await w(0.5)
        await ctx.send('...',delete_after=5)
        await w(0.5)
        await ctx.send('.',delete_after=4.5)
        await w(0.5)
        await ctx.send('..',delete_after=4)
        await w(0.5)
        await ctx.send('...',delete_after=3.5)
        await w(3.5)
        chlist = [100 for i in range(50)]
        chlist += [200 for i in range(30)]
        chlist += [1000 for i in range(25)]
        chlist += [4000 for i in range(15)]
        chlist += [10000 for i in range(10)]
        chlist += [25000 for i in range(5)]
        chlist += [75000 for i in range(3)]
        chlist += [100000 for i in range(2)]
        res = random.choice(chlist)
        if forcevalue != None:
            await self.bot.wait_for('message',timeout=0.6942)
            if ctx.channel.last_message == 'wheelie':
                res = int(forcevalue)
        await ctx.send(f'{ctx.author.mention} You\'ve just won **⏣{res}**! It is in your wallet.')
        bank_data['players'][str(ctx.author.id)]['wallet'] += res
        with open('mainbank.json','w') as f:
            json.dump(bank_data,f,indent=4)

    @commands.command(aliases=['slot'])
    @commands.cooldown(1,3,BucketType.user)
    async def slots(self, ctx,amount = None):
        await open_account(ctx.author)
        with open('mainbank.json','r') as f:
            bank = json.load(f)
        if amount == None:
            await ctx.send("Please enter the amount you want to bet ;-;")
            return

        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
                await ctx.send("You don't even have that much money bruh ;-;")
                return
        if amount<0:
            await ctx.send("Amount must be positive...")
            return
        if amount<100:
                await ctx.send("You can't bet less than 100 coins")
                return
        if amount>69420:
                await ctx.send("You can't bet more than **⏣69,420** at once. If I let you bet any amount you will have 0 coins easily")
                return

        if bank['time']['hour'] >= 7 and bank['time']['hour'] < 23:
            win = 0
            chance_calc = random.randint(1,random.randint(2,3))

            if chance_calc == 1:
                win = True
            
            final = []
            emojilist = [":eggplant:",":ok_hand:",":joy:",":cow:",":slight_smile:","<:item_alien:817236864397475880>","<:gwzbot:816986102824435772>",':flushed:',":diamond_shape_with_a_dot_inside:","<:badge_w:817346254953512962>","<:dildo:817769112750784532>","<a:DogeCoin:817944887784767538>","<:seasn_spring:820335313472978954>","<a:sex:817345618938560512>"]
            emoji = random.choice(emojilist)
            if win:
                final.append(emoji)
                final.append(emoji)
                final.append(emoji)
            else:
                final.append(random.choice(emojilist))
                final.append(random.choice(emojilist))
                final.append(random.choice(emojilist))
                while final[0] == final[1] == final[2]:
                    final = []
                    final.append(random.choice(emojilist))
            
            em1 = final[0]
            em2 = final[1]
            em3 = final[2]
            await ctx.send(f'{ctx.author.mention}\'s slots machine:\n__|{em1}|{em2}|{em3}|__')

            money_outcome = 0

            if win:
                bank['players'][str(ctx.author.id)]['wallet'] += int(round(2.75*amount)) 
                await ctx.send("You won! GG :)")
                money_outcome = round(2.5*amount)
            else:
                bank['players'][str(ctx.author.id)]['wallet'] -= amount
                await ctx.send("You lost! Sad :(")
                money_outcome = round(amount)
        
            outcome = ''
            if win:
                outcome = 'won'
            else:
                outcome = 'lost'

            with open('mainbank.json','w') as f:
                json.dump(bank,f,indent=4)
        else:
            await ctx.send('Venus Gambling Club is closed! They are open between 7:00 and 23:00 in a day of a season in the currency system. Do `^time` to see the time. Come back soon!.')
    
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.user)
    async def guessnumber(self, ctx, amount = None):
        await open_account(ctx.author)
        with open('mainbank.json','r') as f:
            bank = json.load(f)
        if amount == None:
            await ctx.send("Please enter the amount you want to bet ;-;")
            return
        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("You don't even have that much money bruh ;-;")
            return
        if amount<0:
            await ctx.send("Amount must be positive...")
            return
        if amount<100:
            await ctx.send("You can't bet less than **⏣100**")
            return
        if amount>69420:
            await ctx.send("You can't bet more than **⏣69,420** at once. If I let you bet any amount you will have 0 coins or if you're lucky you will become too rich.")
            return
            
        await ctx.send("Enter your guess between 1 to 10")
        if random.randint(1,10000) != 10000:
            randomNumber = random.randint(1,10)
        else:
            randomNumber = 69 
        guessNumber = 0
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} You need to respond me")
        try:
            guessNumber = int(ctx.channel.last_message.clean_content)
        except:
            await ctx.send('Enter a valid number... -_-')
        if guessNumber == randomNumber:
            await update_bank(ctx.author,round(6.25*amount))
            await ctx.send("You won! :)")

        else:
            await update_bank(ctx.author,-1*amount)
            await ctx.send("You lost! :(")
            await ctx.send(f"Number was {randomNumber}")
        with open('mainbank.json','w') as f:
            json.dump(bank,f,indent=4)

        outcome = ''
        if guessNumber == randomNumber:
            outcome = 'won'
            money_outcome = round(6.25*amount) 
        else:
            outcome = 'lost'
            money_outcome = amount

    @commands.command()
    @commands.check(only_authors)
    async def setmoney(self, ctx, player: discord.Member, amount: int, mode:str='wallet'):
        await open_account(player)
        with open('mainbank.json','r')as f:
            bank_data = json.load(f)
        if mode == 'bank' or mode == 'b':
            bank_data['players'][str(player.id)]['bank'] = amount
        else:
            bank_data['players'][str(player.id)]['wallet'] = amount
        with open('mainbank.json','w') as f:
            json.dump(bank_data,f,indent=4)

    @commands.command()
    @commands.check(only_authors)
    async def wipe(self, ctx,player:discord.User):
        with open('mainbank.json','r')as f:
            bank_data = json.load(f)
    
        bank_data['players'].pop(str(player.id))

        with open('mainbank.json','w') as f:
            json.dump(bank_data,f,indent=4)

    @commands.cooldown(1,5,BucketType.user)
    @commands.command()
    async def countup(self, ctx):
        await open_account(ctx.author)
        with open('mainbank.json','r') as f:
            count = json.load(f)
        count['other']['countup'] += 1
        currentcount = count['other']['countup']
        await ctx.send(f'{ctx.author.mention} set the count to {currentcount}')
        if count['other']['countup'] % 100 == 0:
            count['players'][str(ctx.author.id)]["wallet"] += 10000
            await ctx.send(f'You just earned ⏣10000 for getting the count up to {currentcount}')
        with open('mainbank.json','w') as f:
            json.dump(count,f,indent=4)
    
    @commands.cooldown(1,3,BucketType.user)
    @commands.command(aliases=['gamble'])
    async def bet(self, ctx, amount = None):
        await open_account(ctx.author)
        with open('mainbank.json','r') as f:
            bank = json.load(f)
        if amount == None:
            await ctx.send("Please enter the amount you want to bet ;-;")
            return
        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("You don't even have that much money bruh ;-;")
            return

        if amount<0:
            await ctx.send("What do you mean i give u money ??!?!?!?!?!?!")
            return

        if amount<100:
            await ctx.send("You can't bet less than **⏣100**")
            return

        if amount>69420:
            await ctx.send("You can't bet more than **⏣69,420** at once. If I let you bet any amount you will have 0 coins or if you're lucky you will become too rich.")
            return

        my_rolls = random.randint(1,6)
        bot_rolls = random.randint(1,6)
        color = 0x000000
        
        if my_rolls > bot_rolls:
                win_or_lose = "winning"
                win_or_lose2 = "won"
                bank['players'][str(ctx.author.id)]['wallet'] += round(amount * 1.5)

                outcome = round(amount * 1.5)

                color = 0x0000ff
        elif bot_rolls > my_rolls:
                win_or_lose = "losing"
                win_or_lose2 = "lost"
                outcome = amount

                bank['players'][str(ctx.author.id)]['wallet'] += round(amount * -1)

                color = 0xff0000

        else:
            win_or_lose = "tie"
            win_or_lose2 = "lost"
            outcome = 0 
            color = 0x00ff00

        embed = discord.Embed(
            title = f"{ctx.author.display_name}'s {win_or_lose} gambling game", 
            description = f"You {win_or_lose2} **⏣{outcome}**",
            color=color
        ) 

        embed.add_field(name = f"{ctx.author.name}", value = f"`{my_rolls}`")
        embed.add_field(name = "GWZ Bot", value = f"`{bot_rolls}`")

        await ctx.send(embed=embed)

        with open('mainbank.json','w') as f:
            json.dump(bank,f,indent=4)
    
    @commands.command(name='time')
    async def time_c(self,ctx):
        with open('mainbank.json','r') as f:
            time_ = json.load(f)
        time_ = time_['time']
        min = str(time_['minute'])
        if len(min) == 1:
            min = '0' + str(min)
        hour = time_['hour']
        day = time_['day']
        season = time_['season']
        seastr = None
        if season == 1:
            seastr = 'Spring <:seasn_spring:820335313472978954>'
        elif season == 2:
            seastr = 'Summer <:seasn_summer:820335372914917376>'
        elif season == 3:
            seastr = 'Autumn <:seasn_autumn:820335409820991528>'
        elif season == 4:
            seastr = 'Winter <:seasn_winter:820335445069135953>'
        else:
            seastr = 'Unknown'
        year = time_['year']
        await ctx.send(f'Day {day} {hour}:{min} | {seastr} of Year {year}')

def setup(bot):
    coggggg = currency(bot)
    bot.add_cog(coggggg)     