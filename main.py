import sys
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("main_site.ui", self) # Pfad vom Design angeben
        self.show()


        self.anlegen.clicked.connect(self.anlegen_clicked)
        self.second_site = None  # Initialisierung von self.second_site WICHTIG!!
        self.load_all_data()

    def anlegen_clicked(self):
        if self.second_site is None:
            self.second_site = SecondWindow()  # Verwendung von self
        self.second_site.show()
        self.close() # Damit das Hauptfenster schließt wenn man etwas eingibt

    @staticmethod
    def connect_to_database():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="pyqt"
        )
        return connection

    def load_all_data(self):
        # Connection herstellen
        connection = self.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nutzerdaten")
        rows = cursor.fetchall()

        self.anzeige.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.anzeige.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        connection.close()

class SecondWindow(QWidget):
    def __init__(self):
        super(SecondWindow, self).__init__()
        uic.loadUi("second_site.ui", self)
        self.show()

def main():
    app = QApplication([])
    window = MyGUI()
    window.setFixedSize(800, 581) # Damit man die Fenstergröße nicht ändern kann
    app.exec_()

# Zum Ausführen des Fensters
if __name__ == '__main__':
    main()
