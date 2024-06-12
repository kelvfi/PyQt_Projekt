# PyQt Projekt
Ich möchte ein Passwort-Manager erstellen der es in einer Datenbank speichert und auch verschlüsselt dieses Framework ist dazu da
um die GUI für eine Desktop anwendung zu erstellen.

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