# Importation de la classe DataManager depuis le module DataManager
from DataManager import DataManager
# Importation de toutes les classes et fonctions de tkinter
from tkinter import *
# Importation de la classe messagebox depuis le module tkinter pour afficher des boîtes de dialogue
from tkinter import messagebox
# Importation de customtkinter pour personnaliser l'apparence des widgets tkinter
import customtkinter as ctk
# Importation du module hashlib pour le hachage des mots de passe
import hashlib
# Importation du module re pour utiliser des expressions régulières
import re
# Importation de la fonction path depuis le module os pour manipuler les chemins de fichiers
from os import path
# Importation de la classe BooleanVar depuis le module tkinter pour stocker des valeurs booléennes
import Kamikaze
import Blackjack
# Initialisation de la connexion à la base de données
dataManager = DataManager('localhost', 'root', '', 's&m')
dataManager.Connect()
cursor = dataManager.connection.cursor()

# Fonction pour appliquer un thème à Tkinter
def apply_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

# Fonction pour enregistrer un utilisateur
def register_user(username, password, verify_password, register_window):
    try:
        # Vérification si le mot de passe répond aux exigences
        if not (re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[!@#$%^&*(),.?\":{}|<>]", password) and len(password) >= 8):
            messagebox.showerror("Error", "Le mot de passe doit contenir au moins 1 majuscule, 1 minuscule, 1 caractère spécial et doit avoir une longueur d'au moins 8 caractères.")
            return
        
        # Vérification si les mots de passe correspondent
        if password != verify_password:
            messagebox.showerror("Error", "Les mots de passe ne correspondent pas.")
            return

        # Hachage du mot de passe
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insertion de l'utilisateur dans la base de données
        insert_query = "INSERT INTO users (UserName, Password) VALUES (%s, %s)"
        data = (username, hashed_password)
        cursor.execute(insert_query, data)
        dataManager.connection.commit()
        messagebox.showinfo("Success", "Inscription réussie!")
        
        # Fermeture de la fenêtre d'inscription
        register_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Échec de l'inscription: {str(e)}")

# Fonction pour afficher la fenêtre d'inscription
def register_window():
    # Fonction pour basculer la visibilité du mot de passe
    def toggle_password_visibility():
        if show_password.get():
            # Afficher le mot de passe
            champVerifyMdp.configure(show="")
            champMdp.configure(show="")
        else:
            # Masquer le mot de passe
            champVerifyMdp.configure(show="*")
            champMdp.configure(show="*")

    # Création de la fenêtre d'inscription
    register_window = Toplevel()
    register_window.geometry("600x400")
    register_window.title("S&M Inscription")

    frame = ctk.CTkFrame(master=register_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="S'inscrire")
    label.pack(pady=12, padx=10)

    champUserName = ctk.CTkEntry(master=frame, placeholder_text="Nom d'utilisateur")
    champUserName.pack(pady=12)

    champMdp = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
    champMdp.pack(pady=12)

    champVerifyMdp = ctk.CTkEntry(master=frame, placeholder_text="Vérifier le mot de passe", show="*")
    champVerifyMdp.pack(pady=12)

    show_password = BooleanVar()
    show_checkbox = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", variable=show_password, command=toggle_password_visibility)
    show_checkbox.pack(pady=12, padx=10)

    ButtonInscrip = ctk.CTkButton(master=frame, text="Inscription", command=lambda: register_user(champUserName.get(), champMdp.get(), champVerifyMdp.get(), register_window))
    ButtonInscrip.pack(pady=12, padx=10)

    annulerInsc = ctk.CTkButton(master=frame, text="Annuler", command=register_window.destroy)
    annulerInsc.pack(pady=12, padx=10)

# Fonction pour la connexion de l'utilisateur
def login():
    username = champ1.get()
    password = champ2.get()

    try:
        # Hachage du mot de passe
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Vérification si l'utilisateur existe
        query = "SELECT * FROM users WHERE UserName = %s AND Password = %s"
        data = (username, hashed_password)
        cursor.execute(query, data)
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Connexion réussie!")
            home_page(username)  # Ouvrir la page d'accueil
            main_window.withdraw() # Cacher la fenêtre de connexion
        else:
            messagebox.showerror("Error", "Nom d'utilisateur ou mot de passe invalide!")
    except Exception as e:
        messagebox.showerror("Error", f"Échec de la connexion: {str(e)}")

# Fonction pour afficher ou masquer le mot de passe
def show_password():
    if checkbox_var.get():
        champ2.configure(show="")
    else:
        champ2.configure(show="*")

# Fonction pour afficher la page d'accueil
def home_page(username):
    def modify_user():
        def update_user():
            new_username = new_username_entry.get()
            new_password = new_password_entry.get()

            try:
                # Vérification si le mot de passe répond aux exigences
                if not (re.search("[a-z]", new_password) and re.search("[A-Z]", new_password) and re.search("[!@#$%^&*(),.?\":{}|<>]", new_password) and len(new_password) >= 8):
                    messagebox.showerror("Error", "Le mot de passe doit contenir au moins 1 majuscule, 1 minuscule, 1 caractère spécial et doit avoir une longueur d'au moins 8 caractères.")
                    return

                # Hachage du mot de passe
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

                # Mise à jour des informations de l'utilisateur dans la base de données
                update_query = "UPDATE users SET UserName = %s, Password = %s WHERE UserName = %s"
                data = (new_username, hashed_password, username)
                cursor.execute(update_query, data)
                dataManager.connection.commit()

                messagebox.showinfo("Success", "Informations utilisateur mises à jour avec succès!")
                modify_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Échec de la mise à jour des informations utilisateur: {str(e)}")

        modify_window = Toplevel()
        modify_window.geometry("400x300")
        modify_window.title("Modifier l'utilisateur")

        # Étiquettes et Entrées pour le nom d'utilisateur et le mot de passe
        username_label = ctk.CTkLabel(master=modify_window, text="Nouveau nom d'utilisateur:")
        username_label.pack(pady=10)
        new_username_entry = ctk.CTkEntry(master=modify_window)
        new_username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(master=modify_window, text="Nouveau mot de passe:")
        password_label.pack(pady=10)
        new_password_entry = ctk.CTkEntry(master=modify_window, show="*")
        new_password_entry.pack(pady=5)

        # Bouton pour déclencher la fonction update_user
        update_button = ctk.CTkButton(master=modify_window, text="Modifier", command=update_user)
        update_button.pack(pady=20)

    def quit_app():
        home_window.withdraw() # Fermer la fenêtre d'accueil

    # Créer une nouvelle fenêtre pour la page d'accueil
    home_window = Toplevel()
    home_window.geometry("600x400")
    home_window.title("S&M Accueil")

    frame = ctk.CTkFrame(master=home_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    # Ajouter du contenu à la page d'accueil
    label = ctk.CTkLabel(master=frame, text=f"Bienvenue sur Sirtoez&Melangez, {username}!")
    label.pack(pady=20)

    # Créer le menu
    menu = Menu(home_window)
    home_window.config(menu=menu)

    # Menu Utilisateur
    user_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Utilisateur", menu=user_menu)
    user_menu.add_command(label="Modifier l'utilisateur", command=modify_user)
    user_menu.add_separator()
    user_menu.add_command(label="Quitter", command=quit_app)

    # Fermer la fenêtre de connexion
    main_window.withdraw()

# Créer la fenêtre principale de connexion
main_window = ctk.CTk()
main_window.geometry("600x400")
main_window.title("S&M Connexion")

# Créer la variable de contrôle pour la case à cocher
checkbox_var = BooleanVar()

frame = ctk.CTkFrame(master=main_window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Se connecter")
label.pack(pady=12, padx=10)

champ1 = ctk.CTkEntry(master=frame, placeholder_text="Identifiant")
champ1.pack(pady=12)

champ2 = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
champ2.pack(pady=12)

checkbox = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", variable=checkbox_var, command=show_password)
checkbox.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Connexion", command=login)
button.pack(pady=12, padx=10)

button2 = ctk.CTkButton(master=frame, text="Vous n'êtes pas inscrit, inscrivez-vous ICI ", command=register_window)
button2.pack(pady=12, padx=10)

main_window.mainloop()
