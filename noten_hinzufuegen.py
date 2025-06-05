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

# Dialogfenster zum Hinzufügen einer neuen Note
def noten_hinzufuegen_dialog(root, aktualisiere_tabelle, apply_theme):
    win = tk.Toplevel(root)
    win.title("➕ Neue Note eintragen")
    win.geometry("500x500")
    widgets = []

    # Klassen des Lehrers abrufen
    klassen_raw = get_klassen_fuer_lehrer()
    if not klassen_raw:
        messagebox.showwarning("Keine Klassen", "Für diesen Lehrer sind keine Klassen zugewiesen.")
        win.destroy()
        return

    # Initialisierung der benötigten Variablen und Mappings
    klassen_map = {name: kid for name, kid in klassen_raw}
    vars = {"klasse": tk.StringVar(), "schueler": tk.StringVar(), "fach": tk.StringVar(),
            "notentyp": tk.StringVar(), "notenwert": tk.StringVar()}
    schueler_map, fach_map = {}, {}
    typ_map = {name: tid for tid, name in lade_notentypen()}
    wert_map = {str(wert): wid for wid, wert in lade_notenwerte()}

    # Funktion zur Erstellung eines Feldes mit Label und Combobox
    def feld(lbl, var, values, row):
        label = tk.Label(win, text=lbl, font=("Segoe UI", 12))
        combo = ttk.Combobox(win, textvariable=var, values=values,
                             font=("Segoe UI", 12), width=30, state="readonly",
                             style="Custom.TCombobox")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        combo.grid(row=row, column=1, pady=5)
        widgets.extend([label, combo])
        return combo

    # Erzeugen der Formularfelder
    klasse_combo = feld("Klasse:", vars["klasse"], list(klassen_map.keys()), 0)
    schueler_combo = feld("Schüler:", vars["schueler"], [], 1)
    fach_combo = feld("Fach:", vars["fach"], [], 2)
    feld("Notenart:", vars["notentyp"], list(typ_map.keys()), 3)
    feld("Note (1–6):", vars["notenwert"], list(wert_map.keys()), 4)

    # Datumsauswahlfeld mit Einschränkung auf heutiges oder vergangenes Datum
    datum_label = tk.Label(win, text="Datum:", font=("Segoe UI", 12))
    datum_entry = DateEntry(
        win,
        font=("Segoe UI", 12),
        date_pattern="yyyy-mm-dd",
        state="readonly",
        style="Custom.DateEntry",
        maxdate=datetime.date.today()
    )
    datum_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    datum_entry.grid(row=5, column=1, pady=5)
    widgets.extend([datum_label, datum_entry])

    # Wenn sich die Klasse ändert, lade passende Schüler und Fächer
    def on_klasse_change(*args):
        klasse = vars["klasse"].get()
        if klasse not in klassen_map:
            return
        k_id = klassen_map[klasse]
        vars["schueler"].set("")
        vars["fach"].set("")
        schueler_combo["values"] = []
        fach_combo["values"] = []

        s_data = get_schueler_fuer_klasse(k_id)
        schueler_map.clear()
        schueler_map.update({f"{name}": sid for sid, name in s_data})
        schueler_combo.config(values=list(schueler_map.keys()))

        f_data = get_faecher_fuer_lehrer_und_klasse(k_id)
        fach_map.clear()
        fach_map.update({name: fid for name, fid in f_data})
        fach_combo.config(values=list(fach_map.keys()))

    vars["klasse"].trace_add("write", on_klasse_change)

    # Funktion zum Speichern des Eintrags
    def speichern():
        sid = schueler_map.get(vars["schueler"].get())
        fid = fach_map.get(vars["fach"].get())
        tid = typ_map.get(vars["notentyp"].get())
        nwid = wert_map.get(vars["notenwert"].get())
        datum = datum_entry.get()

        # Überprüfung, ob alle Felder korrekt ausgefüllt wurden
        if not all([sid, fid, tid, nwid, datum]):
            messagebox.showerror("Fehler", "Alle Felder korrekt ausfüllen.")
            return

        # Note speichern
        note_hinzufuegen(sid, fid, tid, datum, nwid)
        aktualisiere_tabelle()
        win.destroy()

    speichern_btn = tk.Button(win, text="💾 Speichern", command=speichern,
                               font=("Segoe UI", 12, "bold"),
                               bg="#81d4fa", fg="black")
    speichern_btn.grid(row=6, column=0, columnspan=2, pady=20)
    widgets.append(speichern_btn)

    # Wendet das aktuelle Design auf alle Widgets im Fenster an
    apply_theme(win, widgets)
