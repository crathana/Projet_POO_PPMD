from classes import Grille

def demander_action():
    while True:
        action = input("Action (r = révéler, f = drapeau) : ").lower()
        if action in ("r", "f"):
            return action
        print("Action invalide. Tapez 'r' ou 'f'.")

def demander_coordonnees(max_lignes, max_colonnes):
    while True:
        try:
            x = int(input(f"Ligne (0 à {max_lignes-1}) : "))
            y = int(input(f"Colonne (0 à {max_colonnes-1}) : "))
            if 0 <= x < max_lignes and 0 <= y < max_colonnes:
                return x, y
            print("Coordonnées hors limites !")
        except ValueError:
            print("Veuillez entrer des nombres entiers valides.")

def demander_difficultee():
    while True:
        action = input("Difficulté ? (f = facile, m = moyen, d = difficile) : ").lower()
        if action in ("f", "m", "d"):
            return action
        print("Action invalide. Tapez 'f', 'm' ou 'd'.")


def jouer():
    difficulte = demander_difficultee()
    if difficulte == "f":
        grille = Grille("Facile")
    elif difficulte == "m":
        grille = Grille("Moyen")
    if difficulte == "d":
        grille = Grille("Difficile")

    print("Grille initiale (fictive) :")
    grille.afficher_grille()

    print("\nPremier clic (la grille sera générée à partir de cette case)")
    x, y = demander_coordonnees(grille.taille[0], grille.taille[1])
    grille.generer_grille((x, y))
    grille.reveler(x, y)

    while grille.etat_grille == 0:
        print("\nGrille actuelle :")
        grille.afficher_grille()

        action = demander_action()
        x, y = demander_coordonnees(grille.taille[0], grille.taille[1])

        if action == "r":
            grille.reveler(x, y)
        elif action == "f":
            if grille.grille[x][y].etat_case == 0:
                grille.cocher(x, y)
            elif grille.grille[x][y].etat_case == -1:
                grille.decocher_case(x, y)

        # Vérifier si toutes les cases safe ont été révélées
        grille.test_grille_finie()

    # Fin de partie
    print("\nGrille finale :")
    grille.afficher_grille()
    print(grille.fin_partie())

if __name__ == "__main__":
    jouer()