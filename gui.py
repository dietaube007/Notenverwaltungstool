# Funktion: Zentrale GUI für Notenverwaltung

# Benötigte Bibliotheken importieren
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import auth
from db import verbinde_db
from daten_laden import lade_noten
from noten_hinzufuegen import noten_hinzufuegen_dialog
from noten_bearbeiten import note_bearbeiten
from noten_export import noten_exportieren
from theme import toggle_darkmode, apply_theme, colors


# Globale Variablen
root = None          # Hauptfenster
tabelle = None       # Treeview für Notenanzeige
is_darkmode = False  # Status Darkmode


# Login-Fenster anzeigen
def zeige_login():
    global is_darkmode
    login_win = tk.Tk()
    login_win.title("🏫 Notenheld – Login")
    login_win.geometry("1400x600")
    widgets = []

    # Umschalter-Text für Darkmode
    toggle_text = tk.StringVar(value="🌙 Dunkel")

    # Überschrift
    title = tk.Label(login_win, text="Willkommen beim Notenheld", font=("Segoe UI", 28, "bold"))
    title.pack(pady=40)
    widgets.append(title)

    # Rahmen für Eingabefelder
    frame = tk.Frame(login_win)
    frame.pack()
    widgets.append(frame)

    # Eingabe E-Mail
    l1 = tk.Label(frame, text="E-Mail:", font=("Segoe UI", 16))
    l1.grid(row=0, column=0, padx=20, pady=15, sticky="e")
    email_entry = tk.Entry(frame, font=("Segoe UI", 16), width=32)
    email_entry.grid(row=0, column=1)
    widgets.extend([l1, email_entry])

    # Eingabe Passwort
    l2 = tk.Label(frame, text="Passwort:", font=("Segoe UI", 16))
    l2.grid(row=1, column=0, padx=20, pady=15, sticky="e")
    pw_entry = tk.Entry(frame, show="*", font=("Segoe UI", 16), width=32)
    pw_entry.grid(row=1, column=1)
    widgets.extend([l2, pw_entry])


    