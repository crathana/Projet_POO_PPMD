import numpy as np
import random
import os 


### Code du jeu du démineur sur terminal

class Case:
    def __init__(self):
        self.etat_case = 0  # 0: cachée, 1: révélée, -1: marquée
        self.affichage = "□" # l'affichage de base

    def definir_affichage_drapeau(self):
        """Choisit une pièce d'échec aléatoire et définit son chemin d’image."""
        pieces_echec = {0: "pion", 1: "tour", 2: "cavalier", 3: "fou", 4: "dame", 5: "roi"}
        tirage = random.randint(0, 5)

        dossier_courant = os.path.dirname(__file__)
        chemin_image = os.path.join(dossier_courant, "images_drapeaux", f"{pieces_echec[tirage]}.png")

        self.affichage = chemin_image


    def cocher_case(self):
        if self.etat_case == 0:  # seulement si elle est cachée
            self.etat_case = -1
            self.definir_affichage_drapeau()
            

    def decocher_case(self):
        if self.etat_case == -1: # seulement s'il y a un drapeau
            self.etat_case = 0
            self.affichage = "□"

    def reveler_case(self):
        if self.etat_case == 0:  # seulement si elle est cachée
            self.etat_case = 1


class Case_safe(Case):
    def __init__(self, nb_voisins):
        super().__init__()
        self.type_case="safe"
        self.nb_voisins = nb_voisins # Doit afficher el nombre de bombes aux alentours

    def reveler_case(self):
        if self.etat_case == 0:  # seulement si elle est cachée
            self.etat_case = 1
            self.affichage = self.nb_voisins


class Case_bombe(Case):
    def __init__(self):
        super().__init__()
        self.type_case = "bombe"
    
    def reveler_case(self):
        if self.etat_case == 0:  # seulement si elle est cachée
            self.etat_case = 1
            dossier_courant = os.path.dirname(__file__)
            chemin_image = os.path.join(dossier_courant, "images_drapeaux", "dame_noire.png")
            self.affichage = chemin_image

    


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
        
        self.nb_cases_safe = self.taille[0]*self.taille[1] - self.nb_bombes

        self.etat_grille = 0 # 0: en cours, 1: grille réussie, -1: grille échouée

        self.grille = [[Case() for _ in range(self.taille[1])] for _ in range(self.taille[0])]

    def voisins(self, x, y):
        """ Renvoie une liste des coordonnées des cases voisines à la case (x,y) dans les limites de la grille"""
        liste = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                rr, cc = x + dx, y + dy
                if 0 <= rr < self.taille[0] and 0 <= cc < self.taille[1]:
                    liste.append((rr, cc)) 
        return liste

    def generer_grille(self,case_depart):
        """ Génère la grille de telle sorte à ce qu'il n'y ait pas de bombes sur la case de départ choisie par le joueur"""
        bombes=[]
        voisins = self.voisins(case_depart[0],case_depart[1])
        for i in range(self.nb_bombes):
            x = random.randint(0,self.taille[0]-1)
            y = random.randint(0,self.taille[1]-1)
            while (x,y) in bombes or (x,y) == case_depart or (x,y) in voisins:
                x = random.randint(0,self.taille[0]-1)
                y = random.randint(0,self.taille[1]-1)
            bombes.append((x,y))
        
        for bombe in bombes:
            self.grille[bombe[0]][bombe[1]] = Case_bombe()

        for r in range(self.taille[0]):
            for c in range(self.taille[1]):
                if not isinstance(self.grille[r][c], Case_bombe):
                    nb = self.nb_bombes_voisines(r, c)
                    self.grille[r][c] = Case_safe(nb)
        return self.grille
    
    def nb_bombes_voisines(self, x, y):
        """ Calcule le nombre de bombes dans un rayon de 1 case autour de la case (x,y)"""
        count = 0
        for (i, j) in self.voisins(x, y):
            if isinstance(self.grille[i][j], Case_bombe):
                count += 1
        return count
    
    def afficher_grille(self):
        """ Gère l'affichage de la grille dans son état actuel"""
        for r in range(self.taille[0]):
            ligne = ""
            for c in range(self.taille[1]):
                case = self.grille[r][c]
                ligne += f" {case.affichage} "
            print(ligne)

    def reveler(self, x, y):
        """ Permet de révéler la case (x,y)"""
        case = self.grille[x][y]

        # Si déjà révélée ou marquée, on ne fait rien
        if case.etat_case != 0:
            return

        # On révèle la case
        case.reveler_case()
        self.nb_cases_safe-=1

        # Si c'est une bombe c'est ciao
        if isinstance(case, Case_bombe):
            self.etat_grille = -1
            return

        if case.affichage > 0:
            return
        # Récursivité qui permet de révéler les cases voisines de la case révélée si cette case ne possède aucune bombe adjacente
        for (rr, cc) in self.voisins(x, y):
            if self.grille[rr][cc].etat_case == 0:
                self.reveler(rr, cc)
            

    def cocher(self,x,y):
        """ Permet de placer un drapeau sur la case (x,y)"""
        self.grille[x][y].cocher_case()

    def decocher_case(self,x,y):
        """ Permet de retirer un drapeau de la case (x,y)"""
        self.grille[x][y].decocher_case()
    
    def test_grille_finie(self):
        """ Teste si la grille est finie et place l'état de la grille sur 1"""
        if self.nb_cases_safe == 0:
            self.etat_grille = 1
    
    def fin_partie(self):
        """ Détermine la fin de la partie"""
        if self.etat_grille == 1:
            return "Vous avez gagné !"
        
        if self.etat_grille == -1:
            return "Vous avez perdu !"







if __name__ == "__main__":

    grille=Grille("Facile")

    grille.generer_grille((0,0))
    grille.afficher_grille()
