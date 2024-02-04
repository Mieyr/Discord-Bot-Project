import discord
from discord.ext import commands
import json
import main
import Gacha_List_Main

def Embed_Template_Finance(Embed_Title, Description, ctx):
    embed = discord.Embed(
        title = Embed_Title,
        description = Description,
        color = 0xFF5733
    )
    embed.set_author(
        name = ctx.author,
        icon_url = ctx.author.avatar
    )

    return embed

def Card_Country(Country, Value1, Value2, Value3, ctx):
    embed = discord.Embed(
        title = f"{Country}'s Available Cards", 
        color = 0xFF5733
    )
    embed.add_field(
        name = 'Uncommon',
        value = f'{Value1}',
        inline = True
    )
    embed.add_field(
        name = 'Rare',
        value = f'{Value2}',
        inline = True
    )
    embed.add_field(
        name = 'Ultra Rare',
        value = f'{Value3}',
        inline = True
    )
    embed.set_author(
        name = ctx.author,
        icon_url = ctx.author.avatar
    )
    embed.set_thumbnail(
        url = str(Gacha_List_Main.Gacha_Country_List_2[0][1])
    )
    return embed