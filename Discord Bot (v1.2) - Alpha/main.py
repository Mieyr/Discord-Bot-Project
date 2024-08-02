# INSTALL DISCORD LIBRARY
# sudo apt install python3-pip
# pip3 install discord.py

# Notes

# When ever its a command, must be @client.command()
# async def {Command}(ctx):

# To send message, use await ctx.send("{Message}")

from socket import timeout
from tabnanny import check

# Discord dependant/Libraries
from discord.ext import commands
from discord.utils import get
import discord
import asyncio
import subprocess

import json
import logging
import logging.handlers 
import os

# import other .py files
import SQL
import Card_functions
from SQL import mydb, cursor

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the config file
config_path = os.path.join(script_dir, 'config.json')

try:
    with open(config_path, 'r') as f:
        data = json.load(f)
        token = data["TOKEN"]
        prefix = data["PREFIX"]
except FileNotFoundError:
    print(f"Error: {config_path} not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

intents = discord.Intents.default()
intents.message_content = True

# Loggers

## Will only logs users with specific IDs
ALLOWED_USER_IDS = ["INSERT USER_ID"] # Redact

## Define the directory of the logs and its name
Log_Directory = 'INSERT DIRECTORY' # Redact
Log_Filename = 'discord.log'
Log_Path = os.path.join(Log_Directory, Log_Filename)

## Checks if a folder for logs exist
if not os.path.exists(Log_Directory):
    os.makedirs(Log_Directory)
    print(f"Created log directory: {Log_Directory}")

## Initialize logging
Logger = logging.getLogger('discord')
Logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

## Remove existing handlers if any
if Logger.hasHandlers():
    for handler in Logger.handlers[:]:
        Logger.removeHandler(handler)

## Add new handler
Handler = logging.handlers.RotatingFileHandler(
    filename=Log_Path,
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024, # 32 MiB
    backupCount=5 # Rotate through 5 files
)

Dt_Fmt = '%Y-%m-%d %H:%M:%S'
Formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', Dt_Fmt, style='{')
Handler.setFormatter(Formatter)
Logger.addHandler(Handler)

## Custom log function

def custom_log(ctx, message, level=logging.INFO):
    try:
        if str(ctx.author.id) in ALLOWED_USER_IDS:
            if level == logging.INFO:
                Logger.info(message)
            elif level == logging.ERROR:
                Logger.error(message)
            elif level == logging.DEBUG:
                Logger.debug(message)
            elif level == logging.WARNING:
                Logger.warning(message)
            elif level == logging.CRITICAL:
                Logger.critical(message)
    except Exception as e:
        print(f"Logging error: {e}")

class RavuBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = prefix, intents = intents)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id='INSERT SERVER_ID')) # Register commands globally # Redact
        print(f"Synced slash commands for {self.user}.")
        commands = await self.tree.fetch_commands()
        for command in commands:
            print(f"Command registered: {command.name}")
    
    async def close(self):
        await super().close()
        await self.session.close()

client = RavuBot()
client.remove_command('help') # Removes default help command

Cooldown_Error = "**On Cooldown**, {}, the command you\'ve attempted to execute is still on cooldown. Please try again in **{:.1f}s**"

# Database

@client.event
async def on_disconnect():
    print("Back to the cage")

def Error(Error_Code, *Args):
    Error_Messages = {
        "101": "Error 101: {}, the command has timeout.",
        "201": "Error 201: {}, an error has occurred within a database command.",
        "301": "**On Cooldown**, {}, the command you\'ve attempted to execute is still on cooldown. Please try again in **{:.1f}s**",
        "401": "Error 401: {}, you're not authorized to execute this command.",
        "501": "Error 501: {}, you've made an invalid command argument.",
        "601": "Error 601: {}, you've yet to register. Use `R register` beforehand."
    }

    # Get the error message template based on the error code
    Error_Message = Error_Messages.get(Error_Code, "Unknown error code: {}")
    
    # Format the message with additional arguments
    return Error_Message.format(*Args)

