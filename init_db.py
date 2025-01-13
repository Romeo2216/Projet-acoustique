import sqlite3
import os
from itertools import product
import numpy as np
import signal_manager as sm


connection_signal_db = sqlite3.connect("Db_Folder/signal.db", check_same_thread=False)

cursor_signal_db = connection_signal_db.cursor()

connection_result_db = sqlite3.connect("Db_Folder/result.db", check_same_thread=False)

cursor_result_db = connection_result_db.cursor()

def _init_db(): 

    cursor_signal_db.execute("CREATE TABLE IF NOT EXISTS Impulse_Response (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_signal_db.execute("CREATE TABLE IF NOT EXISTS Excitation_Files (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_signal_db.execute("CREATE TABLE IF NOT EXISTS HRTF (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_signal_db.execute("CREATE TABLE IF NOT EXISTS OBTF (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_signal_db.execute("CREATE TABLE IF NOT EXISTS Combination (id INTEGER PRIMARY KEY  AUTOINCREMENT, `excitation_file` TEXT REFERENCES `Excitation_Files`(`file_name`), `hrtf` TEXT REFERENCES `HRTF`(`file_name`), `obtf` TEXT REFERENCES `OBTF`(`file_name`), `impulse_response` TEXT REFERENCES `Impulse_Response`(`file_name`),`signal_file_name` TEXT, UNIQUE(id))")
    cursor_signal_db.execute("CREATE TABLE IF NOT EXISTS Test_order (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `signal_1_id` INTEGER REFERENCES `Combination`(`id`), `signal_2_id` INTEGER REFERENCES `Combination`(`id`), `signal_X` INTEGER, `signal_A_B` INTEGER, UNIQUE(id))")
    
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS Sujet (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `nom` TEXT, `prenom` TEXT, `date_de_naissance` TEXT, `sexe` TEXT, `probleme_d_audition` INTEGER, UNIQUE(id))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS Impulse_Response (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS Excitation_Files (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS HRTF (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS OBTF (`id` INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, UNIQUE(file_name))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS Combination (id INTEGER PRIMARY KEY  AUTOINCREMENT, `excitation_file` TEXT REFERENCES `Excitation_Files`(`file_name`), `hrtf` TEXT REFERENCES `HRTF`(`file_name`), `obtf` TEXT REFERENCES `OBTF`(`file_name`), `impulse_response` TEXT REFERENCES `Impulse_Response`(`file_name`), UNIQUE(id))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS Test_order (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `signal_1_id` INTEGER REFERENCES `Combination`(`id`), `signal_2_id` INTEGER REFERENCES `Combination`(`id`), `signal_X` INTEGER, `signal_A_B` INTEGER, UNIQUE(id))")
    cursor_result_db.execute("CREATE TABLE IF NOT EXISTS Result (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `sujet` INTEGER REFERENCES `Sujet`(`id`), `test` INTEGER REFERENCES `Test_order`(`id`), `a_click` INTEGER, `b_click` INTEGER, `x_click` INTEGER, `time` REAL, `answer` INTEGER)")
    
    folder_path = "Impulse_Response"

    files = os.listdir(folder_path)

    for file in files:
        cursor_signal_db.execute("INSERT OR IGNORE INTO Impulse_Response (file_name) VALUES (?)", (file,))
        cursor_result_db.execute("INSERT OR IGNORE INTO Impulse_Response (file_name) VALUES (?)", (file,))

    folder_path = "Excitation_Files"

    files = os.listdir(folder_path)

    for file in files:
        cursor_signal_db.execute("INSERT OR IGNORE INTO Excitation_Files (file_name) VALUES (?)", (file,))
        cursor_result_db.execute("INSERT OR IGNORE INTO Excitation_Files (file_name) VALUES (?)", (file,))

    folder_path = "HRTF"

    files = os.listdir(folder_path)

    for file in files:
        cursor_signal_db.execute("INSERT OR IGNORE INTO HRTF (file_name) VALUES (?)", (file,))
        cursor_result_db.execute("INSERT OR IGNORE INTO HRTF (file_name) VALUES (?)", (file,))

    folder_path = "OBTF"

    files = os.listdir(folder_path)

    for file in files:
        cursor_signal_db.execute("INSERT OR IGNORE INTO OBTF (file_name) VALUES (?)", (file,))
        cursor_result_db.execute("INSERT OR IGNORE INTO OBTF (file_name) VALUES (?)", (file,))

    connection_signal_db.commit()
    connection_result_db.commit()

def get_file_name(i, table):

    cursor_signal_db.execute("SELECT * FROM " + table)
    rows = cursor_signal_db.fetchall()
    row = rows[i]
    file_name = row[1]

    return "".join(file_name)

def save_conbination():

    cursor_signal_db.execute("SELECT * FROM Excitation_Files")
    rows = cursor_signal_db.fetchall()

    nb_of_exi = len(rows)

    cursor_signal_db.execute("SELECT * FROM HRTF")
    rows = cursor_signal_db.fetchall()

    nb_of_hrtf = len(rows)

    cursor_signal_db.execute("SELECT * FROM OBTF")
    rows = cursor_signal_db.fetchall()

    nb_of_obtf = len(rows)

    cursor_signal_db.execute("SELECT * FROM Impulse_Response")
    rows = cursor_signal_db.fetchall()

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
        cursor_signal_db.execute("INSERT OR IGNORE INTO Combination (excitation_file, hrtf, obtf, impulse_response) VALUES (?,?,?,?)", (get_file_name(combinaison[0], "Excitation_Files"), get_file_name(combinaison[1], "HRTF"), get_file_name(combinaison[2], "OBTF"),get_file_name(combinaison[3], "Impulse_Response"),))
        
        cursor_result_db.execute(
            "SELECT COUNT(*) FROM Combination WHERE excitation_file = ? AND hrtf = ? AND obtf = ? AND impulse_response = ?",
            (get_file_name(combinaison[0], "Excitation_Files"), get_file_name(combinaison[1], "HRTF"), get_file_name(combinaison[2], "OBTF"),get_file_name(combinaison[3], "Impulse_Response")),
        )
        result = cursor_result_db.fetchone()

        if result[0] > 0:
            print("User already exists in the database. Skipping insertion.")
        else:
            # Insérer dans la base de données si le profil n'existe pas
            cursor_result_db.execute("INSERT OR IGNORE INTO Combination (excitation_file, hrtf, obtf, impulse_response) VALUES (?,?,?,?)", (get_file_name(combinaison[0], "Excitation_Files"), get_file_name(combinaison[1], "HRTF"), get_file_name(combinaison[2], "OBTF"),get_file_name(combinaison[3], "Impulse_Response"),))

            connection_result_db.commit()
            print("User has been successfully added to the database.")
        
        
    
    connection_signal_db.commit()
    connection_signal_db.commit()

def generate_test():

    cursor_signal_db.execute("SELECT * FROM Combination")
    rows = cursor_signal_db.fetchall()

    nb_of_combi = len(rows) + 1

    combi = np.arange(1,nb_of_combi)
    
    combinaisons = [(a, b) for a, b in product(combi, combi) if a <= b and a != b]

    np.random.shuffle(combinaisons)

    generation_order = [element for tuple_ in combinaisons for element in tuple_]

    X_boolean = np.random.choice(a=[0, 1], size=(len(combinaisons))) 
    A_B_boolean = np.random.choice(a=[0, 1], size=(len(combinaisons))) 

    for i in range(0,len(combinaisons)):
        cursor_signal_db.execute("INSERT OR IGNORE INTO Test_order (signal_1_id, signal_2_id, signal_X, signal_A_B) VALUES (?,?,?,?)", (int(combinaisons[i][0]), int(combinaisons[i][1]), int(X_boolean[i]), int(A_B_boolean[i])))
        
        old_id_1 = int(combinaisons[i][0])

        cursor_signal_db.execute("SELECT * FROM Combination WHERE id = ?",(old_id_1,))
        cb = cursor_signal_db.fetchone()

        cursor_result_db.execute("SELECT id FROM Combination WHERE excitation_file = ? AND hrtf = ? AND obtf = ? AND impulse_response = ?",
                                (cb[1], cb[2], cb[3], cb[4]))
        
        new_id_1 = cursor_result_db.fetchone()[0]

        old_id_2 = int(combinaisons[i][1])

        cursor_signal_db.execute("SELECT * FROM Combination WHERE id = ?",(old_id_2,))
        cb = cursor_signal_db.fetchone()

        cursor_result_db.execute("SELECT id FROM Combination WHERE excitation_file = ? AND hrtf = ? AND obtf = ? AND impulse_response = ?",
                                (cb[1], cb[2], cb[3], cb[4]))

        new_id_2 = cursor_result_db.fetchone()[0]

        cursor_result_db.execute(
            "SELECT COUNT(*) FROM Test_order WHERE signal_1_id = ? AND signal_2_id = ? AND signal_X = ? AND signal_A_B = ?",
            (new_id_1, new_id_2, int(X_boolean[i]), int(A_B_boolean[i]))),
        
        result = cursor_result_db.fetchone()

        if result[0] > 0:
            print("User already exists in the database. Skipping insertion.")
        else:
            # Insérer dans la base de données si le profil n'existe pas
            cursor_result_db.execute("INSERT OR IGNORE INTO Test_order (signal_1_id, signal_2_id, signal_X, signal_A_B) VALUES (?,?,?,?)", 
                                     (new_id_1, new_id_2, int(X_boolean[i]), int(A_B_boolean[i])))
    
            print("User has been successfully added to the database.")
        
        
    connection_signal_db.commit()
    connection_result_db.commit()

    return generation_order

def load_signal(order):

    cursor_signal_db.execute("SELECT * FROM Combination")
    rows = cursor_signal_db.fetchall()

    used_ids = set()

    for id in order:

        if id in used_ids:
            continue

        used_ids.add(id)
        
        file_exi = rows[id - 1][1]
        cursor_signal_db.execute("SELECT id FROM Excitation_Files WHERE file_name = ?",(file_exi,))
        exi_id = cursor_signal_db.fetchone()[0] - 1

        file_hrtf = rows[id - 1][2]
        cursor_signal_db.execute("SELECT id FROM HRTF WHERE file_name = ?",(file_hrtf,))
        hrtf_id = cursor_signal_db.fetchone()[0] - 1

        file_obtf = rows[id - 1][3]
        cursor_signal_db.execute("SELECT id FROM OBTF WHERE file_name = ?",(file_obtf,))
        obtf_id = cursor_signal_db.fetchone()[0] - 1

        file_ir = rows[id - 1][4]
        cursor_signal_db.execute("SELECT id FROM Impulse_Response WHERE file_name = ?",(file_ir,))
        ir_id = cursor_signal_db.fetchone()[0] - 1

        signal_name = sm.generate_signal(exi_id,hrtf_id,obtf_id,ir_id,id)
        cursor_signal_db.execute("UPDATE Combination SET signal_file_name = ? WHERE id = ?", (signal_name, int(id),))

        connection_signal_db.commit()
    
def clear_db():

    cursor_signal_db.execute("DROP TABLE `Combination`")
    cursor_signal_db.execute("DROP TABLE `Test_order`")
    cursor_signal_db.execute("DROP TABLE `Impulse_Response`")
    cursor_signal_db.execute("DROP TABLE `Excitation_Files`")
    cursor_signal_db.execute("DROP TABLE `HRTF`")
    cursor_signal_db.execute("DROP TABLE `OBTF`")

    connection_signal_db.commit()
    


