import discord
import asyncio

from main import Error, client
import sql_stuff as SQLs

from sql_stuff import mydb, cursor

from discord.ext import commands
from discord import app_commands

class CardCog(commands.Cog):
    def __init__(self, client):
        self.client = client


    # Confirmation to make a card drop zone/channel for Tanks Card

    @commands.command(pass_context = True, aliases = ['sc'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_permissions(administrator = True) # Checks if the executor of the command has admin perms
    async def setup_card(self, ctx):

        try: 
            embed = discord.Embed(
                title = "Confirmation", 
                description = "Do you confirm to make this channel the designated (new) card drop zone?", 
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
            
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('👍')
            
            try:
                # the wait_for will only register if the following conditions are met
                def check(reaction, user):
                    return user.id == ctx.author.id and str(reaction) == '👍'

                # timeout kwarg is optional
                reaction, user = await client.wait_for("reaction_add", check=check, timeout=30)

                Server_id = ctx.guild.id # Get the server_id
                Channel_id = ctx.channel.id # Get the Channel id

                try:
                
                    Data = SQLs.Fetch_Data_Server(Server_id)
                    if len(Data) == 0:
                        Query = SQLs.Insert_Server(Server_id, Channel_id)
                        Message = "I have confirmed this channel as the card drop zone!"
                    else:
                        Query = SQLs.Update_Server(Server_id, Channel_id) 
                        Message = "I have updated this channel as the card drop zone" 
                    cursor.execute(Query[0], Query[1])
                    mydb.commit()

                except asyncio.TimeoutError:
                    await ctx.send(Error("201").format(ctx.author.mention))

                # then execute your code here if the author reacts, like so:
                await ctx.send(Message)

            except asyncio.TimeoutError:
                await ctx.send(Error("201").format(ctx.author.mention))

        except:
            await ctx.send(Error("101").format(ctx.author.mention))


    # @commands.command()
    # async def daily

async def setup(client):
    await client.add_cog(CardCog(client))