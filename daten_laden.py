# Importiert die Funktion zur Datenbankverbindung
from db import verbinde_db
import auth  # Für Zugriff auf die eingeloggte Lehrer-ID


# Funktion: lade_noten
# Beschreibung:
# Lädt alle Noteneinträge eines Lehrers aus der Datenbank,
# inklusive Schülername, Geschlecht, Ort, PLZ, Klasse, Eintrittsjahr,
# Fach, Note, Notenart, Datum, Lehrername und benötigter IDs.
# Rückgabe: Liste mit Noten-Datensätzen

def lade_noten():
    conn = verbinde_db()
    cur = conn.cursor()

    # SQL-Abfrage mit mehreren Joins, um alle relevanten Informationen zu kombinieren
    cur.execute("""
    SELECT 
        CONCAT(s.vorname, ' ', s.nachname) AS schuelername,  -- Vollständiger Schülername
        g.art AS geschlecht,                                  -- z.B. männlich, weiblich, divers
        o.ort AS ort,                                         -- Wohnort
        o.postleitzahl,                                       -- Postleitzahl des Schülers
        k.klasse,                                             -- Klassenbezeichnung
        ej.eintrittsjahr,                                     -- Jahr, in dem der Schüler gestartet ist
        f.fachname,                                           -- Fach (z.B. Mathe)
        nw.Note AS notenwert,                                 -- Zahlennote (z.B. 1–6)
        nt.notentyp AS notenart,                              -- Art der Note (z.B. Test, Mitarbeit)
        n.datum,                                              -- Datum der Noteneingabe
        CONCAT(l.vorname, ' ', l.nachname) AS lehrername,     -- Name des Lehrers
        nw.Note,                                              -- Note nochmal für technische Zwecke (z.B. zur Auswertung)
        s.schuelerID, f.fachID, nt.notentypID, n.datum        -- Primärschlüssel für spätere Identifizierung beim Bearbeiten/Löschen
    FROM noten n
    JOIN schueler s ON n.schuelerID = s.schuelerID
    JOIN geschlecht g ON s.geschlechtID = g.geschlechtID
    JOIN ort o ON s.ortID = o.ortID
    JOIN klasse k ON s.klassenID = k.klassenID
    JOIN eintrittsjahr ej ON s.eintrittsjahrID = ej.eintrittsjahrID
    JOIN fach f ON n.fachID = f.fachID
    JOIN lehrer l ON n.lehrerID = l.lehrerID
    JOIN notentyp nt ON n.notentypID = nt.notentypID
    JOIN noten_wert nw ON n.noten_wertID = nw.noten_wertID
    WHERE n.lehrerID = ?
    ORDER BY n.datum DESC
""", (auth.lehrer_id,))

    daten = cur.fetchall()  # Alle Datensätze abrufen
    conn.close()
    return daten



# Funktion: lade_schueler
# Beschreibung:
# Lädt alle Schülernamen mit ihren IDs

def lade_schueler():
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("SELECT schuelerID, CONCAT(vorname, ' ', nachname) FROM schueler")
    return cur.fetchall()


# Funktion: lade_faecher
# Beschreibung:
# Gibt alle Fächer mit IDs zurück (z.B. Mathe, Englisch)

def lade_faecher():
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("SELECT fachID, fachname FROM fach")
    return cur.fetchall()


# Funktion: lade_notentypen
# Beschreibung:
# Gibt die verfügbaren Notentypen zurück (z.B. Test, Klausur)

def lade_notentypen():
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("SELECT notentypID, notentyp FROM notentyp")
    return cur.fetchall()


# Funktion: lade_notenwerte
# Beschreibung:
# Gibt die möglichen Notenwerte (1–6) zurück

def lade_notenwerte():
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("SELECT noten_wertID, Note FROM noten_wert")
    return cur.fetchall()
