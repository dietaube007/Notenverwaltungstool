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

