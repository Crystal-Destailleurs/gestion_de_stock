from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123soleil",
    database="store"
)

# Créer un curseur pour exécuter les requêtes
cursor = conn.cursor()

def lister_categories():
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    return categories

def lister_produits():
    cursor.execute("SELECT * FROM product")
    produits = cursor.fetchall()
    return produits

def ajouter_produit(name, description, price, quantity, id_category):
    query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
    values = (name, description, price, quantity, id_category)
    cursor.execute(query, values)
    conn.commit()

def supprimer_produit(id_produit):
    query = "DELETE FROM product WHERE id=%s"
    values = (id_produit,)
    cursor.execute(query, values)
    conn.commit()

def afficher_categories_combo(combo):
    categories = lister_categories()
    noms_categories = [categorie[1] for categorie in categories]
    combo['values'] = noms_categories

def afficher_produits_gui():
    fenetre_produits = Tk()
    fenetre_produits.title("Liste des produits")

    # Création du tableau pour afficher les produits
    tableau_produits = ttk.Treeview(fenetre_produits)
    tableau_produits['columns'] = ('Nom', 'Description', 'Prix', 'Quantité', 'Catégorie')
    tableau_produits.heading('Nom', text='Nom')
    tableau_produits.heading('Description', text='Description')
    tableau_produits.heading('Prix', text='Prix')
    tableau_produits.heading('Quantité', text='Quantité')
    tableau_produits.heading('Catégorie', text='Catégorie')

    produits = lister_produits()
    for produit in produits:
        tableau_produits.insert('', 'end', values=produit)

    tableau_produits.pack()

    # Bouton pour supprimer le produit sélectionné
    def supprimer_selection():
        selection = tableau_produits.selection()
        if selection:
            id_produit = tableau_produits.item(selection)['values'][0]  # ID du produit sélectionné
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce produit ?"):
                supprimer_produit(id_produit)
                messagebox.showinfo("Succès", "Produit supprimé avec succès.")
                # Actualiser l'affichage après la suppression
                tableau_produits.delete(*tableau_produits.get_children())
                produits = lister_produits()
                for produit in produits:
                    tableau_produits.insert('', 'end', values=produit)

    bouton_supprimer = Button(fenetre_produits, text="Supprimer", command=supprimer_selection)
    bouton_supprimer.pack(pady=10)

    fenetre_produits.mainloop()

def ajouter_produit_gui():
    fenetre_ajout = Tk()
    fenetre_ajout.title("Ajouter un produit")

    # Labels et Entry pour saisir les informations du produit
    label_nom = Label(fenetre_ajout, text="Nom du produit:")
    label_nom.grid(row=0, column=0, padx=5, pady=5)
    entry_nom = Entry(fenetre_ajout)
    entry_nom.grid(row=0, column=1, padx=5, pady=5)

    label_description = Label(fenetre_ajout, text="Description:")
    label_description.grid(row=1, column=0, padx=5, pady=5)
    entry_description = Entry(fenetre_ajout)
    entry_description.grid(row=1, column=1, padx=5, pady=5)

    label_prix = Label(fenetre_ajout, text="Prix:")
    label_prix.grid(row=2, column=0, padx=5, pady=5)
    entry_prix = Entry(fenetre_ajout)
    entry_prix.grid(row=2, column=1, padx=5, pady=5)

    label_quantite = Label(fenetre_ajout, text="Quantité:")
    label_quantite.grid(row=3, column=0, padx=5, pady=5)
    entry_quantite = Entry(fenetre_ajout)
    entry_quantite.grid(row=3, column=1, padx=5, pady=5)

    label_categorie = Label(fenetre_ajout, text="Catégorie:")
    label_categorie.grid(row=4, column=0, padx=5, pady=5)

    # ComboBox pour choisir la catégorie
    combo_categorie = ttk.Combobox(fenetre_ajout, width=30)
    combo_categorie.grid(row=4, column=1, padx=5, pady=5)
    afficher_categories_combo(combo_categorie)

    # Fonction pour ajouter le produit à la base de données
    def valider_ajout():
        nom = entry_nom.get()
        description = entry_description.get()
        prix = entry_prix.get()
        quantite = entry_quantite.get()
        nom_categorie = combo_categorie.get()

        # Récupérer l'ID de la catégorie sélectionnée
        cursor.execute("SELECT id FROM category WHERE name = %s", (nom_categorie,))
        id_categorie = cursor.fetchone()[0]

        ajouter_produit(nom, description, prix, quantite, id_categorie)
        messagebox.showinfo("Succès", "Produit ajouté avec succès")
        fenetre_ajout.destroy()

    # Bouton pour valider
    bouton_valider = Button(fenetre_ajout, text="Valider", command=valider_ajout)
    bouton_valider.grid(row=5, column=0, columnspan=2)

    fenetre_ajout.mainloop()

# Exemple d'utilisation
ajouter_produit_gui()
afficher_produits_gui()
