import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

# Globale Steuerung, ob der Darkmode aktiv ist
is_darkmode = False

# Farbdefinitionen für Lightmode und Darkmode
colors = {
    "light": {
        "bg": "#fce4ec",           # Fensterhintergrund in hellrosa
        "fg": "black",             # Standardtextfarbe
        "btn": "#81d4fa",          # Hintergrundfarbe der Buttons (hellblau)
        "btn_fg": "black",         # Schriftfarbe der Buttons
        "entry_bg": "#ffffff",     # Hintergrund von Eingabefeldern
        "entry_fg": "black",       # Textfarbe in Eingabefeldern
        "tree": "#ffffff",         # Hintergrundfarbe für Tabellenzeilen
        "tree_fg": "black",        # Schriftfarbe für Tabelleninhalt
        "highlight": "#81d4fa",    # Farbe bei Auswahl (z. B. ausgewählte Zeile)
        "highlight_fg": "black",   # Textfarbe der ausgewählten Zeile
        "abmelden": "#c62828",     # Roter Button für Abmelden
        "abmelden_fg": "white",
        "status": {                # Farben für Statusmarkierung
            "gruen": "#d0f0c0",
            "gelb": "#fff8b0",
            "rot": "#ffc0c0"
        },
        "panda_bg": "#fce4ec"      # Hintergrund für Panda-Bild
    },
    "dark": {
        "bg": "#2c2c2c",           # Fensterhintergrund dunkelgrau
        "fg": "white",
        "btn": "#607d8b",          # Dunklerer Buttonhintergrund
        "btn_fg": "white",
        "entry_bg": "#424242",
        "entry_fg": "white",
        "tree": "#424242",
        "tree_fg": "white",
        "highlight": "#607d8b",
        "highlight_fg": "white",
        "abmelden": "#8B0000",     # Dunkelrot für Abmeldebutton
        "abmelden_fg": "white",
        "status": {
            "gruen": "#33691e",
            "gelb": "#fbc02d",
            "rot": "#c62828"
        },
        "panda_bg": "#2c2c2c"
    }
}


# Funktion: apply_theme
# Beschreibung:
# Wendet das gewählte Farbschema (hell/dunkel) auf das Fenster
# und alle enthaltenen Widgets an

def apply_theme(window, widgets):
    theme = colors["dark"] if is_darkmode else colors["light"]

    # Fensterhintergrund setzen
    window.configure(bg=theme["bg"])

    # Stile für ttk-Widgets setzen
    style = ttk.Style()
    style.theme_use('clam')  # Kompatibles Theme für Tkinter

    # Tabelle (Treeview) – normale Zeilen
    style.configure("Treeview",
        font=("Segoe UI", 11),
        rowheight=25,
        background=theme["tree"],
        foreground=theme["tree_fg"],
        fieldbackground=theme["tree"]
    )

    # Tabelle – hervorgehobene Zeile bei Auswahl
    style.map("Treeview", background=[("selected", theme["highlight"])])

    # Tabellenüberschriften
    style.configure("Treeview.Heading",
        background=theme["btn"],
        foreground=theme["btn_fg"],
        font=("Segoe UI", 11, "bold")
    )

    # Dropdown-Menüs (Combobox)
    style.configure("Custom.TCombobox",
        fieldbackground=theme["entry_bg"],
        background=theme["entry_bg"],
        foreground=theme["entry_fg"],
        arrowcolor=theme["fg"]
    )

    # Kalenderfeld (DateEntry)
    style.configure("Custom.DateEntry",
        fieldbackground=theme["entry_bg"],
        background=theme["entry_bg"],
        foreground=theme["entry_fg"]
    )

    # Schleife über alle Widgets, um Theme darauf anzuwenden
    for widget in widgets:
        try:
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])

            elif isinstance(widget, tk.Button):
                # Unterscheide zwischen Abmeldebutton und anderen Buttons
                if "Abmelden" in widget.cget("text"):
                    widget.configure(bg=theme["abmelden"], fg=theme["abmelden_fg"])
                else:
                    widget.configure(bg=theme["btn"], fg=theme["btn_fg"])

            elif isinstance(widget, (tk.Entry, tk.Text)):
                widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])

            elif isinstance(widget, ttk.Combobox):
                widget.configure(style="Custom.TCombobox")

            elif isinstance(widget, DateEntry):
                widget.configure(background=theme["entry_bg"], foreground=theme["entry_fg"])

            elif isinstance(widget, ttk.Treeview):
                widget.configure(style="Treeview")
                # Farbmarkierung für Status
                widget.tag_configure("gruen", background=theme["status"]["gruen"])
                widget.tag_configure("gelb", background=theme["status"]["gelb"])
                widget.tag_configure("rot", background=theme["status"]["rot"])

            elif isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])

        except Exception:
            # Fehler ignorieren – z. B. falls Widget nicht gestylt werden kann
            pass


# Funktion: toggle_darkmode
# Beschreibung:
# Schaltet den Darkmode ein/aus und aktualisiert die Darstellung

def toggle_darkmode(window, widgets, toggle_text_var=None):
    global is_darkmode
    is_darkmode = not is_darkmode

    # Toggle-Button-Beschriftung aktualisieren
    if toggle_text_var:
        toggle_text_var.set("☀️ Hell" if is_darkmode else "🌙 Dunkel")

    # Theme anwenden
    apply_theme(window, widgets)