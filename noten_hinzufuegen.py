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

