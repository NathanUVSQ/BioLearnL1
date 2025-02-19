import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importation de Pillow


class Chapitre:
    def __init__(self, titre, resume, contenu, images_paths=[], favoris=False):
        self.titre = titre
        self.resume = resume
        self.contenu = contenu
        self.images_paths = images_paths  # Liste des chemins des images
        self.favoris = favoris  # Indicateur de chapitre favori



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Répertoire de Connaissances en Bio")
        self.root.geometry("1000x600")

        # Mode par défaut : clair
        self.mode_sombre = False

        # Liste des chapitres avec des images
        self.chapitres = [
            Chapitre(
                "Bi202: Biologie moléculaire et cellulaire, le microscope",
                "Bi202",
                "être vivant: \n un systeme organisé \n capable de synthétiser et de dégrader (anabolisme/catabolisme) \n se reproduit \n naissance et mort \n dynamique \n \n \n Cellule: 25 micro-m, entre 1 et 1000 micro-m cube \n \n MICROSCOPE: \n optique 400/700 nm, filtre: contraste de phase, interférence différentielle, fond noir, fond clair \n microscope confocal = plusieurs plan plus détaillé. \n prélevement \n fixation \n inclusion \n Microtome \n Lame \n Marquage (cytochimie, immunocytochimie, cytoenzymologie) \n \n EPIFLUORESCENCE: \n fluorochrome: Molécules fluorescente quand excité par onde spécifique. emet une onde plus grande mais moins energétique. \n \n \n ELECTRONIQUE: \n MEB: moins précis, ne traverse pas les couches, colonne sous vide \n MET: plus précis, ultraMicrotome, traitement métaux : ombrage \n cryofracture: congelé avec azote, ouvre bicouches, Réplique + ombrage(45 degrés) ",
                ["genetique_image1.jpg", "genetique_image2.jpg", "genetique_image3.jpg"]
            ),
            Chapitre(
                "Bi202: Biologie moléculaire et cellulaire, La cellule",
                "la cellule",
                "NOYAUX: Gros élément sphérique central délimité par deux membranes apellé enveloppe. Il y a dessus des ports nucléaires et d'autres édifices controlant les échanges \n fonction: stocke info génétique, contrôle expression des gènes, duplique ADN. \n Composition: euchromatine: moins dense comparé à hétérochromatine | Nucléole: site ARN ribosomique et maturation + assemblage sous unités \n \n RETICULUM ENDOPLASMIQUE (RE) \n réseau de membrane interconnecté délimitant des cavités l'interieur des cavité est nommé Lumen. \n deux types: RER rugueux ou granuleux et REL lisse. \n Fonction: REL: stockage calcium, messageavec, synthèse lipide, détoxification... RER: traduction de 30% de la voie de sécrétion, modification post trad, transmet à l'appareil de Golgi. \n \n APPAREIL DE GOLGI: \n forme de demi cercle, ensemble de sacs membranaires = saccules \n Fonction: modif post trad + trie en fonction de la destination \n \n VESICULES: \n élément sphériques délimité par une membrane \n type de vésilules: EXOCYTOSE (libère contenu à l'exterieur, mvt centrifuge) et ENDOCYTOSE (prélève élément, mvt centripète) \n \n LYSOSOME: \n Fonction: dégrade constituant non fonctionel et/ou pathogène avec des enzymes comme les protéases, nucléases, lipase, hydrolase... \n \n PEROXYSOME: \n Fonction: réaction d'oxydation acides gras ou peroxyde d'hydrogène",
                ["cellulaire_image1.jpg", "cellulaire_image2.jpg"]
            )
        ]

        # Cadre de contrôle du mode sombre et de navigation
        self.control_frame = tk.Frame(self.root, pady=10)
        self.control_frame.pack(fill="x", side="top", padx=20)

        self.show_favoris_button = tk.Button(self.control_frame, text="Afficher les favoris",
                                             command=self.afficher_favoris, width=20)
        self.show_favoris_button.pack(side="left", padx=5)

        self.show_all_button = tk.Button(self.control_frame, text="Afficher tous les chapitres",
                                         command=self.afficher_tous, width=20)
        self.show_all_button.pack(side="left", padx=5)

        # Bouton pour basculer entre le mode sombre et clair
        self.toggle_button = tk.Button(self.control_frame, text="Passer au mode sombre", command=self.toggle_mode,
                                       width=20)
        self.toggle_button.pack(side="right", padx=5)

        # Cadre de navigation (table des matières)
        self.navigation_frame = tk.Frame(self.root, width=200, bg="#f0f0f0", pady=10)
        self.navigation_frame.pack(side="left", fill="y", padx=10)

        self.chapitre_buttons = []
        for chapitre in self.chapitres:
            button = tk.Button(self.navigation_frame, text=chapitre.resume,
                               command=lambda c=chapitre: self.afficher_contenu(c), width=20)
            button.pack(fill="x", pady=5)
            self.chapitre_buttons.append(button)

        # Cadre d'affichage du contenu
        self.contenu_frame = tk.Frame(self.root, pady=10)
        self.contenu_frame.pack(side="right", fill="both", expand=True, padx=20)

        self.titre_label = tk.Label(self.contenu_frame, text="", font=("Arial", 16, "bold"))
        self.titre_label.pack(pady=10)



        # Créer un widget Text pour afficher le contenu
        self.contenu_text = tk.Text(self.contenu_frame, wrap="word", height=10, width=50, font = "Arial")
        self.contenu_text.pack(fill="both", expand=True)  # Utilisation de 'expand=True' pour remplir l'espace

        # Créer une balise "rouge" pour le texte
        self.contenu_text.tag_configure("rouge", foreground="red")

        # Cadre pour afficher la galerie d'images
        self.galerie_frame = tk.Frame(self.contenu_frame)
        self.galerie_frame.pack(pady=10)

        # Label pour afficher l'image en taille réelle
        self.image_label = tk.Label(self.contenu_frame)
        self.image_label.pack(pady=10)

        # Bouton pour ajouter aux favoris
        self.add_fav_button = tk.Button(self.contenu_frame, text="Ajouter aux favoris", command=self.toggle_favoris,
                                        width=30)
        self.add_fav_button.pack(pady=10)

        # Appliquer les couleurs par défaut (mode clair)
        self.apply_light_mode()



    def rechercher(self):
        # Récupérer le mot-clé de la recherche
        keyword = self.search_entry.get().lower()

        if not keyword:
            messagebox.showinfo("Recherche", "Veuillez entrer un mot-clé.")
            return

        # Filtrer les chapitres contenant le mot-clé
        resultats = []
        for chapitre in self.chapitres:
            if (keyword in chapitre.titre.lower() or
                    keyword in chapitre.resume.lower() or
                    keyword in chapitre.contenu.lower()):
                resultats.append(chapitre)

        # Si des chapitres ont été trouvés, les afficher
        if resultats:
            self.afficher_chapitres(resultats)
        else:
            messagebox.showinfo("Recherche", f"Aucun chapitre trouvé pour '{keyword}'.")

    def afficher_favoris(self):
        # Afficher uniquement les chapitres favoris
        favoris_chapitres = [chapitre for chapitre in self.chapitres if chapitre.favoris]
        if favoris_chapitres:
            self.afficher_chapitres(favoris_chapitres)
        else:
            messagebox.showinfo("Favoris", "Aucun chapitre favori.")

    def afficher_tous(self):
        # Afficher tous les chapitres
        self.afficher_chapitres(self.chapitres)

    def afficher_chapitres(self, chapitres):
        # Effacer les anciens boutons de chapitres
        for widget in self.navigation_frame.winfo_children():
            widget.destroy()

        # Créer des boutons pour chaque chapitre trouvé
        for chapitre in chapitres:
            button = tk.Button(self.navigation_frame, text=chapitre.titre,
                               command=lambda c=chapitre: self.afficher_contenu(c), width=20)
            button.pack(fill="x", pady=5)

    def toggle_favoris(self):
        # Basculer l'état des favoris pour le chapitre actuellement affiché
        chapitre_actuel = self.get_chapitre_actuel()
        chapitre_actuel.favoris = not chapitre_actuel.favoris

        # Mise à jour de l'affichage
        self.afficher_contenu(chapitre_actuel)

    def afficher_contenu(self, chapitre):
        # Affichage du titre et du texte
        self.titre_label.config(text=chapitre.titre)
        self.contenu_text.delete(1.0, tk.END)
        self.contenu_text.insert(tk.END, chapitre.contenu)

        # Effacer les anciennes vignettes d'image
        for widget in self.galerie_frame.winfo_children():
            widget.destroy()

        # Chercher les mots dans le texte et l'appliquer en rouge
        keywords = ["cellule", "taxons", ""]
        for i in keywords:
            start_index = self.contenu_text.search(i, 1.0, tk.END)
            if start_index:
                end_index = f"{start_index}+{len(i)}c"
                self.contenu_text.tag_add("rouge", start_index, end_index)

        # Créer des vignettes d'image pour chaque image du chapitre
        for image_path in chapitre.images_paths:
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

        # Afficher ou masquer le bouton "Ajouter aux favoris" en fonction de l'état actuel du chapitre
        if chapitre.favoris:
            self.add_fav_button.config(text="Retirer des favoris")
        else:
            self.add_fav_button.config(text="Ajouter aux favoris")

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

    def get_chapitre_actuel(self):
        # Retourner le chapitre actuellement affiché
        for chapitre in self.chapitres:
            if self.titre_label.cget("text") == chapitre.titre:
                return chapitre
        return None

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
            button.config(bg="lightgray", fg="black")


# Initialisation de l'application
root = tk.Tk()
app = App(root)
root.mainloop()
