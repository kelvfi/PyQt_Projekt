# PyQt Projekt
Ich möchte einen Passwort-Manager erstellen, der es in einer Datenbank speichert und auch verschlüsselt dieses Framework ist dazu da,
um die GUI für eine Desktop anwendung zu erstellen.
## Version 1
![Tabelle-Passwort](/doku_img/main_site.png)

Hier sieht man die Startseite dieses Projektes, es ist eine einfache Tabelle, die auf
eine Datenbank zugreift, wo die Passwörter gespeichert sind, die man angelegt hat.

Der **Anlegen-Button** leitet einen weiter zu der Eingabe-Seite wo man Daten eingeben kann die dann in
die Datenbank gespeichert werden. 

Der **Abbrechen-Button** schließt das Programm.

Die Datenbank habe ich in Docker bereitgestellt, es ist eine MySQL Datenbank.

![Passwort-Erstellen](/doku_img/second_site.png)

Hier habe ich ein Fenster erstellt, wo man Daten eingeben kann und somit einen **Benutzer erstellen.**
Mittels Speichern gelangen die eingegebenen Daten in die Daten bank und man erhält eine kleine Notiz wo
enthalten ist, wie viel Datensätze angelegt wurden und ob alles Ordnungsgemäß funktioniert hat. (Diese Notiz ist auf
dem folgenden Bild zu sehen!)

![Eingabe-Data](/doku_img/second_site_data.png)

Mit dem Abbrechen Button kommt man zurück auf die Hauptseite dieses Programmes, dort kann
man nachsehen, ob das Anlegen des neuen Datensatzes auch funktioniert hat.

## Version 2
Hier wurde nochmals die neuere version beschrieben und die neuen Funktionen die ich eingebaut habe.
![main2](/doku_img/main_2.png)
Wie man hier auf diesem Bild sieht habe ich einige neue Buttons und Funktionen eingebaut.

Hier eine Kurze beschreibung zu den Neuen Funktionen:
* **Löschen** = Man muss einen Datensatz anklicken und dann Löschen
* **Anzeigen** = Man kann sich die Passwörter anzeigen lassen
* **Bearbeiten** = Man muss auf einen Datensatz anklicken und dann kann man ihn bearbeiten

![main_anzeige](/doku_img/main_2_anzeige.png)
Hier kann man jetzt ganz gut die Anzeige sehen, die Passwörter werden ganz einfach unmaskiert und angezeigt.

### Delete und Bearbeiten
![main_fehler](/doku_img/main_fehler.png)
Wenn man auf Bearbeiten oder Löschen klickt, kommt so ein fehler das man keinen Datensatz ausgewählt hat.

![main_delete1](/doku_img/delete_main.png)
Hat man nun doch einen Datensatz angeklickt dann funktioniert diese Funktion ganz einfach.

![main_delete2](/doku_img/delete_main2.png)
<br>Hier zeigt es nochmals an das der Datensatz erfolgreich gelöscht wurde.

### Anlegen änderungen
![second_site2](/doku_img/second_site2.png)
Bei dieser Abbildung sieht man einen kleinen Button rechts neben dem Passwort, dieser ist dazu da
um ein Passwort generieren zu lassen.

### Hilfsmittel
Um die Designs zu erstellen, von diesen Fenstern habe ich den **Qt-Designer** verwendet, mit diesem Programm
ist es möglich ganz einfach die Fenster mittels Drag-and-drop zu Designen was den Projektaufwand stark vermindert.

Um eine `.exe` zu erstellen muss man diesen Command eingeben: `python -O -m PyInstaller main.py --onefile --window
`

Hier eine kleine Abbildung wie es in diesem Programm aussieht:
![Qt-Designer](/doku_img/qt_designer.png)


### Tutorials
https://www.youtube.com/watch?v=Os_NKlaj5k4
### Demos 
v1
```
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 200, 300)
    window.setWindowTitle("Simple GUI")

    layout = QVBoxLayout()

    label = QLabel("Press the Button below")
    textBox = QTextEdit()
    button = QPushButton("Press me!")

    button.clicked.connect(lambda: on_clicked(textBox.toPlainText()))

    layout.addWidget(label)
    layout.addWidget(textBox)
    layout.addWidget(button)

    window.setLayout(layout)

    window.show()
    app.exec_()

def on_clicked(msg):
    message = QMessageBox()
    message.setText(msg)
    message.exec_()

# Zum ausführen des Fensters
if __name__ == '__main__':
    main()
```

v2: Einbindung mit Qt Designer und Funktionen
```
from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGUI(QMainWindow):

    def __init__(self):
        # UI Design laden
        super(MyGUI, self).__init__()
        uic.loadUi("myGUI.ui", self)
        self.show()

        # Wenn man einen Button klickt hier Paramenter und Funktionen angeben
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(lambda: self.sayIt(self.textEdit.toPlainText()))
        #self.actionClosed.triggered.connect(exit)

    def sayIt(self, msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec_()

    def login(self):
        if self.lineEdit.text() == "kelvin" and self.lineEdit_2.text() == "1234":
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec_()
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

# Zum ausführen des Fensters
if __name__ == '__main__':
    main()
```