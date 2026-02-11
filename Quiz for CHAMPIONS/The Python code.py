import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,QFileDialog, QMessageBox, QVBoxLayout, QWidget)

class BureauFileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Classer les fichiers du Bureau")
        self.setGeometry(200, 200, 400, 120)

        layout = QVBoxLayout()

        self.button = QPushButton("Sélectionner des fichiers à classer depuis le Bureau")
        self.button.clicked.connect(self.classer_fichiers)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def classer_fichiers(self):
        bureau_path = os.path.expanduser('~/Desktop')

        fichiers, _ = QFileDialog.getOpenFileNames(
            self,
            "Choisir des fichiers à classer",
            bureau_path
        )

        if fichiers:
            categories = {
                'Documents': ['.pdf', '.docx', '.txt'],
                'Images': ['.jpg', '.jpeg', '.png', '.gif'],
                'Vidéos': ['.mp4', '.avi', '.mkv'],
                'Archives': ['.zip', '.rar', '.7z'],
                'Autres': [] }

            for chemin in fichiers:
                nom = os.path.basename(chemin)
                _, extension = os.path.splitext(nom)
                extension = extension.lower()

                dossier_cible = None
                for nom_cat, extensions in categories.items():
                    if extension in extensions:
                        dossier_cible = os.path.join(bureau_path, nom_cat)
                        break

                if not dossier_cible:
                    dossier_cible = os.path.join(bureau_path, 'Autres')

                os.makedirs(dossier_cible, exist_ok=True)

                try:
                    shutil.move(chemin, os.path.join(dossier_cible, nom))
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur pour {nom} : {e}")
                    return

            QMessageBox.information(self, "✅ Terminé", "Tous les fichiers ont été classés avec succès.")

def main():
    app = QApplication(sys.argv)
    fenetre = BureauFileOrganizer()
    fenetre.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()