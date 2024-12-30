import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Validation des images
def validate_image(image_path):
    try:
        # Vérification de l'extension
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError(f"Format de fichier non supporté : {image_path}")
            
        # Vérification de la taille maximale (5MB)
        if os.path.getsize(image_path) > 5 * 1024 * 1024:
            raise ValueError(f"Image trop grande : {image_path}")
            
        # Vérification que c'est bien une image valide
        with Image.open(image_path) as img:
            img.verify()
            
        return True
    except Exception as e:
        messagebox.showerror("Erreur", f"Image invalide : {str(e)}")
        return False

# Initialisation des cartes avec des images
def generate_cards():
    try:
        # Créer une liste de 8 paires d'images
        images = ["14579.png", "14601.png", "14652.png", "14653.png", 
                 "14654.png", "14668.png", "14694.png", "14718.png"]
        
        # Valider toutes les images avant de continuer
        valid_images = [img for img in images if validate_image(img)]
        if len(valid_images) < len(images):
            raise ValueError("Certaines images sont invalides")
            
        cards = valid_images * 2  # 2 fois chaque image
        random.shuffle(cards)  # Mélanger les images
        return cards
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération des cartes : {str(e)}")
        return []

# Classe du jeu
class MemoryGame:
    MAX_MEMORY = 100 * 1024 * 1024  # 100MB limite
    
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Mémoire")
        self.memory_usage = 0

        self.cards = generate_cards()
        if not self.cards:  # Si pas de cartes valides
            self.root.quit()
            return

        self.buttons = []
        self.flipped_cards = []
        self.matched_pairs = 0
        self.total_pairs = len(self.cards) // 2
        self.images = {}  # Dictionnaire pour stocker les images des cartes
        
        try:
            # Charger les images de la carte arrière
            if not validate_image("card_back.png"):
                raise ValueError("Image de dos de carte invalide")
                
            self.card_back = self.load_image("card_back.png")
            if not self.card_back:
                raise ValueError("Impossible de charger l'image de dos de carte")

            # Charger toutes les images des cartes
            self.load_all_images()
            
            # Créer l'interface
            self.create_interface()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'initialisation : {str(e)}")
            self.root.quit()

    def load_image(self, image_path, size=(100, 100)):
        try:
            img_size = os.path.getsize(image_path)
            self.track_memory(img_size)
            
            with Image.open(image_path) as img:
                img = img.resize(size)
                return ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image {image_path}: {str(e)}")
            return None

    def track_memory(self, image_size):
        self.memory_usage += image_size
        if self.memory_usage > self.MAX_MEMORY:
            raise MemoryError("Limite de mémoire dépassée")

    def load_all_images(self):
        try:
            for img in set(self.cards):
                loaded_image = self.load_image(img)
                if loaded_image:
                    self.images[img] = loaded_image
                else:
                    raise ValueError(f"Impossible de charger l'image: {img}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            raise

    def create_interface(self):
        # Créer une grille de boutons pour représenter les cartes
        for i in range(4):  # 4 rangées
            row = []
            for j in range(4):  # 4 colonnes
                button = tk.Button(self.root, image=self.card_back, width=100, height=100,
                                 command=lambda i=i, j=j: self.flip_card(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def flip_card(self, row, col):
        try:
            # Retourner la carte à la position donnée (row, col)
            button = self.buttons[row][col]
            card_index = row * 4 + col
            card_value = self.cards[card_index]

            if button["image"] == str(self.card_back) and len(self.flipped_cards) < 2:
                button["image"] = self.images[card_value]
                self.flipped_cards.append((row, col, card_value))

                # Vérifier si deux cartes sont retournées
                if len(self.flipped_cards) == 2:
                    self.check_match()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du retournement de la carte : {str(e)}")

    def check_match(self):
        try:
            # Vérifier si les deux cartes retournées sont identiques
            (row1, col1, value1), (row2, col2, value2) = self.flipped_cards

            if value1 == value2:  # Si les cartes sont identiques
                self.matched_pairs += 1
                self.flipped_cards = []  # Réinitialiser les cartes retournées
                if self.matched_pairs == self.total_pairs:  # Si toutes les paires sont trouvées
                    self.show_win_message()
            else:
                # Si les cartes ne correspondent pas, les retourner à l'envers après un délai
                self.root.after(500, self.hide_cards, row1, col1, row2, col2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la vérification des cartes : {str(e)}")

    def hide_cards(self, row1, col1, row2, col2):
        try:
            self.buttons[row1][col1]["image"] = self.card_back
            self.buttons[row2][col2]["image"] = self.card_back
            self.flipped_cards = []  # Réinitialiser les cartes retournées
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du masquage des cartes : {str(e)}")

    def show_win_message(self):
        messagebox.showinfo("Félicitations!", "Vous avez trouvé toutes les paires!")
        self.root.quit()

# Créer la fenêtre principale
if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = MemoryGame(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erreur Fatale", f"Une erreur critique est survenue : {str(e)}")
