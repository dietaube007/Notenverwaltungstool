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


    # Funktion zum Einloggen des Lehrers
    def versuche_login():
        email = email_entry.get().strip()
        pw = pw_entry.get().strip()
        if auth.login(email, pw):
            login_win.destroy()
            starte_gui()
        else:
            messagebox.showerror("Login fehlgeschlagen", "❌ E-Mail oder Passwort ist ungültig.")

    # Login-Button
    login_btn = tk.Button(login_win, text="🔐 Login", font=("Segoe UI", 16, "bold"),
                          width=16, command=versuche_login,
                          bg=colors["light"]["highlight"], fg=colors["light"]["highlight_fg"])
    login_btn.pack(pady=40)
    widgets.append(login_btn)

    # Darkmode-Umschalter
    toggle_btn = tk.Button(login_win, textvariable=toggle_text,
                           command=lambda: toggle_darkmode(login_win, widgets, toggle_text),
                           font=("Segoe UI", 12))
    toggle_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
    widgets.append(toggle_btn)

    # Bild anzeigen (z. B. Panda)
    try:
        panda_img = Image.open("panda.png").resize((180, 240), Image.LANCZOS)
        panda_tk = ImageTk.PhotoImage(panda_img)
        panda_label = tk.Label(login_win, image=panda_tk, bg=colors["light"]["panda_bg"])
        panda_label.image = panda_tk
        panda_label.place(x=login_win.winfo_width() - 200, y=login_win.winfo_height() - 260)

        def repositioniere_panda(event=None):
            panda_label.place(x=login_win.winfo_width() - panda_label.winfo_width() - 20,
                              y=login_win.winfo_height() - panda_label.winfo_height() - 20)

        login_win.bind("<Configure>", repositioniere_panda)
        widgets.append(panda_label)
    except Exception as e:
        print("Panda-Bild konnte nicht geladen werden:", e)

    # Theme anwenden und starten
    apply_theme(login_win, widgets)
    login_win.mainloop()


# Haupt-Dashboard starten
def starte_gui():
    global root, tabelle
    root = tk.Tk()
    root.title("🏫 Notenheld – Lehrer Dashboard")
    root.geometry("1400x600")
    root.resizable(True, True)
    widgets = []

    toggle_text = tk.StringVar(value="🌙 Dunkel")

    # Begrüßung
    begruessung = tk.Label(root, text=f"Hallo beim Notenheld {auth.lehrer_vorname} ", font=("Segoe UI", 18, "bold"))
    begruessung.pack(pady=10)
    widgets.append(begruessung)


    # Abmelden-Button
    def abmelden():
        global root
        if messagebox.askyesno("Abmelden", "Willst du dich wirklich abmelden?"):
            root.destroy()
            zeige_login()

    abmelde_btn = tk.Button(root, text="🚪 Abmelden", font=("Segoe UI", 12, "bold"),
                            command=abmelden, bg=colors["light"]["abmelden"], fg=colors["light"]["abmelden_fg"])
    abmelde_btn.pack(pady=5)
    widgets.append(abmelde_btn)


    # Funktionsbuttons
    frame = tk.Frame(root)
    frame.pack(pady=10)
    widgets.append(frame)

    tk.Button(frame, text="➕ Note hinzufügen", font=("Segoe UI", 12, "bold"),
              command=lambda: noten_hinzufuegen_dialog(root, aktualisiere_tabelle, apply_theme),
              bg=colors["light"]["btn"], fg=colors["light"]["btn_fg"]).pack(side=tk.LEFT, padx=10)

    tk.Button(frame, text="✏️ Note bearbeiten", font=("Segoe UI", 12, "bold"),
              command=lambda: note_bearbeiten(tabelle, root, aktualisiere_tabelle, apply_theme),
              bg=colors["light"]["btn"], fg=colors["light"]["btn_fg"]).pack(side=tk.LEFT, padx=10)

    tk.Button(frame, text="🗑️ Note löschen", font=("Segoe UI", 12, "bold"),
              command=loesche_note,
              bg=colors["light"]["btn"], fg=colors["light"]["btn_fg"]).pack(side=tk.LEFT, padx=10)

    tk.Button(frame, text="📤 Exportieren", font=("Segoe UI", 12, "bold"),
              command=noten_exportieren,
              bg=colors["light"]["btn"], fg=colors["light"]["btn_fg"]).pack(side=tk.LEFT, padx=10)

    # Darkmode-Toggle auch im Dashboard
    toggle_btn = tk.Button(frame, textvariable=toggle_text,
                           command=lambda: toggle_darkmode(root, widgets, toggle_text),
                           font=("Segoe UI", 12))
    toggle_btn.pack(side=tk.RIGHT, padx=10)
    widgets.append(toggle_btn)


   # Noten-Tabelle
    spalten = ("Schüler", "Geschlecht", "Ort", "Postleitzahl", "Klasse", "Eintrittsjahr",
               "Fach", "Note", "Notenart", "Datum", "Lehrer", "Status")
    tabelle = ttk.Treeview(root, columns=spalten, show="headings")
    for spalte in spalten:
        tabelle.heading(spalte, text=spalte)
        tabelle.column(spalte, anchor="center", width=120)
    tabelle.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    widgets.append(tabelle)

    # Scrollbar
    scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tabelle.xview)
    tabelle.configure(xscrollcommand=scrollbar.set)
    scrollbar.pack(fill="x", side="bottom")

    # Panda-Bild im Dashboard
    try:
        panda_img = Image.open("panda.png").resize((180, 240), Image.LANCZOS)
        panda_tk = ImageTk.PhotoImage(panda_img)
        panda_label = tk.Label(root, image=panda_tk, bg=colors["light"]["panda_bg"])
        panda_label.image = panda_tk
        panda_label.place(x=0, y=0)

        def repositioniere_panda(event=None):
            w = root.winfo_width()
            h = root.winfo_height()
            panda_label.place(x=w - panda_label.winfo_width() - 20,
                              y=h - panda_label.winfo_height() - 20)

        root.bind("<Configure>", repositioniere_panda)
        widgets.append(panda_label)
    except Exception as e:
        print("Panda-Bild konnte nicht geladen werden:", e)

    apply_theme(root, widgets)
    aktualisiere_tabelle()
    root.mainloop()

