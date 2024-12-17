import sqlite3
import os
from itertools import product
import numpy as np
import signal_manager as sm


connection = sqlite3.connect("signal.db", check_same_thread=False)

cursor = connection.cursor()

def _init_db(): 

    cursor.execute("CREATE TABLE IF NOT EXISTS Impulse_Response (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Excitation_Files (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS HRTF (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS OBTF (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Combination (id INTEGER PRIMARY KEY  AUTOINCREMENT, `excitation_file` TEXT REFERENCES `Excitation_Files`(`file_name`), `hrtf` TEXT REFERENCES `HRTF`(`file_name`), `obtf` TEXT REFERENCES `OBTF`(`file_name`), `impulse_response` TEXT REFERENCES `Impulse_Response`(`file_name`),`signal_file_name` TEXT, UNIQUE(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Test_order (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `signal_1_id` INTEGER REFERENCES `Combination`(`id`), `signal_2_id` INTEGER REFERENCES `Combination`(`id`), `signal_X` INTEGER, `signal_A_B` INTEGER, UNIQUE(id))")

    folder_path = "Impulse_Response"

    files = os.listdir(folder_path)

    for file in files:
        cursor.execute("INSERT OR IGNORE INTO Impulse_Response (file_name) VALUES (?)", (file,))

    folder_path = "Excitation_Files"

    files = os.listdir(folder_path)

    for file in files:
        cursor.execute("INSERT OR IGNORE INTO Excitation_Files (file_name) VALUES (?)", (file,))

    folder_path = "HRTF"

    files = os.listdir(folder_path)

    for file in files:
        cursor.execute("INSERT OR IGNORE INTO HRTF (file_name) VALUES (?)", (file,))

    folder_path = "OBTF"

    files = os.listdir(folder_path)

    for file in files:
        cursor.execute("INSERT OR IGNORE INTO OBTF (file_name) VALUES (?)", (file,))

    connection.commit()

def get_file_name(i, table):

    cursor.execute("SELECT * FROM " + table)
    rows = cursor.fetchall()
    row = rows[i]
    file_name = row[1]

    return "".join(file_name)

def save_conbination():

    cursor.execute("SELECT * FROM Excitation_Files")
    rows = cursor.fetchall()

    nb_of_exi = len(rows)

    cursor.execute("SELECT * FROM HRTF")
    rows = cursor.fetchall()

    nb_of_hrtf = len(rows)

    cursor.execute("SELECT * FROM OBTF")
    rows = cursor.fetchall()

    nb_of_obtf = len(rows)

    cursor.execute("SELECT * FROM Impulse_Response")
    rows = cursor.fetchall()

    nb_of_i_reponse = len(rows)

    # Définir les plages de chaque position
    range1 = range(0, nb_of_exi) 
    range2 = range(0, nb_of_hrtf)
    range3 = range(0, nb_of_obtf)  
    range4 = range(0, nb_of_i_reponse)  

    # Générer toutes les permutation
    combinaisons = list(product(range1, range2, range3, range4))

    # Afficher les résultats
    for combinaison in combinaisons:
        cursor.execute("INSERT OR IGNORE INTO Combination (excitation_file, hrtf, obtf, impulse_response) VALUES (?,?,?,?)", (get_file_name(combinaison[0], "Excitation_Files"), get_file_name(combinaison[1], "HRTF"), get_file_name(combinaison[2], "OBTF"),get_file_name(combinaison[3], "Impulse_Response"),))

    
    connection.commit()

def generate_test():

    cursor.execute("SELECT * FROM Combination")
    rows = cursor.fetchall()

    nb_of_combi = len(rows) + 1

    first_part = np.arange(1,nb_of_combi)
    second_part = np.arange(1,nb_of_combi)
    third_part = np.arange(1,nb_of_combi)

    np.random.shuffle(first_part)
    np.random.shuffle(second_part)
    np.random.shuffle(third_part)

    test_order_temp = np.append(first_part, second_part)
    test_order = np.append(test_order_temp, third_part)

    X_boolean = np.random.choice(a=[0, 1], size=(len(test_order))) 

    for i in range(0,len(test_order),2):
        cursor.execute("INSERT OR IGNORE INTO Test_order (signal_A_id, signal_B_id, signal_X) VALUES (?,?,?)", (int(test_order[i]), int(test_order[i+1]), int(X_boolean[i])))

    connection.commit()

    return first_part

def load_signal(order):

    cursor.execute("SELECT * FROM Combination")
    rows = cursor.fetchall()

    for id in order:
        
        file_exi = rows[id - 1][1]
        cursor.execute("SELECT id FROM Excitation_Files WHERE file_name = ?",(file_exi,))
        exi_id = cursor.fetchone()[0] - 1

        file_hrtf = rows[id - 1][2]
        cursor.execute("SELECT id FROM HRTF WHERE file_name = ?",(file_hrtf,))
        hrtf_id = cursor.fetchone()[0] - 1

        file_obtf = rows[id - 1][3]
        cursor.execute("SELECT id FROM OBTF WHERE file_name = ?",(file_obtf,))
        obtf_id = cursor.fetchone()[0] - 1

        file_ir = rows[id - 1][4]
        cursor.execute("SELECT id FROM Impulse_Response WHERE file_name = ?",(file_ir,))
        ir_id = cursor.fetchone()[0] - 1

        signal_name = sm.generate_signal(exi_id,hrtf_id,obtf_id,ir_id,id)
        cursor.execute("UPDATE Combination SET signal_file_name = ? WHERE id = ?", (signal_name, int(id),))

        connection.commit()
    
def clear_db():

    cursor.execute("DROP TABLE `Combination`")
    cursor.execute("DROP TABLE `Test_order`")
    cursor.execute("DROP TABLE `Impulse_Response`")
    cursor.execute("DROP TABLE `Excitation_Files`")
    cursor.execute("DROP TABLE `HRTF`")
    cursor.execute("DROP TABLE `OBTF`")

    connection.commit()
    


