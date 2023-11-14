import tkinter

import customtkinter
import sqlite3
from database import Database
from PIL import ImageTk, Image

DATABASE_NAME = "fitness.db"

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1600x930")
app.title("My Fitness App")

db = Database(DATABASE_NAME)


def login(username, password):
    # Check credentials
    try:
        db.get_user(username, password)

    except Exception as e:
        print(e)

    # Clear inputs
    username_input.delete(0, "end")
    username_input.focus_set()
    password_input.delete(0, "end")


# ===== BACKGROUND FRAME ==== #
wallpaper = ImageTk.PhotoImage(Image.open("images/background.jpg"))

background = customtkinter.CTkLabel(master=app, image=wallpaper)
background.pack()

# ===== LOGIN FORM FRAME ==== #
login_frame = customtkinter.CTkFrame(master=background, width=600, height=500, corner_radius=20)
login_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# Header
login_title = customtkinter.CTkLabel(master=login_frame, text="Log into your Account", font=('Hoefler Text Black', 30))
login_title.place(x=140, y=45)

# Username input
username_input = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username", width=300, height=50, font=('Georgia', 25))
username_input.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

# Password input
password_input = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*", width=300, height=50, font=('Georgia', 25))
password_input.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

# Login button
button = customtkinter.CTkButton(
    master=login_frame,
    text="Login",
    command=lambda: login(username_input.get(), password_input.get()),
    width=300, height=60,
    font=('Hoefler Text Black', 40)
)
button.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

app.mainloop()