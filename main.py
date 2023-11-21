import customtkinter
from database import Database
from controller import Controller

DATABASE_NAME = "fitness.db"

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

db = Database(DATABASE_NAME)
view = Controller(db)