# Command cooldown

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): # Checks whether the command is in cooldown
        Message = Error("301").format(ctx.author.mention, error.retry_after)
        await ctx.send(Message)

# Periodic card drop system (in development)

# @client.event
# async def on_message(ctx):
#     if ctx.author == client.user: # If message sender is bot then ignore
#         return

#     Roll = random.randrange(0,1000)
#     if Roll == 0:
#         Data = SQL.Fetch_Data_Server(ctx.guild.id)
#         channel = client.get_channel(int(Data[2]))
#         await channel.send("A card has dropped!")

# Hello Command

@client.command()
async def hello(ctx):
    await ctx.send("Hello!!")
    # await ctx.channel.purge(limit = 1)

# Card Help command

@client.command()
async def help(ctx):
    custom_log(ctx, f"Help command called by {ctx.author}")
    
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
    custom_log(ctx, f"'Command Help' command called by {ctx.author}")
    
    Data = SQL.Fetch_Command_Data(str(arg))
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
    custom_log(ctx, f"Register command called by {ctx.author}")
    
    try:
        cursor.execute(f"SELECT * FROM user_stats WHERE User_ID = {ctx.author.id}")
        results = cursor.fetchall()
        custom_log(ctx, f"Fetched data for {ctx.author}: {results}")
        
        if not results: # Checks if there's no data found
            custom_log(ctx, "No registered data found in database, registering now")
            
            sql = f"INSERT INTO user_stats (User_ID) VALUES ({ctx.author.id})"
            cursor.execute(sql)
            mydb.commit()
            
            await ctx.send(f"{ctx.author.mention} has been successfully registered")
        else: # Existing data for user is found
            await ctx.send(f"Error, {ctx.author.mention} has already been registered")
            
    except Exception as e:
        Logger.error(f"Exception occurred while registering user {ctx.author.id}: {e}")
        await ctx.send(Error("201").format(ctx.author.mention)) # Database can't be called

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
        Data = SQL.Card_General_Data(Input[1])
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
    if str(ctx.author.id) == 'INSERT USER_ID': # Redact
        await ctx.send("Ordered received, shutting down")
        print("Ravu has shutdown due to an absolute order")
        exit()
    else: 
        await ctx.send("WARNING! You're not authorised to shut me down >:(")  

async def database_backup():
    # Set the path to the mysqldump command.
    mysqldump_path = "INSERT DIRECTORY"  # Include the executable name # Redact

    database_name = "INSERT DATABASE" # Redact
    host = "INSERT HOST NAME" # Redact
    username = "INSERT USERNAME" # Redact
    password = "INSERT PASSWORD" # Redact

    # Directory and file format
    backup_directory = "INSERT DIRECTORY" # Redact
    backup_path = os.path.join(backup_directory, f"{database_name}.sql")

    # Ensure the backup directory exists
    os.makedirs(backup_directory, exist_ok=True)

    # Access for the database
    command = [
        mysqldump_path,
        "-h", host,
        "-u", username,
        f"-p{password}",  # Note: There should be no space between -p and the password
        database_name
    ]

    # Run the command using subprocess with output redirection
    with open(backup_path, 'wb') as backup_file:
        result = subprocess.run(command, stdout=backup_file, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")
    else:
        print("Backup completed successfully.")

# Schedules database backup
async def scheduled_backup(interval_hours):
    while True:
        await database_backup()
        await asyncio.sleep(interval_hours * 3600)

@client.event
async def on_ready(): # On event that the client goes online
    print("{0.user} is ready to slave away!".format(client))    
    await client.change_presence(activity=discord.Game("Ravu Development")) # Changes status
    await load()
    
    client.loop.create_task(scheduled_backup(interval_hours=1)) # Schedules backup every hour

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        Logger.error(f"Command error: {error}")
        raise error
    
# Loading/Booting cogs

async def load():
    for file in os.listdir('INSERT DIRECTORY'): # Redact
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')

# from cogs.EconomyCog import EconomyCog
if __name__ == "__main__":
    client.run(token)  # Replace with your bot's token