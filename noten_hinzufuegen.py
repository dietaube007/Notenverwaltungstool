# Importieren der notwendigen Module
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import verbinde_db
from daten_laden import lade_notentypen, lade_notenwerte
import auth
import datetime
import mariadb
from theme import apply_theme

# Funktion zum Abrufen aller Klassen, die einem Lehrer zugeordnet sind
def get_klassen_fuer_lehrer():
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT k.klasse, k.klassenID 
        FROM unterricht u 
        JOIN klasse k ON u.klassenID = k.klassenID 
        WHERE u.lehrerID = ?
    """, (auth.lehrer_id,))
    return cur.fetchall()

# Funktion zum Abrufen aller Schüler einer bestimmten Klasse
def get_schueler_fuer_klasse(klassen_id):
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT schuelerID, CONCAT(vorname, ' ', nachname) 
        FROM schueler 
        WHERE klassenID = ?
    """, (klassen_id,))
    return cur.fetchall()

# Funktion zum Abrufen aller Fächer, die ein Lehrer in einer Klasse unterrichtet
def get_faecher_fuer_lehrer_und_klasse(klassen_id):
    conn = verbinde_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT f.fachname, f.fachID
        FROM unterricht u
        JOIN fach f ON u.fachID = f.fachID
        WHERE u.lehrerID = ? AND u.klassenID = ?
    """, (auth.lehrer_id, klassen_id))
    return cur.fetchall()

# Funktion zum Einfügen einer neuen Note in die Datenbank
def note_hinzufuegen(sid, fid, tid, datum, nwid):
    conn = verbinde_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO noten (schuelerID, lehrerID, fachID, notentypID, datum, noten_wertID)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sid, auth.lehrer_id, fid, tid, datum, nwid))
        conn.commit()
    except mariadb.IntegrityError:
        # Falls es bereits eine Note für dieses Datum gibt
        conn.rollback()
        messagebox.showerror("Fehler", "Eintrag existiert bereits für dieses Datum.")
    except Exception as e:
        # Allgemeiner Fehler beim Speichern
        conn.rollback()
        messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{e}")
    finally:
        conn.close()

