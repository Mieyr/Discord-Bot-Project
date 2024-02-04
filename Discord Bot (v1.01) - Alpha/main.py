# INSTALL DISCORD LIBRARY
# sudo apt install python3-pip
# pip3 install discord.py

# Notes

## When ever its a command, must be @client.command()
## async def {Command}(ctx):

## To send message, use await ctx.send("{Message}")

from ast import Return
from email.message import Message
from socket import timeout
from tabnanny import check
import time
from discord.utils import get
import discord
import asyncio
import random
import Gacha_List_Main
from discord.ext import commands
import json
import xlsxwriter
import mysql.connector

with open("config.json") as f:
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["PREFIX"]

print(prefix)
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = prefix, intents = intents)
Cooldown_Error = "**On Cooldown**, {}, the command you\'ve attempted to execute is still on cooldown. Please try again in **{:.1f}s**"

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'ravu_bot'
)

cursor = mydb.cursor(dictionary = True)

# def Embed(ctx):
#     embed = discord.Embed(
#         title = "Commands", 
#         description = "List of commands for Ravu Bot.", 
#         color = 0xFF5733
#     )

#     embed.add_field(
#         name = "Card Utilities", 
#         value = '''
#         `cardinfo` `daily` `vote` `salvage` `construct` `recover`
#         ''', 
#         inline = True
#     )

#     embed.add_field(
#         name = "Miscellaneous",
#         value = '''
#         `Error`
#         ''',
#         inline = True
#     )

#     embed.add_field(
#         value = "Use R ch <command> to acquire more information regarding the command."
#     )

#     embed.set_author(
#         name = ctx.author,
#         icon_url = ctx.author.avatar
#     )

#     embed.set_footer(
#         icon_url = client.user.avatar, 
#         text = "Ravu - Alpha v1.01"
#     )
    
#     return embed


@client.event
async def on_ready():
    print("{0.user} is ready to slave away!".format(client))
    await client.change_presence(activity=discord.Game("Ravu Development"))

@client.event
async def on_disconnect():
    print("Back to the cage")

def Error(Error_Code):
    if Error_Code == "101":
        Error_Message = "Error 101: {}, the command has timeout."
    elif Error_Code == "201":
        Error_Message = "Error 201: {}, an error has occured within a database command."
    elif Error_Code == "301":
        Error_Message = "**On Cooldown**, {}, the command you\'ve attempted to execute is still on cooldown. Please try again in **{:.1f}s**"
    elif Error_Code == "401":
        Error_Message = "Error 401: {}, you're not authorised to execute this command."
    return Error_Message

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): # Checks whether the command is in cooldown
        Message = Error("301").format(ctx.author.mention, error.retry_after)
        await ctx.send(Message)

# Hello Command

@client.command()
async def hello(ctx):
    await ctx.send("hello, bitch.")

# Card Help command

@client.command()
async def command(ctx):

    embed = discord.Embed(
        title = "Commands", 
        description = "List of commands for Ravu Bot.", 
        color = 0xFF5733
    )

    embed.add_field(
        name = "Card Utilities", 
        value = '''
        `cardinfo` `daily` `vote` `salvage` `construct` `recover`
        ''', 
        inline = True
    )

    embed.add_field(
        name = "Miscellaneous",
        value = '''
        `Error`
        ''',
        inline = True
    )

    embed.add_field(
        name = "Tips:",
        value = "Use *R ch `<command>`* to acquire more information regarding the command.",
        inline = False
    )

    embed.set_author(
        name = ctx.author,
        icon_url = ctx.author.avatar
    )

    embed.set_footer(
        icon_url = client.user.avatar, 
        text = "Ravu - Alpha v1.01"
    )

    await ctx.send(embed=embed)

