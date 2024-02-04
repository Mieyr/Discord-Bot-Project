import discord
import formula
import sql_stuff as SQLs
import random
import Search_Places_List
import asyncio
import aiohttp

from sql_stuff import cursor, mydb
from main import Error#, User_Register_Check
import main
from discord.ext import commands
from discord import app_commands

class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

# Balance

    # @main.client.hybrid_command(name = "ping", with_app_command= True, description = "Checks your balance")
    # @app_commands.guilds(discord.Object(id = 762859199146491944))
    @commands.command(aliases = ['bal'])
    async def balance(self, ctx):
        try:
            Data = SQLs.Fetch_Data_User(ctx.author.id)

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
    async def coinflip(self, ctx, amount: int, guess):
        lower_guess = guess.lower()
        Flip = ["head", "tail"]
        try:
            Data = SQLs.Fetch_Data_User(ctx.author.id)
            if Data[0] >= amount:
                if lower_guess == "head" or lower_guess == "tail":

                    def Case(Flipped):
                        if Flipped == lower_guess:
                            Mutliplier = 1
                        else:
                            Mutliplier = -1
                        return Mutliplier

                    Multiplier = Case(random.choice(Flip)) # Random 50/50 1 (head), 2(tail)
                    Winning = amount*Multiplier
                    New_Balance = int(Data[0]) + Winning
                    
                    Query = SQLs.Update_User(New_Balance, ctx.author.id, Data[2])
                    SQLs.cursor.execute(Query[0], Query[1])

                    SQLs.mydb.commit()

                    embed = discord.Embed(
                        title = "Coinflip Result", 
                        color = 0xFF5733
                        )
                    embed.add_field(
                        name = "Result",
                        value = f"You won {formula.Number_translate(Winning)} coins!", # amount is a text from user, so int(amount)
                        )
                    embed.set_author(
                            name = ctx.author,
                            icon_url = ctx.author.avatar
                        )

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(Error("501").format(ctx.author.mention)) # Has to be head or tail
            else:
                await ctx.send("{}, you've an insufficient balance.".format(ctx.author.mention)) # Balance has to be more than balance

        except Exception:
            await ctx.send(Error("201").format(ctx.author.mention)) # Something is wrong with sql

# Search

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def search(self, ctx):

        # if User_Register_Check(ctx) == True:
        #     await ctx.send(Error("601").format(ctx.author.mention)) # Not registered
        #     return
        
        Area = []
        while len(Area) < 3:
            place = random.choice(Search_Places_List.Area)
            if place not in Area:
                Area.append(place)
        print(Area)

        embed = discord.Embed(
            title = "Area To Search", 
            description = f"""
        1. {Area[0]}
        2. {Area[1]}
        3. {Area[2]}""",
        color = 0xFF5733)

        embed.set_author(
            name = ctx.author, 
            icon_url = ctx.author.avatar
            )
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author.id == ctx.author.id

        try:
            Chosen_Place = await main.client.wait_for("message", timeout = 10, check=check)
            if Chosen_Place.content not in Area:
                await ctx.send("Error #3, **timed out**. You have attempted to search an **invalid area**.")
            else:
                Finding = formula.Search_base*formula.Search_multiplier
                Data = SQLs.Fetch_Data_User(ctx.author.id)
                New_Balance = Data[0] + round(Finding)

                Query = SQLs.Update_User(New_Balance, ctx.author.id, Data[1]+1)
                cursor.execute(Query[0], Query[1])
                mydb.commit()

                embed = discord.Embed(
                    title = "Search Result",
                    description = f"""**Searched Area**: {Chosen_Place.content}
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
        try:
            Data = SQLs.Fetch_Data_User(ctx.author.id)
            Daily_Reward = random.randrange(1000,2000)
            New_Balance = Data[0] + Daily_Reward
            
            print(New_Balance)

            Query = SQLs.Update_User(New_Balance, ctx.author.id)
            cursor.execute(Query[0], Query[1])
            mydb.commit()
            
            print("lol")

            embed = discord.Embed(
                title = "Daily Claimed",
                description = f"**Reward**: {Daily_Reward}",
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