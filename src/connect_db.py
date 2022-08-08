import pymysql
import pandas as pd

user = 'root'
password = 'password'
host = 'host'
port = '3306'
database = 'db_name'

command = """
SELECT * from parts
"""

import mysql.connector

mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)

mycursor = mydb.cursor()

sql = """
SELECT part_number, stock from parts
"""

df = pd.read_sql(sql, mydb)

part_number_test = [
    ['12003', 20],
    ['1247', 13],
]

mask = df['part_number'] == part_number_test[0][0]
df.at[df.index[mask], 'stock'] = df[mask]['stock'].astype(float) - 20 

# Write new column into parts_history
new_column = "ALTER TABLE parts_history \
            ADD stock_08_07_2022 int"
# execute the query
mycursor.execute(new_column)

# update new column with df stock values
sql_insert_values = """
INSERT INTO parts_history (stock_08_07_2022) VALUES (%s)
"""
data = [(x,) for x in df['stock']]
mycursor.executemany(sql_insert_values, data)