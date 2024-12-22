import tkinter as tk
from tkinter import ttk
import config  # Importer les paramètres graphiques
import sqlite3

connection = sqlite3.connect("signal.db", check_same_thread=False)
cursor = connection.cursor()


class UserFormApp:
    def __init__(self):
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("User Form")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.BACKGROUND_COLOR)

        # Variables
        self.sexe_var = tk.StringVar(value="F")  # Sexe par défaut
        self.hearing_var = tk.StringVar(value="N")  # Trouble auditif par défaut
        self.lastname_entry = None
        self.firstname_entry = None
        self.day_combo = None
        self.month_combo = None
        self.year_combo = None

        # Construire l'interface utilisateur
        self.setup_ui()

        # Lancer la boucle principale
        self.root.mainloop()

    def setup_ui(self):
        """Crée et configure l'interface utilisateur"""
        # Titre principal
        tk.Label(
            self.root, text="User Form", font=("Arial", 16, "bold"), bg=config.BACKGROUND_COLOR
        ).pack(pady=10)

        # Champs pour le nom de famille et prénom
        tk.Label(self.root, text="LastName:", font=config.LABEL_FONT, bg=config.BACKGROUND_COLOR).place(x=50, y=60)
        self.lastname_entry = tk.Entry(self.root, font=config.ENTRY_FONT, width=20)
        self.lastname_entry.place(x=150, y=60)

        tk.Label(self.root, text="FirstName:", font=config.LABEL_FONT, bg=config.BACKGROUND_COLOR).place(x=400, y=60)
        self.firstname_entry = tk.Entry(self.root, font=config.ENTRY_FONT, width=20)
        self.firstname_entry.place(x=500, y=60)

        # Bouton "User known"
        user_known_button = tk.Button(
            self.root,
            text="User known",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_BG_COLOR,
            command=self.user_known_action,
        )
        user_known_button.place(x=650, y=10)

        # Section Sexe
        tk.Label(self.root, text="Sexe:", font=config.LABEL_FONT, bg=config.BACKGROUND_COLOR).place(x=50, y=100)
        tk.Radiobutton(self.root, text="F", variable=self.sexe_var, value="F", font=config.RADIO_BUTTON_FONT, bg=config.BACKGROUND_COLOR).place(x=150, y=100)
        tk.Radiobutton(self.root, text="M", variable=self.sexe_var, value="M", font=config.RADIO_BUTTON_FONT, bg=config.BACKGROUND_COLOR).place(x=200, y=100)

        # Section Date de naissance avec Combobox
        tk.Label(self.root, text="Date of Birth:", font=config.LABEL_FONT, bg=config.BACKGROUND_COLOR).place(x=50, y=150)
        
        # Combobox pour le jour
        self.day_combo = ttk.Combobox(self.root, values=[str(i) for i in range(1, 32)], font=config.ENTRY_FONT, width=5)
        self.day_combo.place(x=200, y=150)
        self.day_combo.set("Day")  # Placeholder

        # Combobox pour le mois
        self.month_combo = ttk.Combobox(
            self.root,
            values=[
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
            font=config.ENTRY_FONT,
            width=10
        )
        self.month_combo.place(x=300, y=150)
        self.month_combo.set("Month")  # Placeholder

        # Combobox pour l'année
        self.year_combo = ttk.Combobox(self.root, values=[str(i) for i in range(2024, 1900, -1)], font=config.ENTRY_FONT, width=8)
        self.year_combo.place(x=450, y=150)
        self.year_combo.set("Year")  # Placeholder

        # Section pour les troubles auditifs
        tk.Label(self.root, text="Do you have some hearing impairment?", font=config.LABEL_FONT, bg=config.BACKGROUND_COLOR).place(x=50, y=200)
        tk.Radiobutton(self.root, text="Y", variable=self.hearing_var, value="Y", font=config.RADIO_BUTTON_FONT, bg=config.BACKGROUND_COLOR).place(x=450, y=200)
        tk.Radiobutton(self.root, text="N", variable=self.hearing_var, value="N", font=config.RADIO_BUTTON_FONT, bg=config.BACKGROUND_COLOR).place(x=500, y=200)

        # Bouton "Validate"
        validate_button = tk.Button(
            self.root,
            text="Validate",
            font=config.BUTTON_FONT,
            bg=config.BUTTON_BG_COLOR,
            command=self.validate_action,
        )
        validate_button.place(x=350, y=300)

    def user_known_action(self):
        """Ouvrir une fenêtre pour sélectionner un utilisateur existant"""
        # Créer une nouvelle fenêtre
        user_window = tk.Toplevel(self.root)
        user_window.title("Select User")
        user_window.geometry("400x300")
        user_window.configure(bg=config.BACKGROUND_COLOR)

        # Titre
        tk.Label(
            user_window, text="Select a User Profile", font=("Arial", 14, "bold"), bg=config.BACKGROUND_COLOR, fg=config.TEXT_COLOR
        ).pack(pady=10)

        # Liste des utilisateurs
        users_listbox = tk.Listbox(user_window, font=("Arial", 12), width=40, height=10)
        users_listbox.pack(pady=10)

        # Charger les utilisateurs depuis la base de données
        cursor.execute("SELECT prenom, nom, sexe, date_de_naissance FROM Sujet")
        users = cursor.fetchall()

        # Ajouter les utilisateurs à la Listbox
        for user in users:
            users_listbox.insert(tk.END, f"{user[0]}, {user[1]}")

        def select_user():
            """Remplir le formulaire principal avec les données utilisateur sélectionnées"""
            selected_index = users_listbox.curselection()
            if not selected_index:
                print("No user selected.")
                return
            selected_user = users[selected_index[0]]

            # Préremplir les champs du formulaire
            self.lastname_entry.delete(0, tk.END)
            self.lastname_entry.insert(0, selected_user[1])  # Last name

            self.firstname_entry.delete(0, tk.END)
            self.firstname_entry.insert(0, selected_user[0])  # First name

            # Remplir la date de naissance
            day, month, year = selected_user[3].split("/")
            self.day_combo.set(day)
            self.month_combo.set(month)
            self.year_combo.set(year)

            # Remplir le sexe
            self.sexe_var.set(selected_user[2])

            user_window.destroy()

        # Bouton pour confirmer la sélection
        tk.Button(
            user_window,
            text="Select",
            font=("Arial", 12),
            bg=config.BUTTON_BG_COLOR,
            command=select_user,
        ).pack(pady=10)

    def validate_action(self):
        """Action pour le bouton 'Validate'"""
        jour = self.day_combo.get()
        mois = self.month_combo.get()
        annee = self.year_combo.get()
        nom = self.lastname_entry.get()
        prenom = self.firstname_entry.get()
        sexe = self.sexe_var.get()
        audition = 1 if self.hearing_var.get() == "Y" else 0

        # Vérification que tous les champs sont remplis
        if not jour.isdigit() or not annee.isdigit() or mois == "Month" or nom == "" or prenom == "":
            print("Invalid form")
            return

        # Construire la date de naissance
        date_naissance = f"{jour}/{mois}/{annee}"

        # Vérifier si le profil existe déjà
        cursor.execute(
            "SELECT COUNT(*) FROM Sujet WHERE nom = ? AND prenom = ? AND date_de_naissance = ?",
            (nom, prenom, date_naissance),
        )
        result = cursor.fetchone()

        if result[0] > 0:
            print("User already exists in the database. Skipping insertion.")
        else:
            # Insérer dans la base de données si le profil n'existe pas
            cursor.execute(
                "INSERT INTO Sujet (nom, prenom, date_de_naissance, sexe, probleme_d_audition) VALUES (?,?,?,?,?)",
                (nom, prenom, date_naissance, sexe, audition),
            )
            connection.commit()
            print("User has been successfully added to the database.")

        # Fermer l'application après validation
        self.root.destroy()



# Lancer l'application
if __name__ == "__main__":
    UserFormApp()
