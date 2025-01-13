import tkinter as tk
import sounddevice as sd
import soundfile as sf
import sqlite3
from tkinter import ttk
import os
import IHM_Folder.config as config  # Importation du fichier de configuration
import time
import wave

class ListeningTestApp:
    def __init__(self, subject_id):
        # connextion_signal_db à la base de données
        self.connection_signal_db = sqlite3.connect("Db_Folder/signal.db")
        self.cursor_signal_db = self.connection_signal_db.cursor()

        self.connection_result_db = sqlite3.connect("Db_Folder/result.db", check_same_thread=False)
        self.cursor_result_db = self.connection_result_db.cursor()

        # Charger les données nécessaires
        self.cursor_signal_db.execute("SELECT * FROM Combination")
        self.rows = self.cursor_signal_db.fetchall()
        self.total_listenings = len(self.rows) * 3 / 2

        # Initialiser les variables
        self.listening_number = 1
        self.a_clicked = 0
        self.b_clicked = 0
        self.x_clicked = 0
        self.start = time.perf_counter()
        self.subject = subject_id
        self.max_duration_signal = None
        self.button_A = None
        self.button_B = None
        self.button_X = None

        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Listening Test")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.BACKGROUND_COLOR)

        # Construire l'interface
        self.setup_ui()

        # Lancer la boucle principale
        self.root.mainloop()

    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Titre principal
        self.title_label = tk.Label(
            self.root,
            text="Listening n°1",
            font=config.TITLE_FONT,
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR,
        )
        self.title_label.pack(pady=20)

        # Barre de progression
        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=config.PROGRESS_BAR_LENGTH, mode="determinate"
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.place(x=650, y=30)

        self.progress_label = tk.Label(
            self.root,
            text="0% completed",
            font=config.PROGRESS_LABEL_FONT,
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR,
        )
        self.progress_label.pack(pady=10)
        self.progress_label.place(x=645, y=60)

        # Boutons A, B, X
        self.button_frame = tk.Frame(self.root, bg=config.BACKGROUND_COLOR)
        self.button_frame.pack(pady=20)

        self.button_A = tk.Button(
            self.button_frame,
            text="A",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=10,
            height=2,
            command=lambda: self.play_signal("A"),
        )
        self.button_A.grid(row=0, column=0, padx=20)

        self.button_B = tk.Button(
            self.button_frame,
            text="B",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=10,
            height=2,
            command=lambda: self.play_signal("B"),
        )
        self.button_B.grid(row=0, column=1, padx=20)

        self.button_X = tk.Button(
            self.button_frame,
            text="X",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=10,
            height=2,
            command=lambda: self.play_signal("X"),
        )
        self.button_X.grid(row=0, column=2, padx=20)

        # Question
        question_label = tk.Label(
            self.root,
            text="Which stimulus is X ?",
            font=config.LABEL_FONT,
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR,
        )
        question_label.pack(pady=20)

        # Boutons de réponse
        answer_frame = tk.Frame(self.root, bg=config.BACKGROUND_COLOR)
        answer_frame.pack(pady=10)

        tk.Button(
            answer_frame,
            text="X is A",
            font=("Arial", 14),
            bg="#d1d1d1",
            width=15,
            command=lambda: self.on_answer("A"),
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            answer_frame,
            text="X is B",
            font=("Arial", 14),
            bg="#d1d1d1",
            width=15,
            command=lambda: self.on_answer("B"),
        ).grid(row=0, column=1, padx=10)

        # Pied de page
        footer_label = tk.Label(
            self.root,
            text="LABORATORY OF ACOUSTICS    KU LEUVEN",
            font=config.FOOTER_FONT,
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR,
        )
        footer_label.pack(side="bottom", pady=10)

    

    def increment_listening_number(self):
        """Incrémenter le numéro d'écoute et mettre à jour l'interface"""
        self.listening_number += 1
        self.title_label.config(text=f"Listening n°{self.listening_number}")

        progress_value = (self.listening_number - 1) / self.total_listenings * 100
        self.progress_bar["value"] = progress_value
        self.progress_label.config(text=f"{progress_value:.0f}% completed")

    def play_signal(self, selected):

        def disable_button_for_duration(button, duration):
            """Désactive le bouton pendant une durée en secondes."""
            button.config(state="disabled")  # Désactiver le bouton
            button.after(duration * 1000, lambda: button.config(state="normal"))  # Réactiver après `duration`

        self.cursor_signal_db.execute("SELECT * FROM Test_order WHERE rowid = ?", (self.listening_number,))
        row = self.cursor_signal_db.fetchone()

        if selected == "X":
            self.x_clicked +=1
            A_B_index = row[row[3] + 1]
        elif selected == "A":
            self.a_clicked += 1
            A_B_index = row[row[4] + 1]
        elif selected == "B":
            self.b_clicked += 1
            A_B_index = row[2 - row[4]]

        self.cursor_signal_db.execute("SELECT * FROM Combination WHERE rowid = ?", (A_B_index,))
        row = self.cursor_signal_db.fetchone()

        A_B_file_name = row[5]
        file_path = "Signal_Response/" + str(A_B_file_name)

        if not os.path.exists(file_path):
            print(f"Erreur : Le fichier {file_path} n'existe pas.")
            return

        try:
            disable_button_for_duration(self.button_A, 10)
            signal, sampling_rate = sf.read(file_path)
            sd.play(signal, samplerate=sampling_rate)
            sd.wait()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    

    def on_answer(self, selected):

        def get_wav_duration(file_path):
            with wave.open(file_path, "r") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
            return duration
        
        end = time.perf_counter()

        self.cursor_signal_db.execute("SELECT * FROM Test_order WHERE id = ?", (self.listening_number,))
        row = self.cursor_signal_db.fetchone()

        answer = row[4]
        x_is = row[3]

        elapsed = end - self.start

        if answer == x_is:
            ans = 1 if selected == "A" else 0
        else:
            ans = 1 if selected == "B" else 0

        self.cursor_result_db.execute("SELECT id FROM Test_order WHERE signal_1_id = ? AND signal_2_id = ? AND signal_X = ? AND signal_A_B = ?",
            (row[1], row[2], row[3], row[4]))
        
        row = self.cursor_result_db.fetchone()
        
        print(f"Id : {row[0]}")

        self.cursor_result_db.execute("INSERT OR IGNORE INTO Result (sujet, test, a_click, b_click, x_click, time, answer) VALUES (?,?,?,?,?,?,?)",
                                      (self.subject,  row[0], self.a_clicked, self.b_clicked, self.x_clicked, elapsed, ans))

        
        self.connection_result_db.commit()
        self.increment_listening_number()

        self.cursor_signal_db.execute("SELECT * FROM Test_order WHERE rowid = ?", (self.listening_number,))
        row = self.cursor_signal_db.fetchone()

        self.max_duration_signal = 0
        for i in range(2):

            self.cursor_signal_db.execute("SELECT * FROM Combination WHERE rowid = ?", (i + 1,))
            row = self.cursor_signal_db.fetchone()

            A_B_file_name = row[5]
            file_path = "Signal_Response/" + str(A_B_file_name)

            file_path = "Signal_Response/y_out_1.wav"
            duration_temp = get_wav_duration(file_path)

            print(duration_temp)

            if duration_temp > self.max_duration_signal:
                self.max_duration_signal = duration_temp

        print(self.max_duration_signal)

        self.start = time.perf_counter()

        self.a_clicked = 0
        self.b_clicked = 0
        self.x_clicked = 0


# Lancer l'application
if __name__ == "__main__":
    ListeningTestApp(1)
