import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("main_site.ui", self)  # Pfad vom Design angeben
        self.show()

        # Funktionen aufrufen
        self.anlegen.clicked.connect(self.anlegen_clicked) # Insert in Datenbank
        self.second_site = None  # Initialisierung von self.second_site WICHTIG!!
        self.third_site = None # Initialisierung
        self.load_all_data_mask() # Alle Daten holen
        self.loeschen_main.clicked.connect(self.delete) # Daten löschen
        self.bearbeiten_main.clicked.connect(self.update) # Daten updaten
        self.pwd_anzeigen.clicked.connect(self.pwd_anzeigen_clicked)
        self.passwort_visible = False

    def update(self):
        selected_row = self.anzeige.currentRow()
        if selected_row == -1: # Wenn keine Zeile angeklickt wurde
            QMessageBox.warning(self, 'Fehler', 'Bitte wählen Sie eine Zeile zum aktualisieren aus.')
            return

        # Daten speichern zum Übergeben
        data = {
            "id": self.anzeige.item(selected_row, 0).text(),
            "webseite": self.anzeige.item(selected_row, 1).text(),
            "url": self.anzeige.item(selected_row, 2).text(),
            "username": self.anzeige.item(selected_row, 3).text(),
            "passwort": self.anzeige.item(selected_row, 4).text()
        }

        # Update Fenster aufrufen
        if self.third_site is None:
            self.third_site = ThirdWindow()  # Verwendung von self
        self.third_site.set_data(data)
        self.third_site.setFixedSize(804, 380)
        self.third_site.show()
        self.close()  # Damit das Hauptfenster schließt, wenn man etwas eingibt

    def delete(self):
        selected_row = self.anzeige.currentRow()
        if selected_row == -1: # Wenn keine Zeile angeklickt wurde
            QMessageBox.warning(self, 'Fehler', 'Bitte wählen Sie eine Zeile zum Löschen aus.')
            return

        # Message Box zum Versichern
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Bestätigung')
        msg_box.setText('Möchten Sie diesen Datensatz wirklich löschen?')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText('Ja')
        msg_box.button(QMessageBox.No).setText('Nein')
        reply = msg_box.exec()

        if reply == QMessageBox.Yes:
            # ID des zu löschenden Datensatzes abrufen
            record_id = self.anzeige.item(selected_row, 0).text()

            # Löschen aus der Datenbank
            connection = DatabaseConnector.connect_to_database()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM nutzerdaten WHERE id = %s", (record_id,))
            connection.commit()
            connection.close()

            # Zeile aus der Tabelle entfernen
            self.anzeige.removeRow(selected_row)
            QMessageBox.information(self, 'Erfolg', 'Datensatz wurde gelöscht.')
        else:
            print("Löschung abgebrochen")

    def anlegen_clicked(self):
        if self.second_site is None:
            self.second_site = SecondWindow()  # Verwendung von self
        self.second_site.setFixedSize(804, 380)
        self.second_site.show()
        self.close()  # Damit das Hauptfenster schließt, wenn man etwas eingibt

    def load_all_data_mask(self):
        # Connection herstellen
        connection = DatabaseConnector.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nutzerdaten")
        rows = cursor.fetchall()

        self.anzeige.setRowCount(len(rows))
        self.real_passwort = []

        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                if col_index == 4:
                    self.real_passwort.append(col_data)
                    col_data = "******" # Maskieren
                self.anzeige.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        connection.close()

    def pwd_anzeigen_clicked(self):
        if self.passwort_visible:
            self.passwort_visible = False
            self.load_all_data_mask()
        else:
            self.passwort_visible = True
            self.load_all_data()

    def load_all_data(self):
        # Connection herstellen
        connection = DatabaseConnector.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nutzerdaten")
        rows = cursor.fetchall()

        self.anzeige.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.anzeige.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        connection.close()


class DatabaseConnector:
    @staticmethod
    def connect_to_database():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="pyqt"
        )
        return connection