@client.command()
async def ch(ctx,*,arg):

    if arg == "cardinfo":
        title_detail = "R cardinfo"
        description_detail = """
        Shortcut: `R ci`
        Instruction: `R ci` `Country of Origin` `Designated Card Code`

        View the description of a Card."""

    elif arg == "daily":
        title_detail = "R daily"
        description_detail = """
        Shortcut: `N/A`
        Instruction: `R daily`

        Receive a daily reward with a cooldown of 24 hour."""

    elif arg == "vote":
        title_detail = "R vote"
        description_detail = """
        Shortcut: `N/A`
        Instruction: `R vote`
        
        Receive a reward by voting for Ravu Bot!"""

    elif arg == "recover":
        title_detail = "R recover"
        description_detail = """
        Shortcut: `R rec`
        Instruction: `R recover` `Unique Code`
        
        Recover a damaged, or a potentially working Card!"""
    
    elif arg == "salvage":
        title_detail = "R salvage"
        description_detail = """
        Shortcut: `R sal`
        Instruction: `R salvage` `Unique Code`
        
        Salvage a Card you own in your garage."""
    
    elif arg == "construct":
        title_detail = "R construct"
        description_detail = """
        Shortcut: `R con`
        Instruction: `R construct` `Designated Card Code`
        
        Construct a Card of varying quality!"""
        
    embed = discord.Embed(
        title = f"Command Info: `{title_detail}`", 
        description = description_detail, 
        color = 0xFF5733,
    )
    embed.set_footer(
        icon_url = client.user.avatar, 
        text = "Ravu - Alpha v1.01"
    )
    embed.set_author(
        name = ctx.author,
        icon_url = ctx.author.avatar
    )
    await ctx.send(embed=embed)

