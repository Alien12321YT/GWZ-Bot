import discord
from discord.ext import commands
import asyncio
from discord.ext.commands.cooldowns import BucketType
import random
import json

def only_authors(ctx):
    return ctx.author.id == 718109447825915946 or ctx.author.id == 692250820741300266

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

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        await open_account(member)
        users = await get_bank_data()
        wallet_amt = users['players'][str(member.id)]["wallet"]
        bank_amt = users['players'][str(member.id)]["bank"]

        embed = discord.Embed(
            title=f"{member.name}'s balance",
            color=discord.Color.red())
        embed.add_field(name="Wallet balance",value=wallet_amt, inline = False)
        embed.add_field(name ="Bank balance",value=bank_amt, inline = False)
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
        user = await open_account(ctx.author)
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
            if itemfound['price'] == None:
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

    @commands.command()
    async def sell(self, ctx,item:str='',amount:int=1):
        await open_account(ctx.author)
        bankdata = await get_bank_data()
        user = await open_account(ctx.author)
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
            if user['inv'].count(itemfound) <= amount:
                if itemfound['sellable'] == True:
                    user['wallet'] += cost
                    await ctx.send(f'You\'ve sold {amount} {itemname}(s) for ⏣{cost}')
                    await ctx.bot.get_guild(811547367979221042).get_channel(811583394033958943).send(f'{ctx.author.mention} has sold {amount} {itemname} for ⏣{cost}')
                    for i in range(amount):
                        user['inv'].append(itemid)
                else:
                    await ctx.send(f'Sorry, you can\'t sell {itemname}s.')
            else:
                await ctx.send(f'You don\'t have enough {itemname.lower()}s!')
        else:
            await ctx.send('Bruh that item isn\'t even in the shop ;-;')
            return False
        bankdata['players'][str(ctx.author.id)] = user
        
        with open('mainbank.json','w') as f:
            json.dump(bankdata,f,indent=4)

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

    @commands.command(aliases=['slot'])
    @commands.cooldown(1,3, commands.BucketType.user)
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
        if amount>169000:
                await ctx.send("You can't bet more than **⏣169,000** at once. If I let you bet any amount you will have 0 coins easily")
                return

        
        win = 0
        chance_calc = random.randint(1,random.randint(2,3))

        if chance_calc == 1:
            win = True
        
        final = []
        emojilist = [":eggplant:",":ok_hand:",":joy:",":cow:",":slight_smile:","<:item_alien:817236864397475880>","<:gwzbot:816986102824435772>",':flushed:',":diamond_shape_with_a_dot_inside:","<:badge_w:817346254953512962>","<:dildo:817769112750784532>","<a:DogeCoin:817944887784767538>"]
        emoji = random.choice(emojilist)
        loseemojilist = emojilist.copy()
        loseemojilist.pop(loseemojilist.index(emoji))
        for i in range(3):
            if win:
                final.append(emoji)
            else:
                final.append(random.choice(loseemojilist))
                while final[0] == final[1] == final[2]:
                    final = []
                    final.append(random.choice(loseemojilist))
        
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
    
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.user)
    async def guessnumber(self, ctx, amount:int = None):
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
        if amount>169000:
            await ctx.send("You can't bet more than **⏣169,000** at once. If I let you bet any amount you will have 0 coins easily")
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
    async def setmoney(self, ctx, player: discord.User, amount: int, mode:str='wallet'):
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

    @commands.command()
    async def danktaxcalc(self, ctx, question = None):
        question = int(question)
        if question == None:
            await ctx.send("Enter a valid amount")
        if 7125 < question >= 2300000:
            await ctx.send(f"{question}, coins, you would have to pay", round({question} / 0.85, 0), "with a 15% tax rate")
        elif 97001 < question >= 712500:
            await ctx.send(f"{question}, coins, you would have to pay", round({question} / 0.92, 0), "with a 8% tax rate")
        elif 48959 < question >= 97001:
            await ctx.send(f"{question}, coins, you would have to pay", round({question} / 0.95, 0), "with a 5% tax rate")
        elif 25001 < question >= 48959:
            await ctx.send(f"{question}, coins, you would have to pay", round({question} / 0.97, 0), "with a 3% tax rate")
        elif 1 < question >= 25001:
            await ctx.send(f"{question}, coins, you would have to pay", round({question} / 0.99, 0), "with a 1% tax rate")
        elif 0 < question >= 1:
            await ctx.send(f"{question}, coins, You would have to pay {question}")
        elif question == 0:
            await ctx.send("Um, 0 doesnt have a tax dumbass")
        else:
            await ctx.send("Dont enter commas, words or idk for tax calculations...")

def setup(bot):
    bot.add_cog(currency(bot))