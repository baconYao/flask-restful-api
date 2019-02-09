import sqlite3

# 資料會存在data.db檔案
connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# 建立名為users的table，其欄位有id username 和 password
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)


users = [
    (2, 'yao', 'qaz'),
    (3, 'judy', 'qaz'),
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# save to disk
connection.commit()

connection.close()