@client.command(fallback = "Country:")
async def test(ctx,*,arg): ### (*,arg) so that it would take the whole sentence bruh.
    ### {prefix} test {Country} [Optional {Code/Card number}]

    Input = arg.split(" ")
    if len(Input) == 1:
        if Input[0] == 'Germany' or 'germany':
            Uncommon_List = ""
            Rare_List = ""
            UltraRare_List = ""
            Card_Code = 1
        
            Card_Index = 0
            while Card_Index < len(Gacha_List_Main.Germany_Uncommon):
                Uncommon_List = f'{Uncommon_List}\n{Card_Code}. {Gacha_List_Main.Germany_Uncommon[Card_Index]}'
                Card_Code += 1
                Card_Index += 1

            Card_Index = 0
            while Card_Index < len(Gacha_List_Main.Germany_Rare):
                Rare_List = f'{Rare_List}\n{Card_Code}. {Gacha_List_Main.Germany_Rare[Card_Index]}'
                Card_Code += 1
                Card_Index += 1

            Card_Index = 0
            while Card_Index < len(Gacha_List_Main.Germany_UltraRare):
                UltraRare_List = f'{UltraRare_List}\n{Card_Code}. {Gacha_List_Main.Germany_UltraRare[Card_Index]}'
                Card_Code += 1
                Card_Index += 1
        
        embed = discord.Embed(
        title = f"Germany's Available Cards", 
        color = 0xFF5733
        )
        embed.add_field(
            name = 'Uncommon',
            value = f'{Uncommon_List}',
            inline = True
        )
        embed.add_field(
            name = 'Rare',
            value = f'{Rare_List}',
            inline = True
        )
        embed.add_field(
            name = 'Ultra Rare',
            value = f'{UltraRare_List}',
            inline = True
        )
        embed.set_footer(
            icon_url = client.user.avatar, 
            text = "Ravu - Alpha v1.01"
        )
        embed.set_author(
            name = ctx.author,
            icon_url = ctx.author.avatar
        )
        embed.set_thumbnail(
            url = str(Gacha_List_Main.Gacha_Country_List_2[0][1])
        )
        await ctx.send(embed=embed)

    elif len(Input) == 2:
        if Input[1] == '6':
            embed = discord.Embed(
                title = "Panther A", 
                description = 'Pz.Kpfw.V Ausf.A, commonly known as Panther A, is an all rounded World War 2 medium Card.', 
                color = 0xFF5733,
            )
            embed.add_field(
                name = 'Rarity',
                value = "Uncommon",
                inline = True
            )
            embed.add_field(
                name = 'Armament',
                value = '''
                75 mm KwK42 cannon
                Smoke grenade launcher x6
                7.92 mm MG34 machine gun x2''',
                inline = True
            )
            embed.add_field(
                name = 'In service',
                value = "953",
                inline = True
            )
            embed.set_image(
                url = 'https://cdn.discordapp.com/attachments/833610986262495302/1006096168280936490/panther_A.png?size=4096'
            )
            embed.set_footer(
                icon_url = client.user.avatar, 
                text = "Ravu - Alpha v1.01"
            )
            embed.set_author(
                name = ctx.author,
                icon_url = ctx.author.avatar
            )
            embed.set_thumbnail(
                url = str(Gacha_List_Main.Gacha_Country_List_2[0][1])
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send('Prob')

# Confirmation to make a card drop zone/channel for Cards Card

@client.command()
async def myroles(ctx):
    await ctx.send(ctx.roles)
    print(ctx.roles)

@client.command(pass_context = True)
@commands.has_permissions(ban_members = True)
async def setup_card(ctx):
    try: 

        # if ctx.top_role =

        embed = discord.Embed(
            title = "Confirmation", 
            description = "Are you sure to confirm to make this channel a card drop zone?", 
            color = 0xFF5733
        )
        embed.add_field(
            name = "Timeout in", 
            value = "20s", 
            inline = False
        )
        embed.set_author(
            name = ctx.author,
            icon_url = ctx.author.avatar

        )
        embed.set_footer(
            icon_url = client.user.avatar, 
            text = "Ravu - Alpha v1.01"
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        
        try:
            
            # the wait_for will only register if the following conditions are met
            def check(reaction, user):
                return user.id == ctx.author.id and str(reaction) == '👍'

            # timeout kwarg is optional
            reaction, user = await client.wait_for("reaction_add", check=check, timeout=30)

            # then execute your code here if the author reacts, like so:
            await ctx.send("I have confirmed this channel as a card drop zone!")

        except asyncio.TimeoutError:
            await ctx.send(Error("101").format(ctx.author.mention))
            

    except:
        await ctx.send(Error("101").format(ctx.author.mention))

## Games

@client.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def search(ctx):

    import Search_Places_List # Import the list

    Author = ctx.message.author # Similar ig...
    User = str(ctx.author) # To get name and # of the author/the person who executes the command
    Allocated_Place = 0
    Place1 = "x"
    Place2 = "x"
    Place3 = "x"

    while Allocated_Place < 3: # Will keep repeating until all 3 allocated places are filled
        Potential = random.randrange(0,len(Search_Places_List.Area)) # Get a random area from the list
        if Place1 == "x" and Place1 != Potential and Place2 != Potential and Place3 != Potential: # These 3 are to prevent multiple area that are the same, so they check one by one and compare it with the others 
            Place1 = Potential
            Allocated_Place += 1
        elif Place2 == "x" and Place1 != Potential and Place2 != Potential and Place3 != Potential:
            Place2 = Potential
            Allocated_Place += 1
        elif Place3 =="x" and Place1 != Potential and Place2 != Potential and Place3 != Potential:
            Place3 = Potential
            Allocated_Place += 1

    Area1 = Search_Places_List.Area[Place1]
    Area2 = Search_Places_List.Area[Place2]
    Area3 = Search_Places_List.Area[Place3]

    await ctx.send(f'''
Where do you want to search?
    1. {Area1}
    2. {Area2}
    3. {Area3}
Pick an area to search >>>''')

    def check(msg):
        return msg.author.id == ctx.author.id
    user_mention = ctx.author.mention # To get name, #, and also mention the author/the person who executes the command

    try:
        Chosen_Place = await client.wait_for("message", timeout = 10, check=check)
        if Area1 != Chosen_Place.content and Area2 != Chosen_Place.content and Area3 != Chosen_Place.content:
            await ctx.send("Error #3, **timed out**. You have attempted to search an **invalid area**.")
        else:
            embed = discord.Embed(title = "Search Result", description = f"{User} have searched a place!", color = 0xFF5733)
            embed.add_field(name = "Searched Area", value = Chosen_Place.content, inline = True)
            embed.add_field(name = "Coins Found", value = "25", inline = True)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar)
            embed.set_footer(icon_url = client.user.avatar, text = "Ravu - Alpha v1.01")
            await ctx.send(embed=embed)
    except asyncio.TimeoutError:
        await ctx.send(Error("101").format(ctx.author.mention).format(user_mention))

@client.command()
async def gacha(ctx, Gacha_Roll):

    ## await ctx.send('Unfortunately this feature is currently under maintenance, it may be discontinued in favor of a much sophisticated feature in the near future. Thank you for your understanding and support for Ravu Bot!')

    try:

        ## Useful statistic
        Gacha_Rolled = 0

        Gacha_Tier_List = ["Ultra Rare"]
        Uncommon_Repetition = 995
        Rare_Repetition = 4

        Repetition_Count = 0
        while Repetition_Count < Uncommon_Repetition:
            Gacha_Tier_List.append("Uncommon")
            Repetition_Count += 1
        
        Repetition_Count = 0
        while Repetition_Count < Rare_Repetition:
            Gacha_Tier_List.append("Rare")
            Repetition_Count += 1


        await ctx.send("\nRewards:")

        while Gacha_Rolled < int(Gacha_Roll):
            Gacha_Rolled += 1

            ## So get the index of List of countries and get the country as a string in a variable

            Country = random.randrange(Gacha_List_Main.Gacha_Country_List)
            Tier = random.randrange(Gacha_List_Main.Gacha_Tier_List)

            ## A bit complicated but, Rarity first , Country, then Vehicle.
            def Rarity_Case(Case1):
                if Case1 == "Uncommon":
                    def Country_Case(Case2):
                        if Case2 == "USSR":
                            Country_Rarity = Gacha_List_Main.USSR_Uncommon
                        elif Case2 == "Germany":
                            Country_Rarity = Gacha_List_Main.Germany_Uncommon
                        else:
                            Country_Rarity = Gacha_List_Main.USA_Uncommon
                        return Country_Rarity
                    Country_Rarity = Country_Case(Country)
                    Vehicle = random.randrange(0,len(Country_Case(Country)))

                elif Case1 == "Rare":
                    def Country_Case(Case2):
                        if Case2 == "USSR":
                            Country_Rarity = Gacha_List_Main.USSR_Rare
                        elif Case2 == "Germany":
                            Country_Rarity = Gacha_List_Main.Germany_Rare
                        else:
                            Country_Rarity = Gacha_List_Main.USA_Rare
                        return Country_Rarity
                    Country_Rarity = Country_Case(Country)
                    Vehicle = random.randrange(0,len(Country_Case(Country)))

                else:
                    def Country_Case(Case2):
                        if Case2 == "USSR":
                            Country_Rarity = Gacha_List_Main.USSR_UltraRare
                        elif Case2 == "Germany":
                            Country_Rarity = Gacha_List_Main.Germany_UltraRare
                        else:
                            Country_Rarity = Gacha_List_Main.USA_UltraRare
                        return Country_Rarity
                    Country_Rarity = Country_Case(Country)
                    Vehicle = random.randrange(0,len(Country_Case(Country)))
                return Vehicle, Country_Rarity

            X,Y = Rarity_Case(Tier)
            await ctx.send(f"{Gacha_Rolled}. {Y[X]} ({Country}) ({Tier})")

        await ctx.send("Roll has been completed.")

    except asyncio.TimeoutError:
        await ctx.send(Error("101").format(ctx.author.mention))

### Economic related commands

#R register doesn't work after line 468 is true, works for line 474 and onwards
@client.command()
async def register(ctx):
    cursor.execute(f"SELECT * FROM user_stats WHERE User_ID = {ctx.author.id}")

    try:
        results = cursor.fetchall()
        # for row in results:
        #     User_Balance = row['User_Balance']
        
        # print(len(User_Balance))

        if len(results) == 0:
            sql = f"INSERT INTO user_stats (User_ID, User_Balance) VALUES ({ctx.author.id}, 100)"
            cursor.execute(sql)
            mydb.commit()
            
            await ctx.send(f"{ctx.author.mention} has been successfully registered")
        else:
            await ctx.send(f"Error, {ctx.author.mention} has already been registered")
    except:
        await ctx.send(Error("201").format(ctx.author.mention))

@client.command()
async def unregister(ctx):
    if ctx.author.id == '464965108955611137':
        try:
            cursor.execute(f"DELETE FROM user_stats WHERE User_ID = {ctx.author.id}")
            await ctx.send("User has been deleted.")
        except:
            await ctx.send(Error("201").format(ctx.author.mention))
    else:
        await ctx.send(Error("401").format(ctx.author.mention))

@client.command()
async def register_test(ctx):
    sql = f"INSERT INTO user_stats (User_ID, User_Balance) VALUES ({ctx.author.id}, 100)"
    cursor.execute(sql)
    mydb.commit()
            
    await ctx.send(f"{ctx.author.mention} has been successfully registered")


@client.command()
async def bal(ctx):
    cursor.execute(f"SELECT * FROM user_stats WHERE User_ID = {ctx.author.id}")

    try:
        results = cursor.fetchall()
        for row in results:
            User_Balance = row['User_Balance']

        print(results)

        embed = discord.Embed(title = "Financial Report", color = 0xFF5733)
        embed.add_field(name = "Balance", value = User_Balance, inline = True)
        embed.set_author(
                name = ctx.author,
                icon_url = ctx.author.avatar
            )
        embed.set_footer(icon_url = client.user.avatar, text = "Ravu - Alpha v1.01")
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        await ctx.send(Error("201").format(ctx.author.mention))

@client.command()
async def shutdown(ctx):
    if str(ctx.author.id) == '464965108955611137':
        await ctx.send("Ordered received, shutting down")
        print("Ravu has shutdown due to an absolute authorisation")
        exit()
    else: 
        await ctx.send("Bitch, you're not authorised to shut me down >:(")  

client.run(token)