import sqlite3

conn = sqlite3.connect('dbdate')
c = conn.cursor()
print("Opened database successfully")

# c.execute("alter table COMPANY t_app modify column ID int(5) auto_increment;")
# c.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
#       VALUES ('Paull', 13, 'California', 20000.00 )")
# cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#    print("ID = ", row[0])
#    print("NAME = ", row[1])
#    print("ADDRESS = ", row[2])
#    print("SALARY = ", row[3], "\n")

print("Operation done successfully")

conn.close()