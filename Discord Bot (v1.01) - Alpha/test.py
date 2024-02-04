import random
from openpyxl import Workbook
import pandas as pd
import xlsxwriter

Alpha = '5000000'
Alpha_Len = len(Alpha)
Number_of_split = int(Alpha_Len / 3)
Left_over = Alpha_Len % 3
print(Number_of_split)
number = list(Alpha)

print(number)
print(Left_over)

Split = True
number_Index = 6
new_number = []
While_left_over = 0
While_Term = 0
while While_left_over < Left_over:
    while While_Term < Number_of_split:
        new_number.append(number[number_Index])
        number_Index -= 1
        new_number.append(number[number_Index])
        number_Index -= 1
        new_number.append(number[number_Index])
        number_Index -= 1
        While_Term += 1
        new_number.append(',')
    new_number.append(number[number_Index])
    While_left_over += 1

new_number.reverse()
True_Number = ('').join(new_number)
print(True_Number)

workbook = xlsxwriter.Workbook('Ravu_Bot.xlsx')
worksheet = workbook.add_worksheet('Users Balance')

worksheet.write('A1','UserID')
worksheet.write('B1', 'Pocket Bal')
worksheet.write('C1', 'Bank Bal')
worksheet.write('D1', 'Net Worth')
workbook.read_only

rowIndex = 2

for row in range(100):

    UserID = random.randrange(10000,10000000)
    PocketBal = random.randrange(100,1000000)
    BankBal = random.randrange(100,1000000)
    NetWorth = PocketBal + BankBal

    worksheet.write('A' + str(rowIndex), UserID)
    worksheet.write('B' + str(rowIndex), PocketBal)
    worksheet.write('C' + str(rowIndex), BankBal)
    worksheet.write('D' + str(rowIndex), NetWorth)
    
    rowIndex += 1
workbook.close()