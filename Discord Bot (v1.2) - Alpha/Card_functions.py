import Gacha_List_Main
import discord

def Tank_List(Argument):

    Uncommon_List = ""
    Rare_List = ""
    UltraRare_List = ""

    def Import(Country):
        if Country == "Germany" or "germany":
            Country_Uncommon = Gacha_List_Main.Germany_Uncommon
            Country_Rare = Gacha_List_Main.Germany_Rare
            Country_UltraRare = Gacha_List_Main.Germany_UltraRare
            Country_Image = Gacha_List_Main.Gacha_Country_List[0][1]
            Country_Name = "Germany"
        elif Country == "USSR" or "ussr":
            Country_Uncommon = Gacha_List_Main.USSR_Uncommon
            Country_Rare = Gacha_List_Main.USSR_Rare
            Country_UltraRare = Gacha_List_Main.USSR_UltraRare
            Country_Image = Gacha_List_Main.Gacha_Country_List[1][1]
            Country_Name = "USSR"
        elif Country == "USA" or "usa":
            Country_Uncommon = Gacha_List_Main.USA_Uncommon
            Country_Rare = Gacha_List_Main.USA_Rare
            Country_UltraRare = Gacha_List_Main.USA_UltraRare
            Country_Image = Gacha_List_Main.Gacha_Country_List[2][1]
            Country_Name = "USA"
        return Country_Uncommon, Country_Rare, Country_UltraRare, Country_Image, Country_Name

    Imported_Data = Import(Argument)
    Country_Image = Imported_Data[3]
    Country_Name = Imported_Data[4]

    Tank_Code = 1
    Tank_Index = 0

    # Keep doing until Tank_Index is no longer less than length of the list
    while Tank_Index < len(Imported_Data[0]):

        # Get uncommon_list and enter, then tank_code and the tank name from list. Then put into the variable, stacking it up
        Uncommon_List = f'{Uncommon_List}\n{Tank_Code}. {(Imported_Data[0])[Tank_Index]}'
        Tank_Code += 1
        Tank_Index += 1

    Tank_Index = 0
    while Tank_Index < len(Imported_Data[1]):
        Rare_List = f'{Rare_List}\n{Tank_Code}. {(Imported_Data[1])[Tank_Index]}'
        Tank_Code += 1
        Tank_Index += 1

    Tank_Index = 0
    while Tank_Index < len(Imported_Data[2]):
        UltraRare_List = f'{UltraRare_List}\n{Tank_Code}. {(Imported_Data[2])[Tank_Index]}'
        Tank_Code += 1
        Tank_Index += 1

    Argument = ""
    return Uncommon_List, Rare_List, UltraRare_List, Country_Image, Country_Name