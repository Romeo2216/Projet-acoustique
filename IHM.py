import tkinter as tk
import sounddevice as sd
import soundfile as sf
import sqlite3
from tkinter import ttk
import os
import config  # Importation du fichier de configuration

listening_number = 1

def run_test(): 
    connexion = sqlite3.connect("signal.db")
    cursor = connexion.cursor()

    cursor.execute("SELECT * FROM Combination")
    rows = cursor.fetchall()
    total_listenings = len(rows) * 3 / 2

    def increment_listening_number():
        global listening_number
        listening_number += 1
        title_label.config(text="Listening n°" + str(listening_number))

        progress_value = (listening_number - 1) / total_listenings * 100
        progress_bar["value"] = progress_value
        progress_label.config(text=f"{progress_value:.0f}% completed")

    def play_signal(selected):
        global listening_number
        cursor.execute("SELECT * FROM Test_order WHERE rowid = ?", (listening_number,))
        row = cursor.fetchone()

        if selected == "X":
            A_B_index = row[row[3] + 1]
        elif selected == "A":
            A_B_index = row[row[4] + 1]
        elif selected == "B":
            A_B_index = row[2 - row[4]]

        cursor.execute("SELECT * FROM Combination WHERE rowid = ?", (A_B_index,))
        row = cursor.fetchone()

        A_B_file_name = row[5]

        file_path = "Signal_Response/" + str(A_B_file_name)

        if not os.path.exists(file_path):
            print(f"Erreur : Le fichier {file_path} n'existe pas.")
            return

        try:
            signal, sampling_rate = sf.read(file_path)
            sd.play(signal, samplerate=sampling_rate)
            sd.wait()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    def on_answer(selected):
        increment_listening_number()

    root = tk.Tk()
    root.title("Listening Test")
    root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    root.configure(bg=config.BACKGROUND_COLOR)

    title_label = tk.Label(root, text="Listening n°1", font=config.TITLE_FONT, bg=config.BACKGROUND_COLOR, fg=config.TEXT_COLOR)
    title_label.pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=config.PROGRESS_BAR_LENGTH, mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar.place(x=650, y=30)

    progress_label = tk.Label(root, text="0% completed", font=config.PROGRESS_LABEL_FONT, bg=config.BACKGROUND_COLOR, fg=config.TEXT_COLOR)
    progress_label.pack(pady=10)
    progress_label.place(x=645, y=60)

    button_frame = tk.Frame(root, bg=config.BACKGROUND_COLOR)
    button_frame.pack(pady=20)

    btn_A = tk.Button(button_frame, text="A", font=config.BUTTON_FONT, bg=config.BUTTON_COLOR, fg=config.TEXT_COLOR, width=10, height=2, command=lambda: play_signal("A"))
    btn_A.grid(row=0, column=0, padx=20)

    btn_B = tk.Button(button_frame, text="B", font=config.BUTTON_FONT, bg=config.BUTTON_COLOR, fg=config.TEXT_COLOR, width=10, height=2, command=lambda: play_signal("B"))
    btn_B.grid(row=0, column=1, padx=20)

    btn_X = tk.Button(button_frame, text="X", font=config.BUTTON_FONT, bg=config.BUTTON_COLOR, fg=config.TEXT_COLOR, width=10, height=2, command=lambda: play_signal("X"))
    btn_X.grid(row=0, column=2, padx=20)

    question_label = tk.Label(root, text="Which stimulus is X ?", font=config.LABEL_FONT, bg=config.BACKGROUND_COLOR, fg=config.TEXT_COLOR)
    question_label.pack(pady=20)

    answer_frame = tk.Frame(root, bg=config.BACKGROUND_COLOR)
    answer_frame.pack(pady=10)

    btn_answer_A = tk.Button(answer_frame, text="X is A", font=("Arial", 14), bg="#d1d1d1", width=15, command=lambda: on_answer("A"))
    btn_answer_A.grid(row=0, column=0, padx=10)

    btn_answer_B = tk.Button(answer_frame, text="X is B", font=("Arial", 14), bg="#d1d1d1", width=15, command=lambda: on_answer("B"))
    btn_answer_B.grid(row=0, column=1, padx=10)

    footer_label = tk.Label(root, text="LABORATORY OF ACOUSTICS    KU LEUVEN", font=config.FOOTER_FONT, bg=config.BACKGROUND_COLOR, fg=config.TEXT_COLOR)
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()
