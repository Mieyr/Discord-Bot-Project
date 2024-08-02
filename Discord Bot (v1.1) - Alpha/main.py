# INSTALL DISCORD LIBRARY
# sudo apt install python3-pip
# pip3 install discord.py

# Notes

# When ever its a command, must be @client.command()
# async def {Command}(ctx):

# To send message, use await ctx.send("{Message}")

from socket import timeout
from tabnanny import check
from discord.utils import get
import discord
import asyncio
import random
from discord.ext import commands
from discord import app_commands
import json
import logging
import logging.handlers 
import aiohttp
import os
import subprocess # For auto backup mysql

# import other .py files

import Search_Places_List # Import the list
import Gacha_List_Main
import embed_template
import sql_stuff as SQLs
import formula
import Card_functions
from sql_stuff import mydb, cursor

with open("config.json") as f:
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["PREFIX"]

intents = discord.Intents.default()
intents.message_content = True

# Loggers

Logger = logging.getLogger('discord')
Logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

Handler = logging.handlers.RotatingFileHandler(
    filename = 'discord.log',
    encoding = 'utf-8',
    maxBytes = 32 * 1024 * 1024, # 32 MiB
    backupCount = 5 # Rotate through 5 files
)

Dt_Fmt = '%Y-%m-%d %H:%M:%S'
Formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', Dt_Fmt, style='{')
Handler.setFormatter(Formatter)
Logger.addHandler(Handler)

# client = commands.Bot(command_prefix = prefix, intents = intents)

class RavuBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = prefix, intents = intents)

    # async def setup_hook(self):
    #     await self.tree.sync(guild = discord.Object(id=INSERT SERVER_ID)) # Loads the hybrid commands
    #     print(f"Synced slash commands for {self.user}.")
    
    # async def close(self):
    #     await super().close()
    #     await self.session.close()

    # def run(self):
    #     super().run(self.token, reconnect=True)

client = RavuBot()
client.remove_command('help') # Remove default help command

Cooldown_Error = "**On Cooldown**, {}, the command you\'ve attempted to execute is still on cooldown. Please try again in **{:.1f}s**"

# Database

@client.event
async def on_ready(): # On event that the client goes online
    print("{0.user} is ready to slave away!".format(client))
    await client.change_presence(activity=discord.Game("Ravu Development")) # Changes status

@client.event
async def on_disconnect():
    print("Back to the cage")

# Return the message for each code of error

def Error(Error_Code):
    if Error_Code == "101":
        Error_Message = "Error 101: {}, the command has timeout."
    elif Error_Code == "201":
        Error_Message = "Error 201: {}, an error has occured within a database command."
    elif Error_Code == "301":
        Error_Message = "**On Cooldown**, {}, the command you\'ve attempted to execute is still on cooldown. Please try again in **{:.1f}s**"
    elif Error_Code == "401":
        Error_Message = "Error 401: {}, you're not authorised to execute this command."
    elif Error_Code == "501":
        Error_Message = "Error 501: {}, you've made an invalid command argument."
    elif Error_Code == "601":
        Error_Message = "Error 601: {}, you've yet to register. Use `R register` beforehand."
    return Error_Message

# Command cooldown

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): # Checks whether the command is in cooldown
        Message = Error("301").format(ctx.author.mention, error.retry_after)
        await ctx.send(Message)

# @client.event
# async def on_message(ctx):
#     if ctx.author == client.user: # If message sender is bot then ignore
#         return

#     Roll = random.randrange(0,1000)
#     if Roll == 0:
#         Data = SQLs.Fetch_Data_Server(ctx.guild.id)
#         channel = client.get_channel(int(Data[2]))
#         await channel.send("A card has dropped!")

# Hello Command

@client.command()
async def hello(ctx):
    await ctx.send("Hello!!")
    await ctx.channel.purge(limit = 1)

# Card Help command

@client.command()
async def help(ctx):

    embed = discord.Embed(
        title = "Commands", 
        description = "List of commands for Ravu Bot.", 
        color = 0xFF5733
    )
    embed.add_field(
        name = "Economy",
        value = """
        `register` `balance` `search` `coinflip`
        """,
        inline = True
    )
    embed.add_field(
        name = "Card Utilities", 
        value = """
        `cardinfo` `daily` `vote` `salvage` `construct` `recover`
        """, 
        inline = True
    )
    embed.add_field(
        name = "Miscellaneous",
        value = '''
        `Error`
        ''',
        inline = False
    )
    embed.add_field(
        name = "Tips:",
        value = "Use *`R ch <command>`* to acquire more information regarding the command."
    )
    embed.set_author(
        name = ctx.author,
        icon_url = ctx.author.avatar
    )

    await ctx.send(embed=embed)

