# INSTALL DISCORD LIBRARY
# sudo apt install python3-pip
# pip3 install discord.py

# Notes

## When ever its a command, must be @client.command()
## async def {Command}(ctx):

## To send message, use await ctx.send("{Message}")

import discord
import random
import Gacha_List
import asyncio
from discord.ext import commands

## Stuff/List for Gacha

Gacha_Country_List = ['Germany', 'USSR', 'USA']
Gacha_Tier_List = ['Ultra Rare', 'Rare', 'Uncommon']
Gacha_Country_Len = len(Gacha_Country_List)

### Germany

Germany_Len_Uncommon = len(Gacha_List.Germany_Uncommon)
Germany_Len_Rare = len(Gacha_List.Germany_Rare)
Germany_Len_UltraRare = len(Gacha_List.Germany_UltraRare)

### USSR

Gacha_USSR_Len_Uncommon = len(Gacha_List.USSR_Uncommon)
Gacha_USSR_Len_Rare = len(Gacha_List.USSR_Rare)
Gacha_USSR_Len_UltraRare = len(Gacha_List.USSR_UltraRare)

### USA

Gacha_USA_Len_Uncommon = len(Gacha_List.USA_Uncommon)
Gacha_USA_Len_Rare = len(Gacha_List.USA_Rare)
Gacha_USA_Len_UltraRare = len(Gacha_List.USA_UltraRare)

TOKEN = '' # Deleted as it is sensitive
client = commands.Bot(command_prefix="R")

@client.event
async def on_ready():
    print('Bot is ready to slave away!')

@client.command()
async def Gacha(ctx,Gacha_Roll):

    ## Useful statistic
    Gacha_Rolled = 0
    Germany_Rolled = 0
    USA_Rolled = 0
    USSR_Rolled = 0
    Uncommon_Rolled = 0
    Rare_Rolled = 0
    UltraRare_Rolled = 0
    Uncommon = 0
    Rare = 0
    Ultra_Rare= 0
    
    ## Gacha System to choose, even odds or unfair odds
    try:
        await ctx.send('''\n
List of Gacha Systems:
1. Gaijin Style
2. Fair Probability Style
Enter a number >>> ''')
        def check(msg):
            return msg.author.id == ctx.author.id
        
        Gacha_System = await client.wait_for('message', timeout = 15, check=check)

