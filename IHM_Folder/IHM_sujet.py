import tkinter as tk
from tkinter import ttk
import IHM_Folder.config as config  # Importer les paramètres graphiques
import sqlite3




class UserFormApp:
    def __init__(self):
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("User Form")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.BACKGROUND_COLOR)

        #
        self.connection_result_db = sqlite3.connect("Db_Folder/result.db", check_same_thread=False)

        self.cursor_result_db = self.connection_result_db.cursor()

        # Variables
        self.sexe_var = tk.StringVar(value="F")  # Sexe par défaut
        self.hearing_var = tk.StringVar(value="N")  # Trouble auditif par défaut
        self.lastname_entry = None
        self.firstname_entry = None
        self.day_combo = None
        self.month_combo = None
        self.year_combo = None
        self.sujet = None

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
        user_window.geometry("500x300")
        user_window.configure(bg=config.BACKGROUND_COLOR)

        # Titre
        tk.Label(
            user_window, text="Select a User Profile", font=("Arial", 14, "bold"), bg=config.BACKGROUND_COLOR, fg=config.TEXT_COLOR
        ).pack(pady=10)

        # Configurer le style pour centrer le texte et modifier les couleurs
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="lightgrey",  # Couleur de fond des lignes
            fieldbackground="lightgrey",  # Couleur de fond globale
            rowheight=25,  # Hauteur des lignes
        )
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), anchor="center")  # Style des en-têtes

        # Cadre pour le tableau
        table_frame = tk.Frame(user_window, bg=config.BACKGROUND_COLOR)
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Ajouter un Treeview (tableau) avec deux colonnes
        user_table = ttk.Treeview(table_frame, columns=("first_name", "last_name"), show="headings", height=10)
        user_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurer les colonnes
        user_table.heading("first_name", text="First Name", anchor="center")
        user_table.heading("last_name", text="Last Name", anchor="center")
        user_table.column("first_name", width=200, anchor="center")
        user_table.column("last_name", width=200, anchor="center")

        # Barre de défilement pour le tableau
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=user_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        user_table.configure(yscrollcommand=scrollbar.set)

        # Charger les utilisateurs depuis la base de données
        try:
            self.cursor_result_db.execute("SELECT prenom, nom, sexe, date_de_naissance FROM Sujet")
            users = self.cursor_result_db.fetchall()
        except sqlite3.Error as e:
            tk.Label(user_window, text=f"Database error: {e}", font=("Arial", 12), bg="red", fg="white").pack(pady=10)
            return

        if not users:
            tk.Label(user_window, text="No users found in the database.", font=("Arial", 12), bg="yellow", fg="black").pack(pady=10)
            return

        # Ajouter les utilisateurs au tableau
        for user in users:
            user_table.insert("", "end", values=(user[0], user[1]))

        def select_user():
            """Remplir le formulaire principal avec les données utilisateur sélectionnées"""
            selected_item = user_table.selection()
            if not selected_item:
                print("No user selected.")
                return

            # Récupérer les données de la ligne sélectionnée
            selected_user = user_table.item(selected_item, "values")
            first_name, last_name = selected_user

            # Trouver les données complètes dans la base
            for user in users:
                if user[0] == first_name and user[1] == last_name:
                    # Préremplir les champs du formulaire
                    self.lastname_entry.delete(0, tk.END)
                    self.lastname_entry.insert(0, user[1])  # Last name

                    self.firstname_entry.delete(0, tk.END)
                    self.firstname_entry.insert(0, user[0])  # First name

                    # Gérer la date de naissance
                    try:
                        day, month, year = user[3].split("/")
                        self.day_combo.set(day)
                        self.month_combo.set(month)
                        self.year_combo.set(year)
                    except ValueError:
                        print("Invalid date format in the database.")

                    # Remplir le sexe
                    self.sexe_var.set(user[2])
                    break

            user_window.destroy()

        # Bouton pour confirmer la sélection
        tk.Button(
            user_window,
            text="Select",
            font=("Arial", 12),
            bg=config.BUTTON_BG_COLOR,
            command=select_user,
        ).pack(pady=5)

        # Bouton pour annuler
        tk.Button(
            user_window,
            text="Cancel",
            font=("Arial", 12),
            bg="gray",
            command=user_window.destroy,
        ).pack(pady=5)




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
        self.cursor_result_db.execute(
            "SELECT COUNT(*) FROM Sujet WHERE nom = ? AND prenom = ? AND date_de_naissance = ?",
            (nom, prenom, date_naissance),
        )
        result = self.cursor_result_db.fetchone()

        if result[0] > 0:
            print("User already exists in the database. Skipping insertion.")
        else:
            # Insérer dans la base de données si le profil n'existe pas
            self.cursor_result_db.execute(
                "INSERT INTO Sujet (nom, prenom, date_de_naissance, sexe, probleme_d_audition) VALUES (?,?,?,?,?)",
                (nom, prenom, date_naissance, sexe, audition),
            )
            self.connection_result_db.commit()
            print("User has been successfully added to the database.")

        self.cursor_result_db.execute(
            "SELECT * FROM Sujet WHERE nom = ? AND prenom = ? AND date_de_naissance = ?",
            (nom, prenom, date_naissance),
        )
        result = self.cursor_result_db.fetchone()
        self.sujet = int(result[0])

        # Fermer l'application après validation
        self.root.destroy()

    def get_subject(self):
        return self.sujet



# Lancer l'application
if __name__ == "__main__":
    UserFormApp()
