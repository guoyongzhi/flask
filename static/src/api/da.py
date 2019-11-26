import sqlite3
conn = sqlite3.connect(r'G:\work\flask\dbdate')

print("Opened database successfully")
cursor = conn.execute("SELECT * from passport;")
for row in cursor:
   print("ID = ", row[0])
   print("NAME = ", row[1])
   print("number = ", row[2])

print("Operation done successfully")
conn.close()
