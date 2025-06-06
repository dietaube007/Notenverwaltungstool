# Login mit bcrypt für sichere Passwortprüfung
import bcrypt
from db import verbinde_db  # Importiert die Funktion zur DB-Verbindung

# Globale Variablen zur Speicherung des eingeloggten Lehrers
lehrer_id = None              # Wird nach erfolgreichem Login mit der Lehrer-ID gefüllt
lehrer_vorname = ""           # Speichert den Vornamen zur Anzeige im Dashboard


# Funktion: login
# Beschreibung:
# Prüft E-Mail und Passwort gegen die Datenbank.
# Bei Erfolg werden die Lehrer-ID und der Vorname global gespeichert.
# Rückgabe: True -> Login erfolgreich, False -> fehlgeschlagen

def login(email, passwort_eingabe):
    global lehrer_id, lehrer_vorname

    # Verbindung zur Datenbank aufbauen
    conn = verbinde_db()
    if not conn:
        return False  # Falls Verbindung fehlschlägt, Login abbrechen

    cur = conn.cursor()

    # SQL-Abfrage: Lehrer mit passender (nicht Groß-/Kleinschreibung-sensitiver) E-Mail finden
    cur.execute(
        "SELECT lehrerID, vorname, passwort FROM lehrer WHERE LOWER(email) = LOWER(?)",
        (email.strip(),)
    )

    result = cur.fetchone()
    conn.close()

    # Wenn ein Lehrer mit dieser E-Mail gefunden wurde
    if result:
        gespeichertes_pw = result[2].encode('utf-8')  # Passwort aus DB in Byte umwandeln
        # Passwortvergleich mit bcrypt
        if bcrypt.checkpw(passwort_eingabe.encode('utf-8'), gespeichertes_pw):
            lehrer_id = result[0]         # speichere Lehrer-ID
            lehrer_vorname = result[1]    # speichere Vorname für Anzeige
            return True                   # Login erfolgreich

    # Falls kein Match oder Passwort falsch: Login fehlgeschlagen
    return False