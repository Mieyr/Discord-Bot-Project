from unittest import result
import mysql.connector

try:
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'ravu_bot'
    )

    cursor = mydb.cursor(dictionary=True)
except:
    print("Unable to connect to the database")

# User Related Stuff

def Update_User(New_Balance, author_id, User_Coin_Multiplier):
    Sql = "UPDATE user_stats SET Balance = %s, User_Coin_Multiplier = %s WHERE User_ID = %s"
    Data_Tuple = (New_Balance, User_Coin_Multiplier, author_id)
    return Sql, Data_Tuple

def Insert_User(author_id):
    Sql = "INSERT INTO `user_stats`(`User_ID`) VALUES (%s)"
    Data_Tuple = (author_id)
    return Sql, Data_Tuple

def Fetch_Data_User(author_id):
    cursor.execute(f"SELECT * FROM user_stats WHERE User_ID = {author_id}") # No need prepared statement (Doesn't take input)
    results = cursor.fetchall()
    for row in results:
        Balance = row['Balance']
        User_Coin_Multiplier = row['User_Coin_Multiplier']
    return int(Balance), results, User_Coin_Multiplier




# Server Stuff

def Insert_Server(Sever_id, Channel_id):
    Sql = "INSERT server_informations SET Server_ID = %s, Channel_ID = %s"
    Data_Tuple = (Sever_id, Channel_id)
    return Sql, Data_Tuple

def Fetch_Data_Server(Sever_id):
    cursor.execute(f"SELECT * FROM server_informations WHERE Server_ID = {Sever_id}")
    results = cursor.fetchall()
    for row in results:
        Server_ID = row['Server_ID']
        Channel_ID = row['Channel_ID']
    return results, Server_ID, Channel_ID # Returning the length of "results", if 0 then there's no match

def Update_Server(Server_id, Channel_id):
    Sql = "UPDATE server_informations SET Channel_ID = %s WHERE Server_ID = %s"
    Data_Tuple = (Channel_id, Server_id)
    return Sql, Data_Tuple




# Card Related stuff

def Card_General_Data(Card_ID):

    # General info table
    cursor.execute(f"SELECT * FROM card_informations t1, rarity_table t2, card_stats t3, country_info t4 WHERE t1.Card_ID = {Card_ID} AND t2.Rarity_ID = t1.Rarity_ID AND t3.Card_ID = {Card_ID} AND t1.Country_ID = t4.Country_ID")
    results = cursor.fetchall()
    for row in results:
        print(row)
        Card_Name = row['Card_Name']
        Card_Description = row['Card_Description']
        Rarity = row['Rarity']
        Image_URL = row['Image_URL']
        In_Service = row['Card_In_Service']
        Country_Name = row['Country_Name']
        Country_Image_URL = row['Country_Image_URL']
        Card_Armament_1 = row['Card_Armament_1']
        Card_Armament_2 = row['Card_Armament_2']
        Card_Armament_3 = row['Card_Armament_3']
    return Card_Name, Card_Description, Rarity, Image_URL, In_Service, Country_Name, Country_Image_URL, Card_Armament_1, Card_Armament_2, Card_Armament_3

# Rarity table

def Card_Rarity_Data(Rarity_ID):   
    cursor.execute(f"SELECT * FROM rarity_table WHERE Rarity_ID = {Rarity_ID}")
    result_2 = cursor.fetchall()
    for row in result_2:
        Rarity = row['Rarity']
    return Rarity

# Card Stats table (In service)

def Card_Stats_Data(Card_ID):
    cursor.execute(f"SELECT * FROM card_stats WHERE Card_ID = {Card_ID}")
    results = cursor.fetchall()
    for row in results:
        In_Service = row['Card_In_Service']
    return In_Service

# Command Related

def Fetch_Command_Data(Command):
    cursor.execute(f"SELECT * FROM command_info WHERE Command = '{Command}'")
    results = cursor.fetchall()
    for row in results:
        Shortcut = row['Shortcut']
        Instruction = row['Instruction']
        Description = row['Description']
    return Shortcut, Instruction, Description