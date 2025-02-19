import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importation de Pillow


class Chapitre:
    def __init__(self, titre, resume, contenu, images_paths=[]):
        self.titre = titre
        self.resume = resume
        self.contenu = contenu
        self.images_paths = images_paths  # Liste des chemins des images


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Répertoire de Connaissances en Bio")
        self.root.geometry("900x600")

        # Mode par défaut : clair
        self.mode_sombre = False

        # Liste des chapitres avec des images
        self.chapitres = [
            Chapitre(
                "Génétique",
                "Introduction à la génétique.",
                "Contenu détaillé sur la génétique...",
                ["genetique_image1.jpg", "genetique_image2.jpg", "genetique_image3.jpg"]
            ),
            Chapitre(
                "Biologie cellulaire",
                "Fonctions et structures des cellules.",
                "Contenu détaillé sur la biologie cellulaire...",
                ["cellulaire_image1.jpg", "cellulaire_image2.jpg"]
            )
        ]

        # Cadre de navigation (table des matières)
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.chapitre_buttons = []
        for chapitre in self.chapitres:
            button = tk.Button(self.navigation_frame, text=chapitre.titre,
                               command=lambda c=chapitre: self.afficher_contenu(c))
            button.pack(fill="x", pady=5)
            self.chapitre_buttons.append(button)

        # Cadre d'affichage du contenu
        self.contenu_frame = tk.Frame(self.root)
        self.contenu_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.titre_label = tk.Label(self.contenu_frame, text="", font=("Arial", 16, "bold"))
        self.titre_label.pack(pady=10)

        self.contenu_text = tk.Text(self.contenu_frame, wrap="word", height=10, width=50)
        self.contenu_text.pack()

        # Cadre pour afficher la galerie d'images
        self.galerie_frame = tk.Frame(self.contenu_frame)
        self.galerie_frame.pack(pady=10)

        # Label pour afficher l'image en taille réelle
        self.image_label = tk.Label(self.contenu_frame)
        self.image_label.pack(pady=10)

        # Bouton pour basculer entre le mode sombre et clair
        self.toggle_button = tk.Button(self.root, text="Passer au mode sombre", command=self.toggle_mode)
        self.toggle_button.pack(pady=10)

        # Appliquer les couleurs par défaut (mode clair)
        self.apply_light_mode()

    def afficher_contenu(self, chapitre):
        # Affichage du titre et du texte
        self.titre_label.config(text=chapitre.titre)
        self.contenu_text.delete(1.0, tk.END)
        self.contenu_text.insert(tk.END, chapitre.contenu)

        # Effacer les anciennes vignettes d'image
        for widget in self.galerie_frame.winfo_children():
            widget.destroy()

        # Créer des vignettes d'image pour chaque image du chapitre
        for image_path in chapitre.images_paths:
            # Charger l'image et la redimensionner en petite taille (vignette)
            try:
                image = Image.open(image_path)
                image.thumbnail((100, 100))  # Redimensionner l'image pour créer la vignette
                photo = ImageTk.PhotoImage(image)

                # Créer un bouton avec la vignette
                button = tk.Button(self.galerie_frame, image=photo,
                                   command=lambda img=image_path: self.afficher_image(img))
                button.image = photo  # Sauvegarder la référence de l'image
                button.pack(side="left", padx=5, pady=5)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image : {e}")

    def afficher_image(self, image_path):
        # Afficher l'image en taille réelle lorsqu'une vignette est cliquée
        try:
            image = Image.open(image_path)
            image = image.resize((400, 300))  # Redimensionner pour l'affichage en taille réelle
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Sauvegarder la référence de l'image
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher l'image : {e}")

    def toggle_mode(self):
        # Basculer entre le mode sombre et le mode clair
        self.mode_sombre = not self.mode_sombre

        if self.mode_sombre:
            self.apply_dark_mode()
            self.toggle_button.config(text="Passer au mode clair")
        else:
            self.apply_light_mode()
            self.toggle_button.config(text="Passer au mode sombre")

    def apply_dark_mode(self):
        # Appliquer les couleurs du mode sombre
        self.root.config(bg="black")
        self.navigation_frame.config(bg="black")
        self.contenu_frame.config(bg="black")
        self.titre_label.config(fg="white", bg="black")
        self.contenu_text.config(bg="gray20", fg="white")
        self.toggle_button.config(bg="gray30", fg="white")

        for button in self.chapitre_buttons:
            button.config(bg="gray20", fg="white")

    def apply_light_mode(self):
        # Appliquer les couleurs du mode clair
        self.root.config(bg="white")
        self.navigation_frame.config(bg="white")
        self.contenu_frame.config(bg="white")
        self.titre_label.config(fg="black", bg="white")
        self.contenu_text.config(bg="white", fg="black")
        self.toggle_button.config(bg="lightgray", fg="black")

        for button in self.chapitre_buttons:
            button.config(bg="white", fg="black")


# Création de la fenêtre principale
root = tk.Tk()
app = App(root)
root.mainloop()