## Unfair Gaijin Style Gacha (A game company that makes simulation, war, etc genre. The Gacha is inspired by the extremely unfair gacha in a game called 'War Thunder')
  
        if Gacha_System == '1':
            Gacha_Tier_List = ['Ultra Rare']
            Uncommon_Repetition = 995
            Rare_Repetition = 4

            Repetition_Count = 0
            while Repetition_Count < Uncommon_Repetition:
                Gacha_Tier_List.append('Uncommon')
                Repetition_Count = Repetition_Count + 1
            
            Repetition_Count = 0
            while Repetition_Count < Rare_Repetition:
                Gacha_Tier_List.append('Rare')
                Repetition_Count = Repetition_Count + 1
            await ctx.send('\nThe odds of the Gacha has been changed :D, enjoy the Gaijin experience!')

        elif Gacha_System == '2':
            await ctx.send('\nEnjoy your unadulterated odds :D')

        else:
            await ctx.send('Invalid input has been detected.')

        await ctx.send('\nRewards:')

        while Gacha_Rolled < Gacha_Roll:
            Gacha_Rolled = Gacha_Rolled + 1

            ## So get the index of List of countries and get the country as a string in a variable

            Gacha_Tier_Len = len(Gacha_Tier_List)
            Origin = random.randrange(0,Gacha_Country_Len)
            Country = Gacha_Country_List[Origin]
            Tier_Index = random.randrange(0,Gacha_Tier_Len)
            Tier = Gacha_Tier_List[Tier_Index]

            ## Use the assigned variable and then randomly pick an index of that country in order print the vehicle that you the person rolled
            if Country == 'Germany':
                if Tier == 'Uncommon':
                    Country_Tier = Gacha_List.Germany_Uncommon
                    Vehicle = random.randrange(0,Germany_Len_Uncommon)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (Germany) ({Tier})')
                    Uncommon_Rolled = Uncommon_Rolled + 1

                elif Tier == 'Rare':
                    Country_Tier = Gacha_List.Germany_Rare
                    Vehicle = random.randrange(0,Germany_Len_Rare)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (Germany) ({Tier})')
                    Rare_Rolled = Rare_Rolled + 1

                elif Tier == 'Ultra Rare':
                    Country_Tier = Gacha_List.Germany_UltraRare
                    Vehicle = random.randrange(0,Germany_Len_UltraRare)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (Germany) ({Tier})')
                    UltraRare_Rolled = UltraRare_Rolled + 1
                
                Germany_Rolled = Germany_Rolled + 1


            elif Country == 'USSR':
                if Tier == 'Uncommon':
                    Country_Tier = Gacha_List.USSR_Uncommon
                    Vehicle = random.randrange(0,Gacha_USSR_Len_Uncommon)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (USSR) ({Tier})')
                    Uncommon_Rolled = Uncommon_Rolled + 1

                elif Tier == 'Rare':
                    Country_Tier = Gacha_List.USSR_Rare
                    Vehicle = random.randrange(0,Gacha_USSR_Len_Rare)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (USSR) ({Tier})')
                    Rare_Rolled = Rare_Rolled + 1

                elif Tier == 'Ultra Rare':
                    Country_Tier = Gacha_List.USSR_UltraRare
                    Vehicle = random.randrange(0,Gacha_USSR_Len_UltraRare)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (USSR) ({Tier})')
                    UltraRare_Rolled = UltraRare_Rolled + 1

                USSR_Rolled = USSR_Rolled + 1

            elif Country == 'USA':
                if Tier == 'Uncommon':
                    Country_Tier = Gacha_List.USA_Uncommon
                    Vehicle = random.randrange(0,Gacha_USA_Len_Uncommon)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (USA) ({Tier})')
                    Uncommon_Rolled = Uncommon_Rolled + 1

                elif Tier == 'Rare':
                    Country_Tier = Gacha_List.USA_Rare
                    Vehicle = random.randrange(0,Gacha_USA_Len_Rare)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (USA) ({Tier})')
                    Rare_Rolled = Rare_Rolled + 1

                elif Tier == 'Ultra Rare':
                    Country_Tier = Gacha_List.USA_UltraRare
                    Vehicle = random.randrange(0,Gacha_USA_Len_UltraRare)
                    await ctx.send(f'{Gacha_Rolled}. {Country_Tier[Vehicle]} (USA) ({Tier})')
                    UltraRare_Rolled = UltraRare_Rolled + 1
                
                USA_Rolled = USA_Rolled + 1

        await ctx.send(f'''\n
Gacha Statistic:
Total Roll = {Gacha_Rolled}
Germany Roll = {Germany_Rolled}
USSR Roll = {USSR_Rolled}
USA Roll = {USA_Rolled}

Uncommon Rolled = {Uncommon_Rolled}
Rare Rolled = {Rare_Rolled}
Ultra Rare Rolled = {UltraRare_Rolled}

Probability:
Uncommon = 995/1000
Rare = 4/1000
Ultra Rare = 1/1000
    ''')
    except asyncio.TimeoutError:
        await ctx.send('The command has timed out.')





async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return
    if message.channel.name == "general":
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hello {username}!')

        elif user_message.lower() == 'bye':
            await message.channel.send(f'Bbai {username}!')

        elif user_message.lower() == '!random':
            response = f'This is your random number: {random.randrange(100)}'
            await message.channel.send(f'Your lucky number is {response} {username}!')
            return
        
        elif user_message.lower() == 'swuck mwy bwolls pwease':
            await message.channel.send('Oki UwU')

        elif user_message.lower() == 'man':
            await message.channel.send('man')

        elif user_message.lower() == 'help':
            await message.channel.send("""
            usage: hello bye !random
            """)

client.run(TOKEN)

