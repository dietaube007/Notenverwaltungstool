# Importieren der notwendigen Bibliotheken
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import verbinde_db
from daten_laden import lade_notentypen, lade_notenwerte, lade_noten
from datetime import datetime, date
from theme import apply_theme

