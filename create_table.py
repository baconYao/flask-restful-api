import sqlite3

# 資料會存在data.db檔案
connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# 建立名為users的table，其欄位有id(自動新增的Primary Key) username 和 password
create_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)
# 建立名為items的table，其欄位有id(自動新增的Primary Key) name 和 price (real是浮點數的一種表示)
create_table = "CREATE TABLE items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# save to disk
connection.commit()

connection.close()