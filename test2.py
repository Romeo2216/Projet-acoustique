import sqlite3

connection = sqlite3.connect("test.db")

print(connection.total_changes)

cursor = connection.cursor()

"""cursor.execute("CREATE TABLE IF NOT EXISTS Excitation_Files (id INTEGER, name TEXT)")

cursor.execute("INSERT INTO Excitation_Files VALUES (1, 'ssss')")"""


connection.commit()

cursor.execute("SELECT * FROM Excitation_Files")
rows = cursor.fetchall()
for row in rows:
    print(row)

a,b = rows[0]
print(b)