import tkinter as tk
from tkinter import ttk
import config  # Importer les paramètres graphiques

class InstructionsApp:
    def __init__(self):
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Instructions")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.BACKGROUND_COLOR)

        # Construire l'interface utilisateur
        self.setup_ui()

        # Lancer la boucle principale
        self.root.mainloop()

    def setup_ui(self):
        """Créer et configurer l'interface utilisateur"""
        # Label pour le titre des instructions
        tk.Label(
            self.root,
            text="Instructions:",
            font=("Arial", 16, "bold"),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR
        ).pack(pady=10, anchor="w", padx=20)

        # Charger le texte depuis un fichier
        instructions_text = self.load_instructions("instructions.txt")

        # Ajouter une zone de texte pour afficher les instructions
        instructions_label = tk.Label(
            self.root,
            text=instructions_text,
            font=("Arial", 12),
            bg=config.BACKGROUND_COLOR,
            fg=config.TEXT_COLOR,
            justify="left",
            wraplength=700  # Limiter la largeur du texte pour un affichage clair
        )
        instructions_label.pack(pady=20, padx=20, anchor="w")

        # Ajouter un bouton "Ready"
        ready_button = tk.Button(
            self.root,
            text="Ready",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_BG_COLOR,
            command=self.on_ready
        )
        ready_button.pack(pady=20, anchor="center")

    def load_instructions(self, filepath):
        """Charger les instructions depuis un fichier texte"""
        try:
            with open(filepath, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "Error: instructions file not found."

    def on_ready(self):
        """Action pour le bouton Ready"""
        print("Ready clicked!")
        self.root.destroy()  # Fermer la fenêtre

# Lancer l'application
if __name__ == "__main__":
    InstructionsApp()
