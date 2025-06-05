# Importieren der notwendigen Bibliotheken
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import verbinde_db
from daten_laden import lade_notentypen, lade_notenwerte, lade_noten
from datetime import datetime, date
from theme import apply_theme

# Funktion zum Bearbeiten einer bestehenden Note aus der Tabelle
def note_bearbeiten(tabelle, root, aktualisiere_tabelle, apply_theme):
    # Sicherstellen, dass eine Zeile ausgewählt ist
    ausgewaehlt = tabelle.selection()
    if not ausgewaehlt:
        messagebox.showwarning("Keine Auswahl", "Bitte eine Note auswählen.")
        return

    # Alle Werte der ausgewählten Zeile holen
    daten = tabelle.item(ausgewaehlt)["values"]

    # Lade alle Noten erneut, um auf die Originaldaten mit IDs zugreifen zu können
    noten_liste = lade_noten()
    index = tabelle.index(ausgewaehlt[0])
    original = noten_liste[index]  # enthält IDs für UPDATE

    # Einzelne Felder extrahieren
    schueler_name = daten[0]
    fach_name = daten[6]
    notentyp_name = daten[8]
    datum_alt = daten[9]
    notenwert_alt = daten[7]

    # Lade Notentypen und Notenwerte zur Auswahl
    typ_map = {name: tid for tid, name in lade_notentypen()}
    wert_map = {str(wert): wid for wid, wert in lade_notenwerte()}

    # Neues Fenster zum Bearbeiten erstellen
    win = tk.Toplevel(root)
    win.title("✏️ Note bearbeiten")
    win.geometry("500x400")
    widgets = []

    # Schüler- und Fachanzeige (nicht änderbar)
    tk.Label(win, text=f"Schüler: {schueler_name}", font=("Segoe UI", 12)).pack(pady=5)
    tk.Label(win, text=f"Fach: {fach_name}", font=("Segoe UI", 12)).pack(pady=5)

    # Notentyp-Dropdown
    frame1 = tk.Frame(win)
    frame1.pack(pady=5)
    tk.Label(frame1, text="Notentyp:", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=5)
    typ_var = tk.StringVar(value=notentyp_name)
    typ_combo = ttk.Combobox(
        frame1, textvariable=typ_var,
        values=list(typ_map.keys()),
        font=("Segoe UI", 12),
        state="readonly", style="Custom.TCombobox"
    )
    typ_combo.pack(side=tk.LEFT)
    widgets.extend([frame1, typ_combo])

    # Notenwert-Dropdown (1 bis 6)
    frame2 = tk.Frame(win)
    frame2.pack(pady=5)
    tk.Label(frame2, text="Note (1–6):", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=5)
    wert_var = tk.StringVar(value=str(notenwert_alt))
    wert_combo = ttk.Combobox(
        frame2, textvariable=wert_var,
        values=list(wert_map.keys()),
        font=("Segoe UI", 12),
        state="readonly", style="Custom.TCombobox"
    )
    wert_combo.pack(side=tk.LEFT)
    widgets.extend([frame2, wert_combo])

    # Datumsauswahl
    frame3 = tk.Frame(win)
    frame3.pack(pady=5)
    tk.Label(frame3, text="Datum:", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=5)

    datum_entry = DateEntry(
        frame3,
        font=("Segoe UI", 12),
        date_pattern="dd.mm.yyyy",
        state="readonly",
        style="Custom.DateEntry",
        maxdate=date.today()  # Keine Zukunftsdaten erlaubt
    )

    # Sicherstellen, dass das Datum korrekt geparst wird (z. B. von '2025-06-04' zu datetime.date)
    try:
        datum_alt_obj = datetime.strptime(str(datum_alt), "%Y-%m-%d").date()
        datum_entry.set_date(datum_alt_obj)
    except Exception:
        messagebox.showerror("Fehler", f"Ungültiges Datum: {datum_alt}")
        win.destroy()
        return

    datum_entry.pack(side=tk.LEFT)
    widgets.extend([frame3, datum_entry])
