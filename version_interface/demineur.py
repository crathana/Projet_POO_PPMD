import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from classes import Grille, Case_bombe, Case_safe


class DemineurGUI(QWidget):
    def __init__(self, difficulte="Facile"):
        super().__init__()

        self.grille = Grille(difficulte)
        self.premier_clic = True

        self.setWindowTitle(f"Démineur — {difficulte}")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.boutons = []
        self.creer_grille(difficulte)
        self.difficulte = difficulte

    def creer_grille(self,difficulte):
        """ Génère la grille en mettant en place une alternance de couleurs"""
        couleurs = ["#EEEED2", "#555A6A"]

        for i in range(self.grille.taille[0]):
            ligne = []
            for j in range(self.grille.taille[1]):
                bouton = QPushButton(" ")
                if difficulte == "Facile":
                    bouton.setFixedSize(50, 50)
                if difficulte == "Moyen":
                    bouton.setFixedSize(40, 40)
                if difficulte =="Difficile":
                    bouton.setFixedSize(30, 30)
                couleur = couleurs[(i + j) % 2]
                bouton.setStyleSheet(f"background-color: {couleur}; font-size: 20px; border: none;")
                bouton.mousePressEvent = lambda e, x=i, y=j: self.clic_case(e, x, y)
                self.layout.addWidget(bouton, i, j)
                ligne.append(bouton)
            self.boutons.append(ligne)

    def clic_case(self, event, x, y):
        """ Gère l'action du clic sur une case, en adaptant si c'est le premier clic ou non """
        if self.premier_clic:
            self.grille.generer_grille((x, y))
            self.premier_clic = False

        if event.button() == Qt.LeftButton:
            self.action_reveler(x, y)
        elif event.button() == Qt.RightButton:
            self.action_drapeau(x, y)

        self.mettre_a_jour_affichage()

        # Vérifier fin
        self.grille.test_grille_finie()
        if self.grille.etat_grille != 0:
            self.fin_partie()

    def action_reveler(self, x, y):
        """ Révèle la case de coordonnées (x,y)"""
        self.grille.reveler(x, y)

    def action_drapeau(self, x, y):
        """ Ajoute ou enleve un drapeau """
        case = self.grille.grille[x][y]
        if case.etat_case == 0:
            self.grille.cocher(x, y)
        elif case.etat_case == -1:
            self.grille.decocher_case(x, y)

    def mettre_a_jour_affichage(self):
        """ Mets à jour l'affichage des cases """
        for i in range(self.grille.taille[0]):
            for j in range(self.grille.taille[1]):
                bouton = self.boutons[i][j]
                case = self.grille.grille[i][j]

                bouton.setIcon(QIcon())
                bouton.setText(" ")

                if case.etat_case == 0:
                    bouton.setEnabled(True)

                elif case.etat_case == -1:
                    bouton.setEnabled(True)
                    bouton.setIcon(QIcon(case.affichage))
                    if self.difficulte == "Facile":
                        bouton.setIconSize(QSize(40, 40))
                    if self.difficulte == "Moyen":
                        bouton.setIconSize(QSize(30, 30))
                    if self.difficulte == "Difficile":
                        bouton.setIconSize(QSize(20, 20))

                elif case.etat_case == 1:
                    bouton.setEnabled(False)
                    couleur_fond = "#FFFFFF"
                    bouton.setStyleSheet(f"""
                        background-color: {couleur_fond};
                        font-size: 20px;
                        border: none;
                    """)

                    if isinstance(case, Case_bombe):
                        bouton.setIcon(QIcon(case.affichage))
                        if self.difficulte == "Facile":
                            bouton.setIconSize(QSize(40, 40))
                        if self.difficulte == "Moyen":
                            bouton.setIconSize(QSize(30, 30))
                        if self.difficulte == "Difficile":
                            bouton.setIconSize(QSize(20, 20))
                    elif isinstance(case, Case_safe):
                        bouton.setText(str(case.nb_voisins) if case.nb_voisins > 0 else "")

    def fin_partie(self):
        self.mettre_a_jour_affichage()
        msg = QMessageBox()
        msg.setWindowTitle("Fin de partie")
        msg.setText(self.grille.fin_partie())
        msg.exec_()

        for ligne in self.boutons:
            for bouton in ligne:
                bouton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    niveaux = ["Facile", "Moyen", "Difficile"]
    difficulte, ok = QInputDialog.getItem(
        None, "Choisir la difficulté", "Niveau :", niveaux, 0, False
    )

    if ok and difficulte:
        gui = DemineurGUI(difficulte)
        gui.show()
        sys.exit(app.exec_())