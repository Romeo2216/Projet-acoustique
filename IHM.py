import tkinter as tk
import sounddevice as sd
import soundfile as sf
import sqlite3
from tkinter import ttk
import os
import config  # Importation du fichier de configuration


class ListeningTestApp:
    def __init__(self):
        # Connexion à la base de données
        self.connexion = sqlite3.connect("signal.db")
        self.cursor = self.connexion.cursor()

        # Charger les données nécessaires
        self.cursor.execute("SELECT * FROM Combination")
        self.rows = self.cursor.fetchall()
        self.total_listenings = len(self.rows) * 3 / 2

        # Initialiser les variables
        self.listening_number = 1

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

        tk.Button(
            self.button_frame,
            text="A",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=10,
            height=2,
            command=lambda: self.play_signal("A"),
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            self.button_frame,
            text="B",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=10,
            height=2,
            command=lambda: self.play_signal("B"),
        ).grid(row=0, column=1, padx=20)

        tk.Button(
            self.button_frame,
            text="X",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_COLOR,
            fg=config.TEXT_COLOR,
            width=10,
            height=2,
            command=lambda: self.play_signal("X"),
        ).grid(row=0, column=2, padx=20)

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
        """Lire le signal sélectionné"""
        self.cursor.execute("SELECT * FROM Test_order WHERE rowid = ?", (self.listening_number,))
        row = self.cursor.fetchone()

        if selected == "X":
            A_B_index = row[row[3] + 1]
        elif selected == "A":
            A_B_index = row[row[4] + 1]
        elif selected == "B":
            A_B_index = row[2 - row[4]]

        self.cursor.execute("SELECT * FROM Combination WHERE rowid = ?", (A_B_index,))
        row = self.cursor.fetchone()

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

    def on_answer(self, selected):
        """Gérer la réponse de l'utilisateur"""
        self.increment_listening_number()


# Lancer l'application
if __name__ == "__main__":
    ListeningTestApp()
