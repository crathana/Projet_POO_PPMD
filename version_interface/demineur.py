import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
from classes import Grille, Case_bombe, Case_safe


class DemineurGUI(QWidget):
    def __init__(self, difficulte="Facile"):
        super().__init__()

        # Moteur du jeu
        self.grille = Grille(difficulte)

        self.premier_clic = True

        # UI
        self.setWindowTitle("Démineur")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.boutons = []
        self.creer_grille()

    def creer_grille(self):
        """Crée les boutons graphiques"""
        for i in range(self.grille.taille[0]):
            ligne = []
            for j in range(self.grille.taille[1]):
                bouton = QPushButton(" ")
                bouton.setFixedSize(35, 35)
                bouton.setStyleSheet("font-size: 16px;")
                bouton.mousePressEvent = lambda e, x=i, y=j: self.clic_case(e, x, y)
                self.layout.addWidget(bouton, i, j)
                ligne.append(bouton)
            self.boutons.append(ligne)

    def clic_case(self, event, x, y):
        """Gestion clic gauche / droit"""

        # PREMIER CLIC → on génère la grille
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
        self.grille.reveler(x, y)

    def action_drapeau(self, x, y):
        case = self.grille.grille[x][y]
        if case.etat_case == 0:
            self.grille.cocher(x, y)
        elif case.etat_case == -1:
            self.grille.decocher_case(x, y)

    def mettre_a_jour_affichage(self):
        """Affiche dans l’UI ce que ton moteur a décidé"""
        for i in range(self.grille.taille[0]):
            for j in range(self.grille.taille[1]):
                bouton = self.boutons[i][j]
                case = self.grille.grille[i][j]

                if case.etat_case == 0:
                    bouton.setText(" ")
                    bouton.setEnabled(True)

                elif case.etat_case == -1:
                    bouton.setText("🚩")
                    bouton.setEnabled(True)

                elif case.etat_case == 1:
                    bouton.setEnabled(False)

                    if isinstance(case, Case_bombe):
                        bouton.setText("💣")
                    elif isinstance(case, Case_safe):
                        bouton.setText(str(case.nb_voisins) if case.nb_voisins > 0 else "")

    def fin_partie(self):
        """Révèle tout + popup"""
        self.mettre_a_jour_affichage()
        msg = QMessageBox()
        msg.setWindowTitle("Fin de partie")
        msg.setText(self.grille.fin_partie())
        msg.exec_()

        # Bloquer la grille après fin
        for ligne in self.boutons:
            for bouton in ligne:
                bouton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DemineurGUI("Facile")
    gui.show()
    sys.exit(app.exec_())