# For further info of a command
# Return message based on the argument of R ch <Argument/Command> 

@client.command()
async def ch(ctx, arg):

    Data = SQLs.Fetch_Command_Data(str(arg))
    embed = discord.Embed(
        title = f"Command Info: `R {arg}`", 
        description = f"""
        Shortcut: {Data[0]}
        Instruction: {Data[1]}

        {Data[2]}
        """, 
        color = 0xFF5733,
    )
    embed.set_author(
        name = ctx.author,
        icon_url = ctx.author.avatar
    )
    await ctx.send(embed=embed)

# Registration for games

@client.command()
async def register(ctx):

    Data = SQLs.Fetch_Data_User(ctx.author.id)

    try:
        if len(Data[1]) == 0:
            sql = f"INSERT INTO user_stats (User_ID) VALUES ({ctx.author.id})"
            cursor.execute(sql)
            mydb.commit()
            await ctx.send(f"{ctx.author.mention} has been successfully registered")
        else:
            await ctx.send(f"Error, {ctx.author.mention} has already been registered")
    except:
        await ctx.send(Error("201").format(ctx.author.mention)) # Database can't be called

# def User_Register_Check(ctx):
#     Data = SQLs.Fetch_Data_User(ctx.author.id)
#     if len(Data[2]) == 0:
#         Result = 'Y'
#     return Result # Checks if the user is registered, if yes then its not 0


@client.command(fallback = "Country:")
async def test(ctx, *, arg): # (arg) so can do country or specific tank info

    # Group divided based on country
    Input = arg.split(" ")
    print(Input)
    if len(Input) == 1:
        Data = Card_functions.Tank_List(Input[0])

        embed = discord.Embed(
            title = f"{Data[4]}'s Available Cards", 
            color = 0xFF5733
        )
        embed.add_field(
            name = 'Uncommon',
            value = Data[0],
            inline = True
        )
        embed.add_field(
            name = 'Rare',
            value = Data[1],
            inline = True
        )
        embed.add_field(
            name = 'Ultra Rare',
            value = Data[2],
            inline = True
        )
        embed.set_author(
            name = ctx.author,
            icon_url = ctx.author.avatar
        )
        embed.set_thumbnail(
            url = Data[3]
        )
        await ctx.send(embed=embed)

    # If len of input is 2, then it's requesting a specific tank info
    elif len(Input) == 2:
        Data = SQLs.Card_General_Data(Input[1])
        embed = discord.Embed(
            title = f'{Data[0]}', 
            description = f'{Data[1]}', 
            color = 0xFF5733
        )
        embed.add_field(
            name = 'Armament',
            value = f'''
            {Data[7]}
            {Data[8]}
            {Data[9]}''',
            inline = False
        )
        embed.add_field(
            name = 'Rarity',
            value = f'{Data[2]}',
            inline = True
        )
        embed.add_field(
            name = 'In service',
            value = f'{Data[4]}',
            inline = True
        )
        embed.add_field(
            name = 'Country',
            value = f'{Data[5]}',
            inline = True
        )
        embed.set_image(
            url = f"{Data[3]}"
        )
        embed.set_author(
            name = ctx.author,
            icon_url = ctx.author.avatar
        )
        embed.set_thumbnail(
            url = Data[6]
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send('Try different command lmao')

@client.command()
async def reminder(ctx, reason, time: int):
    print(ctx.author.mention)
    await ctx.send(f"I have set a reminder for {reason} in {time}")
    await asyncio.sleep(time)
    await ctx.send(f"{ctx.author.mention}, a friendly reminder: {reason}")

@client.command()
async def shutdown(ctx):
    if str(ctx.author.id) == 'INSERT USER_ID':
        await ctx.send("Ordered received, shutting down")
        print("Ravu has shutdown due to an absolute order")
        exit()
    else: 
        await ctx.send("WARNING! You're not authorised to shut me down >:(")  

# Loading/Booting cogs

async def load():
    for file in os.listdir('INSERT DIRECTORY'):
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await client.start(token, reconnect=True)


# async def database_backup():
#     # Set the path to the mysqldump command.
#     mysqldump_path = "INSERT DIRECTORY"

#     # Set the name of the database you want to backup.
#     database_name = "ravu_bot"

#     # Set the username and password for the database.
#     username = "root"
#     password = ""

#     # Set the path where you want to save the backup file.
#     backup_path = "INSERT DIRECTORY"

#     command = [
#         mysqldump_path,
#         "-u", username,
#         "-p" + password,
#         database_name,
#         ">", backup_path + "/" + database_name + ".sql"
#     ]

#     # Run the command using the subprocess module.
#     subprocess.run(command)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(database_backup())
# loop.run_forever()

# from cogs.EconomyCog import EconomyCog
asyncio.run(main())
