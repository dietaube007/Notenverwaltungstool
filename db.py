# Funktion: Verbindung zur MariaDB-Datenbank herstellen
# Import des MariaDB-Treibers
import mariadb

# Für Fehlermeldungen im GUI-Fenster
from tkinter import messagebox


# Funktion: verbinde_db()
# Beschreibung:
# Stellt eine Verbindung zur lokalen MariaDB-Datenbank her.
# Rückgabe: Eine geöffnete Verbindung oder None im Fehlerfall

def verbinde_db():
    try:
        # Verbindung zur Datenbank herstellen mit Benutzername, Host und Datenbanknamen
        return mariadb.connect(
            user="team06",          # Team-User
            password="GCFWT",       # Passwort
            host="10.80.0.206",     # Lokaler Datenbankserver der Schule
            port=3306,              # Standardport für MariaDB
            database="team06"       # Name der Datenbank
        )
    except mariadb.Error as e:
        # Zeigt bei Fehler eine Meldung im GUI an
        messagebox.showerror("Fehler", f"Datenbankverbindung fehlgeschlagen:\n{e}")
        return None  # Gibt None zurück, wenn Verbindung fehlschlägt
