import random

class Carte:
    def __init__(self, value, forme):
        self.valeur = value  # Valeur de la carte (par exemple : "2", "3", "4", ..., "Valet", "Reine", "Roi", "1")
        self.forme = forme    # Forme de la carte (par exemple : "Coeur", "Carreau", "Pique", "Trèfle")

    def Nom_Carte(self):
        return self.valeur + self.forme[0]  # Méthode pour obtenir le nom complet de la carte correspondant au nom de l'image

    def Puissance(self):
        if self.valeur.isdigit():
            return int(self.valeur)
        elif self.valeur == "J":
            return 11
        elif self.valeur == "Q":
            return 12
        elif self.valeur == "K":
            return 13 
        elif self.valeur == "A":
            return 14
        else:
            return 0

class Cartes:
    def __init__(self):
        valeurs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        formes = ["c", "h", "d", "s"]

        self.cartes = []
        for forme in formes:
            for value in valeurs: 
                self.cartes.append(Carte(value, forme))
        self.cartes_reservees = self.cartes.copy()

    def Nom_Carte(self):
        return self.valeur + self.forme[0]

    def Melanger(self):
        random.shuffle(self.cartes)
        self.cartes_reservees = self.cartes.copy()

    def __len__(self):
        return len(self.cartes)

    def Tirer(self):
        if self.cartes:
            indice = random.randint(0, len(self.cartes)-1)
            ma_carte = self.cartes.pop(indice)
            return ma_carte
        else:
            print("Le jeu de cartes est vide.")
            return None

    def PiocherCartes(self, nombre):
        cartes_piochees = []
        for _ in range(nombre):
            if self.cartes_reservees:
                indice = random.randint(0, len(self.cartes_reservees)-1)
                carte = self.cartes_reservees.pop(indice)
                cartes_piochees.append(carte)
            else:
                print("La réserve de cartes est vide.")
                break
        return cartes_piochees

