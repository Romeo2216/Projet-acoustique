import sqlite3

connection = sqlite3.connect("test.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Impulse_Reponse (id INTEGER, file_name TEXT)")

import os

# Specify the folder path
folder_path = "Impulse_Reponse"

# List all files in the folder
files = os.listdir(folder_path)

for file in files:

    cursor.execute("INSERT OR IGNORE INTO Impulse_Reponse (file_name) VALUES (?)", (file,))


connection.commit()

