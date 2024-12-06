import tkinter as tk
import sounddevice as sd
import soundfile as sf
import sqlite3
from tkinter import ttk

connexion = sqlite3.connect("signal.db")
cursor = connexion.cursor()

listening_number = 1

cursor.execute("SELECT * FROM Test_order")
rows = cursor.fetchall()
total_listenings = len(rows)

# Fonction appelée lorsque l'utilisateur clique sur une réponse

def increment_listening_number():
    global listening_number
    listening_number += 1
    title_label.config(text = "Listening n°" + str(listening_number))

    progress_value = (listening_number - 1) / total_listenings * 100
    progress_bar["value"] = progress_value
    # Mettre à jour le label de progression
    progress_label.config(text=f"{progress_value:.0f}% completed")

def play_signal(selected):
    global listening_number
    cursor.execute("SELECT * FROM Test_order WHERE rowid = ?",(listening_number,))
    row = cursor.fetchone()

    if selected == "X":
        A_B_index = row[row[3]+1]

    elif selected == "A":
        A_B_index = row[1]

    elif selected == "B":
        A_B_index = row[2]

    cursor.execute("SELECT * FROM Combination WHERE rowid = ?",(A_B_index,))
    row = cursor.fetchone()

    A_B_file_name = row[5]

    signal, sampling_rate = sf.read("Signal_Response/" + str(A_B_file_name))

    sd.play(signal, samplerate=sampling_rate)
    sd.wait()

def on_answer(selected):
    increment_listening_number()

# Initialiser la fenêtre principale
root = tk.Tk()
root.title("Listening Test")
root.geometry("800x400")  # Taille de la fenêtre
root.configure(bg="#008cb3")  # Couleur de fond

# Label pour le titre
title_label = tk.Label(
    root, text="Listening n°1", font=("Arial", 20, "bold"), bg="#008cb3", fg="white"
)
title_label.pack(pady=20)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

# Label pour afficher le pourcentage de progression
progress_label = tk.Label(root, text="0% completed", font=("Arial", 12), bg="#008cb3", fg="white")
progress_label.pack(pady=10)

# Cadre pour les boutons A, B, X
button_frame = tk.Frame(root, bg="#008cb3")
button_frame.pack(pady=20)

# Boutons A, B, X
btn_A = tk.Button(
    button_frame, text="A", 
    font=("Arial", 16), 
    bg="#004e73", 
    fg="white", 
    width=10, 
    height=2,
    command=lambda: play_signal("A"),
    )

btn_A.grid(row=0, column=0, padx=20)

btn_B = tk.Button(
    button_frame, 
    text="B", 
    font=("Arial", 16), 
    bg="#004e73", 
    fg="white", 
    width=10, 
    height=2,
    command=lambda: play_signal("B"),
    )

btn_B.grid(row=0, column=1, padx=20)

btn_X = tk.Button(
    button_frame, 
    text="X", 
    font=("Arial", 16), 
    bg="#004e73", 
    fg="white", 
    width=10, 
    height=2,
    command=lambda: play_signal("X"),
    )

btn_X.grid(row=0, column=2, padx=20)

# Label pour la question
question_label = tk.Label(
    root, text="Which stimulus is X ?", font=("Arial", 16), bg="#008cb3", fg="white"
)
question_label.pack(pady=20)

# Cadre pour les options de réponse
answer_frame = tk.Frame(root, bg="#008cb3")
answer_frame.pack(pady=10)

# Boutons pour répondre
btn_answer_A = tk.Button(
    answer_frame,
    text="X is A",
    font=("Arial", 14),
    bg="#d1d1d1",
    width=15,
    command=lambda: on_answer("A"),
)
btn_answer_A.grid(row=0, column=0, padx=10)

btn_answer_B = tk.Button(
    answer_frame,
    text="X is B",
    font=("Arial", 14),
    bg="#d1d1d1",
    width=15,
    command=lambda: on_answer("B"),
)
btn_answer_B.grid(row=0, column=1, padx=10)

# Pied de page avec le logo ou information
footer_label = tk.Label(
    root,
    text="LABORATORY OF ACOUSTICS    KU LEUVEN",
    font=("Arial", 10, "bold"),
    bg="#008cb3",
    fg="white",
)
footer_label.pack(side="bottom", pady=10)

# Lancer la boucle principale de l'application
root.mainloop()
