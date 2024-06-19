import sqlite3


class DatabaseConnector:

    def __init__(self):
        None

    @staticmethod
    def connect_to_database():
        connection = sqlite3.connect('pyqt.db')
        return connection
    @staticmethod
    def create_table():
        connection = DatabaseConnector.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS nutzerdaten (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    webseite TEXT NOT NULL,
                    url TEXT NOT NULL,
                    username TEXT NOT NULL,
                    passwort TEXT NOT NULL
                )
            ''')
        connection.commit()
        connection.close()
