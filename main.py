import tkinter

import customtkinter
import sqlite3
from database import Database
from PIL import ImageTk, Image
from view_controller import ViewController

DATABASE_NAME = "fitness.db"

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.geometry("1600x930")
# app.title("My Fitness App")
# app.resizable(width=False, height=False)

db = Database(DATABASE_NAME)
view = ViewController(db)


# def login(username, password):
#     # Check credentials
#     try:
#         # Throws exception if user or password are incorrect
#         db.get_user(username, password)
#         # Hide login frame
#         login_frame.grid_forget()
#         # Show user home page
#
#
#     except Exception as e:
#         print(e)
#         # Clear inputs
#         username_input.delete(0, "end")
#         username_input.focus_set()
#         password_input.delete(0, "end")



# ===== BACKGROUND FRAME ==== #
# wallpaper = ImageTk.PhotoImage(Image.open("images/background.jpg"))

# background = customtkinter.CTkLabel(master=app, text="", image=wallpaper)
# background.place(x=0, y=0)
# # ===== CHOOSE LEVEL FORM FRAME ==== #
# right_frame = customtkinter.CTkFrame(master=background, width=400, height=500, fg_color="yellow")
# right_frame.grid(row=0, column=3)
#
# side_frame = customtkinter.CTkFrame(master=background, width=200, height=500, fg_color="yellow")
# side_frame.pack()

# # ===== LOGIN FORM FRAME ==== #
# login_frame = customtkinter.CTkFrame(master=background, width=600, height=500, corner_radius=20)
# login_frame.grid(row=0, column=0)
#
# # Header
# login_title = customtkinter.CTkLabel(master=login_frame, text="Log into your Account", font=('Hoefler Text Black', 30))
# login_title.grid(row=0, column=0, padx=(50, 50), pady=(50, 50))
#
# # Username input
# username_input = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username", width=300, height=50, font=('Georgia', 25))
# username_input.grid(row=1, column=0, pady=(0, 30))
#
# # Password input
# password_input = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*", width=300, height=50, font=('Georgia', 25))
# password_input.grid(row=2, column=0, pady=(0, 30))
#
# # Login button
# button = customtkinter.CTkButton(
#     master=login_frame,
#     text="Login",
#     command=lambda: login(username_input.get(), password_input.get()),
#     width=300, height=60,
#     font=('Hoefler Text Black', 40)
# )
# button.grid(row=3, column=0, pady=(50, 80))



app.mainloop()