import customtkinter
import colors
import fonts


class CustomPopup:
    def __init__(self, master, message):
        self.master = master
        self.message = message

        self.popup = customtkinter.CTkToplevel(master)
        self.popup.title("Info")
        self.popup.grab_set()

        # Label to display the message
        label = customtkinter.CTkLabel(self.popup, text=message, font=(fonts.Hoefler, 30), padx=30, pady=30)
        label.pack()

        # OK button to close the pop-up
        ok_button = customtkinter.CTkButton(self.popup, text="OK", fg_color=colors.ORANGE_COLOR, command=self.close_popup)
        ok_button.pack(ipady=10)

    def close_popup(self):
        self.popup.grab_release()
        self.popup.destroy()