class SecondWindow(QWidget):
    def __init__(self):
        super(SecondWindow, self).__init__()
        uic.loadUi("second_site.ui", self)
        self.show()

        # Funktionen
        self.main_site = None  # Initialisierung von self.second_site WICHTIG!!
        self.speichern.clicked.connect(self.speichern_clicked)
        self.abbrechen.clicked.connect(self.abbrechen_clicked)
        self.text_input.hide() # Zum Verstecken der TextBox


    def abbrechen_clicked(self):
        self.close_site()

    def close_site(self):
        if self.main_site is None:
            self.main_site = MyGUI()  # Verwendung von self
        self.main_site.setFixedSize(800, 581)
        self.main_site.show()
        self.close()  # Damit das SecondWindow schließt

    def speichern_clicked(self):
        connection = DatabaseConnector.connect_to_database()
        cursor = connection.cursor()

        # SQL Statement
        sql = "INSERT INTO nutzerdaten (webseite, url, username, passwort) VALUES (%s, %s, %s, %s)"

        # Werte bekommen aus Eingabe
        webseite = self.webseite.text()
        url = self.url.text()
        username = self.username.text()
        passwort = self.passwort.text()

        # Wert vergeben und ausführen
        value = (webseite, url, username, passwort)
        cursor.execute(sql, value)

        # Text anzeigen
        text = f"Es wurde {cursor.rowcount} Datensätz angelegt. \nDer Datensatz wurde erfolgreich angelegt!"
        self.text_input.setText(text)
        self.text_input.show()

        # Abschicken und Speichern
        connection.commit()
        connection.close()

        # Text aus Inputfeldern wieder löschen
        self.webseite.clear()
        self.url.clear()
        self.username.clear()
        self.passwort.clear()

class ThirdWindow(QWidget):
    def __init__(self):
        super(ThirdWindow, self).__init__()
        uic.loadUi("third_site.ui", self)
        self.show()

        self.main_site = None
        self.text_input.hide()  # Zum Verstecken der TextBox
        self.aktuallisieren.clicked.connect(self.update)
        self.abbrechen.clicked.connect(self.abbrechen_clicked)

    def update(self):
        connection = DatabaseConnector.connect_to_database()
        cursor = connection.cursor()

        sql = "UPDATE nutzerdaten SET webseite = %s, url = %s, username = %s, passwort = %s WHERE id = %s"

        # Werte bekommen aus Eingabe
        id = self.id.text()
        webseite = self.webseite.text()
        url = self.url.text()
        username = self.username.text()
        passwort = self.passwort.text()

        # Wert vergeben und ausführen
        value = (webseite, url, username, passwort, id)
        cursor.execute(sql, value)

        # Text anzeigen
        text = f"Datensatz {cursor.rowcount} wurde erfolgreich aktualisiert!"
        self.text_input.setText(text)
        self.text_input.show()

        # Abschicken und Speichern
        connection.commit()
        connection.close()

        # Text aus Inputfeldern wieder löschen
        self.webseite.clear()
        self.url.clear()
        self.username.clear()
        self.passwort.clear()

    def set_data(self, data):
        self.id.setText(data['id'])
        self.webseite.setText(data['webseite'])
        self.url.setText(data['url'])
        self.username.setText(data['username'])
        self.passwort.setText(data['passwort'])

    def abbrechen_clicked(self):
        self.close_site()

    def close_site(self):
        if self.main_site is None:
            self.main_site = MyGUI()  # Verwendung von self
        self.main_site.setFixedSize(800, 581)
        self.main_site.show()
        self.close()  # Damit das ThirdWindow schließt



def main():
    app = QApplication([])
    window = MyGUI()
    window.setFixedSize(800, 581)  # Damit man die Fenstergröße nicht ändern kann
    app.exec_()


# Zum Ausführen des Fensters
if __name__ == '__main__':
    main()
