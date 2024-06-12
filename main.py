import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGUI(QMainWindow):

    def __init__(self):
        # UI Design laden
        super(MyGUI, self).__init__()
        uic.loadUi("anzeige.ui", self) # Pfad vom Design angeben
        self.show()
def main():
    app = QApplication([])
    window = MyGUI()
    window.setFixedSize(711, 581) # Damit man die Fenstergröße nicht ändern kann
    app.exec_()

# Zum ausführen des Fensters
if __name__ == '__main__':
    main()