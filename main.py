import init_db as db
import shutil
import os
import threading
import IHM_Folder.IHM as IHM
import IHM_Folder.IHM_sujet as IHM_sujet
import IHM_Folder.IHM_instruction as IHM_instruction

dossier = "Signal_Response"

if os.path.exists(dossier):
    shutil.rmtree(dossier)

os.mkdir(dossier)

db.clear_db()

db._init_db()

db.save_conbination()

def processe_one():  

    order = db.generate_test()

    db.load_signal(order)

def process_two():

    userform = IHM_sujet.UserFormApp()
    print(userform.get_subject())

    IHM_instruction.InstructionsApp()

    IHM.ListeningTestApp(subject_id=userform.get_subject())

th1 = threading.Thread(target=processe_one)
th2 = threading.Thread(target=process_two)

th1.start()
th2.start()

th1.join()
th2.join()
