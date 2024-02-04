import pandas as pd
import xlsxwriter

xls = pd.ExcelFile('~/Downloads/Coding Projects/Discord Bot/Discord Bot(v1.02) - Alpha/Ravu_Bot.xlsx')
sheet_name = xls.sheet_names
df = pd.read_excel(xls, 'Users Balance', index_col=0, usecols='A')
money = list(df)
print(money[0])