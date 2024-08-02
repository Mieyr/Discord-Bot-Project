import discord
import formula
import SQL as SQL
import random
import Searchable_Area_List
import asyncio

from SQL import cursor, mydb
from main import Error, Logger
import main
from discord.ext import commands
from discord import app_commands

# Constant Variable and Lists
coin_sides = ["head", "tail"]
coin_multiplier_win = 1
coin_multiplier_loss = -1

class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        Logger.info("Economy Cog is running")

    # Balance

    @main.client.hybrid_command(name="balance", aliases=["bal"], with_app_command=True, description="Checks your balance")
    async def balance(self, ctx):
        Logger.info("Balance command called")
        
        try:
            Data = SQL.Fetch_Data_User(ctx.author.id)

            # embed = embed_template.Embed_Template_Finance("Financial Report", "Balance", Data)
            # await ctx.send(embed=embed)
            embed = discord.Embed(
                title = "Financial Report", 
                description = f"**Balance**: {formula.Number_translate(Data[0])}",
                color = 0xFF5733
                )
            embed.set_author(
                    name = ctx.author,
                    icon_url = ctx.author.avatar
                )
            await ctx.send(embed=embed)

        except Exception:
            await ctx.send(Error("201").format(ctx.author.mention))

# Coinflip

    # @main.client.hybrid_command(name = 'coinflip', description = "Flip a coin")
    # @app_commands.guilds(discord.Object(id = 762859199146491944))
    @commands.command(aliases = ['cf'])
    async def coinflip(self, ctx, bet: int, guess):
        Logger.info("Coinflip command called")
        
        lower_guess = guess.lower()
        
        if lower_guess not in coin_sides:
            await ctx.send("Please guess 'head' or 'tail'.")
            return
        try:
            Data = SQL.Fetch_Data_User(ctx.author.id)
            
            if Data[0] < bet: # Check if balance is less than bet
                await ctx.send("{}, you've an insufficient balance.".format(ctx.author.mention))
                return
            
            Logger.info("Data checked, balance sufficient")
            
            def get_multiplier(flip_result, lower_guess):
                return coin_multiplier_win if flip_result == lower_guess else coin_multiplier_loss
            
            flip_result = random.choice(coin_sides)
            multiplier = get_multiplier(flip_result, lower_guess)
            Winning = bet*multiplier
            
            result_message = f"The coin landed on {flip_result}!"
            
            if multiplier == coin_multiplier_win:
                embed_result_message = f"You won {formula.Number_translate(Winning)} coins!"    
            else:
                embed_result_message = f"You lost {formula.Number_translate(Winning)} coins!"
            
            #Run SQL balance update
            New_Balance = int(Data[0]) + Winning
            
            Query = SQL.Update_User(New_Balance, ctx.author.id, Data[2])
            SQL.cursor.execute(Query[0], Query[1])
            SQL.mydb.commit()

            embed = discord.Embed(
                title = "Coinflip Result", 
                color = 0xFF5733
                )
            embed.add_field(
                name = "Result",
                value = f"{result_message} {embed_result_message}", # amount is a text from user, so int(amount)
                )
            embed.set_author(
                    name = ctx.author,
                    icon_url = ctx.author.avatar
                )

            await ctx.send(embed=embed)

        except Exception:
            await ctx.send(Error("201").format(ctx.author.mention)) # Something is wrong with sql

# Search

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def search(self, ctx):
        Logger.info("Search command called")

        # if User_Register_Check(ctx) == True:
        #     await ctx.send(Error("601").format(ctx.author.mention)) # Not registered
        #     return
        
        area_options = []
        while len(area_options) < 3:
            random_area = random.choice(Searchable_Area_List.Area)
            if random_area not in area_options:
                area_options.append(random_area)

        embed = discord.Embed(
            title = "Area To Search", 
            description = f"""
        1. {area_options[0]}
        2. {area_options[1]}
        3. {area_options[2]}""",
        color = 0xFF5733)

        embed.set_author(
            name = ctx.author, 
            icon_url = ctx.author.avatar
            )
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author.id == ctx.author.id

        try:
            selected_area = await main.client.wait_for("message", timeout = 10, check=check)
            if selected_area.content not in area_options:
                await ctx.send("Error #3, **timed out**. You have attempted to search an **invalid area**.")
            else:
                Finding = 20*formula.generate_multiplier() # Base coin reward * Random Coin Multiplier
                Data = SQL.Fetch_Data_User(ctx.author.id)
                New_Balance = Data[0] + round(Finding)

                Query = SQL.Update_User(New_Balance, ctx.author.id, Data[1]+1)
                cursor.execute(Query[0], Query[1])
                mydb.commit()

                embed = discord.Embed(
                    title = "Search Result",
                    description = f"""**Searched Area**: {selected_area.content}
                    **Coins Found**: {Finding}""",
                    color = 0xFF5733
                )
                embed.set_author(
                    name = ctx.author, 
                    icon_url = ctx.author.avatar
                    )
                await ctx.send(embed=embed)
                
        except asyncio.TimeoutError:
            await ctx.send(Error("101").format(ctx.author.mention).format(ctx.author.mention))


    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        Logger.info("Daily command called")
        try:
            Data = SQL.Fetch_Data_User(ctx.author.id)
            generate_daily_reward = random.randint(10,19) * 10 + random.randint(1,10) # First value makes up 2 digit of 4
            daily_reward = generate_daily_reward * 10 # Multiply result by 10 so the last digit is always 0
            New_Balance = Data[0] + daily_reward
            
            print(New_Balance)

            Query = SQL.Update_User(New_Balance, ctx.author.id)
            cursor.execute(Query[0], Query[1])
            mydb.commit()
            
            print("lol")

            embed = discord.Embed(
                title = "Daily Claimed",
                description = f"**Reward**: {daily_reward}",
                color = 0xFF5733
            )
            embed.set_author(
                name = ctx.author, 
                icon_url = ctx.author.avatar
            )
            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send(Error("201").format(ctx.author.mention).format(ctx.author.mention))


async def setup(client):
    await client.add_cog(EconomyCog(client))