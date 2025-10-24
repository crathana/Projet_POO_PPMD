import numpy as np

### Code du jeu du démineur sur terminal

class Grille:
    def __init__(self, difficulte):
        
        if difficulte == "Facile":
            self.taille = (8,10)
            self.nb_bombes = 10
        elif difficulte =="Moyen":
            self.taille = (14,18)
            self.nb_bombes = 40
        elif difficulte == "Difficile":
            self.taille = (20,24)
            self.nb_bombes = 99
        
        self.nb_bombes_restantes = self.nb_bombes

        self.etat_grille = "En cours"

    def generer_grille(self,case_depart):
        grille = np.zeros(self.taille)
        bombes=[]


class Case:
    def __init__(self):
        


if __name__ == "__main__":

    grille=Grille("Facile")

    print(grille.generer_grille())
