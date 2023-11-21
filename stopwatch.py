import customtkinter
from datetime import datetime

ORANGE_COLOR = "#f77f2b"
GREEN_COLOR = "#218b21"
RED_COLOR = "#800000"
YELLOW_COLOR = "#9e8b14"
FONT = 'Hoefler Text Black'

class Stopwatch:
    def __init__(self, root):
        self.root = root

        self.start_time = None
        self.elapsed_time = customtkinter.StringVar(value="00:00:00")
        self.running = False

        # Label to display the time
        self.label = customtkinter.CTkLabel(root, textvariable=self.elapsed_time, font=("Helvetica", 60))
        self.label.grid(row=1, column=0, columnspan=3, pady=(0, 40))

        # Start button
        self.start_button = customtkinter.CTkButton(
            root,
            text="Start",
            corner_radius=20,
            fg_color=GREEN_COLOR,
            height=70,
            font=(FONT, 20),
            command=self.start_stopwatch)
        self.start_button.grid(row=2, column=0)

        # Stop button
        self.stop_button = customtkinter.CTkButton(
            root,
            text="Stop",
            corner_radius=20,
            fg_color=RED_COLOR,
            height=70,
            font=(FONT, 20),
            command=self.stop_stopwatch)
        self.stop_button.grid(row=2, column=1)

        # Reset button
        self.reset_button = customtkinter.CTkButton(
            root,
            text="Reset",
            corner_radius=20,
            fg_color=YELLOW_COLOR,
            height=70,
            font=(FONT, 20),
            command=self.reset_stopwatch)
        self.reset_button.grid(row=2, column=2)

    def start_stopwatch(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.update_stopwatch()

    def stop_stopwatch(self):
        self.running = False

    def reset_stopwatch(self):
        self.running = False
        self.start_time = None
        self.elapsed_time.set("00:00:00")

    def update_stopwatch(self):
        if self.running:
            elapsed_time = datetime.now() - self.start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            self.elapsed_time.set(time_str)
            self.root.after(100, self.update_stopwatch)  # Update every 100 milliseconds