import customtkinter
from PIL import ImageTk, Image
from datetime import datetime
import calendar
import time

WIDTH = 600
HEIGHT = 900

ORANGE_COLOR = "#f77f2b"
BACKGROUND_COLOR = "#303030"
GRAY_COLOR = "gray"
GREEN_COLOR = "#218b21"
BLUE_COLOR= "#64b5f6"


class ViewController:
    def __init__(self, database):
        self.app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        self.app.geometry(f"{WIDTH}x{HEIGHT}")
        self.app.title("My Fitness App")
        self.app.resizable(width=True, height=True)
        # self.app.columnconfigure((0), weight=1, uniform='a')
        # self.app.rowconfigure((0, 1, 2), weight=1, uniform='a')

        # Load DB
        self.db = database
        self.db.get_exercises_by_body_parts_and_difficulty(["back", "chest"], 1)
        # Previous frame
        self.previous_frame_dict = {}

        # Loading background frame
        self.__load_background_frame()

        # Load background image
        # self.wallpaper = self.__load_background_image()

        # Loading login page
        self.__load_login_page()

        self.app.mainloop()

    def __load_login_page(self):
        # ===== LOGIN FORM FRAME ==== #
        self.login_frame = customtkinter.CTkFrame(
            master=self.background,
            width=400, height=500,
            corner_radius=20, fg_color="#333333",
            border_width=2, border_color="#d3fd40"
        )
        # self.login_frame.place(relx=.5, rely=.5, anchor="c")
        self.login_frame.pack(side=customtkinter.TOP, expand=True)

        self.previous_frame_dict["login_frame"] = self.login_frame

        # Header
        self.login_title = customtkinter.CTkLabel(
            master=self.login_frame,
            text="Log into your Account",
            font=('Hoefler Text Black', 30)
        )
        self.login_title.grid(row=0, column=1,  padx=(50, 50), pady=(50, 50))

        # Username input
        self.username_input = customtkinter.CTkEntry(
            master=self.login_frame,
            placeholder_text="Username",
            width=250, height=20,
            font=('Georgia', 25)
        )
        self.username_input.grid(row=1, column=1, pady=(0, 30))

        # Password input
        self.password_input = customtkinter.CTkEntry(
            master=self.login_frame,
            placeholder_text="Password", show="*", width=250,
            height=20, font=('Georgia', 25)
        )
        self.password_input.grid(row=2, column=1, pady=(0, 0))

        # Login button
        button = customtkinter.CTkButton(
            master=self.login_frame,
            fg_color="#FD4074",
            text="Login",
            command=lambda: self.__login(self.username_input.get(), self.password_input.get()),
            width=300, height=40,
            font=('Hoefler Text Black', 25)
        )
        button.grid(row=3, column=1, pady=(30, 80))

    def __load_background_frame(self):
        self.background = customtkinter.CTkFrame(master=self.app, fg_color=BACKGROUND_COLOR)
        self.background.pack(fill=customtkinter.BOTH, expand=True)

    def __load_background_image(self):
        return ImageTk.PhotoImage(Image.open("images/background.jpg"))

    def __login(self, username, password):
        # Check credentials
        try:
            # Throws exception if user or password are incorrect
            # self.db.get_user(username, password)

            # Hide login frame
            self.login_frame.pack_forget()

            # Show user home page
            self.__load_user_home_page("username")
        except Exception as e:
            print(e)
            # Clear inputs
            self.username_input.delete(0, "end")
            self.username_input.focus_set()
            self.password_input.delete(0, "end")

    def __go_back(self, previous_frame_name):
        self.__clean_all_active_widgets()
        # Load last widget
        self.back_button_frame.place_forget()
        self.previous_frame_dict[previous_frame_name].pack()

    def __load_back_button(self, previous_frame_name, current_frame_name):
        self.back_button_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=20,
            fg_color=BACKGROUND_COLOR
        )
        self.back_button_frame.place(x=10, y=0)

        # Image
        back_button_img = ImageTk.PhotoImage(Image.open("images/back-arrow.png").resize((40, 40)))

        self.back_button = customtkinter.CTkButton(
            master=self.back_button_frame,
            text="",
            height=30, width=50,
            fg_color=BACKGROUND_COLOR,
            image=back_button_img,
            command=lambda: self.__go_back(previous_frame_name),
        )
        self.back_button.grid(row=0, column=0)

    def __load_user_home_page(self, user):
        self.__clean_all_active_widgets()
        # self.__load_back_button("login_frame", "homepage_frame")
        # TODO: ADD LOG OUT BUTTON
        # ===== HOMEPAGE FORM FRAME ==== #
        self.homepage_frame = customtkinter.CTkFrame(
            master=self.background,
            width=250, height=300,
            corner_radius=20, fg_color=BACKGROUND_COLOR,
         )
        # self.homepage_frame.place(relx=.5, rely=.45, anchor="c")
        self.homepage_frame.pack()

        # Add frame to dictionary
        self.previous_frame_dict["homepage_frame"] = self.homepage_frame

        # Header
        self.homepage_title = customtkinter.CTkLabel(
            master=self.homepage_frame,
            text=f"Hi, {user}! \r Ready for workout ??",
            font=('Hoefler Text Black', 30)
        )
        self.homepage_title.grid(
            row=1, column=0,
            pady=(20, 20), padx=(30, 30),
            columnspan=2
         )
        # SELECT WORKOUT
        # Custom Image
        custom_img = ImageTk.PhotoImage(Image.open("images/custom.png").resize((60, 60)))
        self.select_workout_btn = customtkinter.CTkButton(
            master=self.homepage_frame,
            text="Custom Workout",
            height=150, width=200,
            font=('Hoefler Text Black', 30),
            fg_color=BACKGROUND_COLOR,
            hover_color=BLUE_COLOR,
            image=custom_img,
            border_width=2,
            border_color=BLUE_COLOR,
            command=lambda: self.__custom_workout(),
        )
        self.select_workout_btn.grid(
            row=2, column=1, padx=(30, 30), pady=(100, 40)
        )

        # RANDOM WORKOUT
        # Automatic Image
        automatic_img = ImageTk.PhotoImage(Image.open("images/automatic.png").resize((60, 60)))

        self.random_workout_btn = customtkinter.CTkButton(
            master=self.homepage_frame,
            text="Random Workout",
            height=150, width=200,
            font=('Hoefler Text Black', 30),
            fg_color=BACKGROUND_COLOR,
            hover_color=GREEN_COLOR,
            border_width=2,
            border_color=GREEN_COLOR,
            image=automatic_img
        )
        self.random_workout_btn.grid(
            row=3, column=1,
            padx=(30, 30), pady=(40, 100)
        )

        self.__load_middle_controls_frame()

    def __custom_workout(self):
        # Hide current frame

        self.homepage_frame.pack_forget()
        # Load Custom Workout Pade
        self.__load_custom_workout_page()

    def __load_custom_workout_page(self):
        self.__load_back_button("homepage_frame", "body_parts_frame")
        # ===== CUSTOM WORKOUT FORM FRAME ==== #
        self.__load_body_parts_frame()

        # ===== CUSTOM BODY PART FORM FRAME ==== #
        self.__load_workout_difficulty_frame()

        # ===== EXERCISES COUNT FORM FRAME ==== #
        self.__load_generate_workout_button_frame()

        # ===== MIDDLE CONTROLS FORM FRAME ==== #
        # self.__load_middle_controls_frame()

    def __load_middle_controls_frame(self):
        self.footer_controls_frame = customtkinter.CTkFrame(master=self.background, corner_radius=0,
                                                            # border_color=ORANGE_COLOR,
                                                            # border_width=2
                                                            fg_color=BACKGROUND_COLOR
                                                            )
        self.footer_controls_frame.place(x=60, y=780, relwidth=0.8, relheight=0.15)

        # create the grid
        self.footer_controls_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Calendar Image
        calendar_img = ImageTk.PhotoImage(Image.open("images/calendar.png").resize((60, 60)))

        calendar_btn = customtkinter.CTkButton(
            master=self.footer_controls_frame,
            image=calendar_img,
            text="",
            fg_color=BACKGROUND_COLOR,
            command=lambda: self.__load_calendar_view(),
            )
        calendar_btn.grid(row=0, column=0)

        # Dumbell Image
        dumbell_img = ImageTk.PhotoImage(Image.open("images/workout.png").resize((100, 100)))

        dumbell_btn = customtkinter.CTkButton(
            master=self.footer_controls_frame,
            image=dumbell_img,
            text="",
            fg_color=BACKGROUND_COLOR,
            command=lambda: self.__go_to_homepage(),
        )
        dumbell_btn.grid(row=0, column=1)

        # Timer Image
        timer_img = ImageTk.PhotoImage(Image.open("images/timer.png").resize((60, 60)))

        timer_btn = customtkinter.CTkButton(
            master=self.footer_controls_frame,
            image=timer_img,
            text="",
            fg_color=BACKGROUND_COLOR
        )
        timer_btn.grid(row=0, column=2)

    def __go_to_homepage(self):
        self.__clean_all_active_widgets()

        self.__load_user_home_page("username")

    def __clean_all_active_widgets(self):
        # TODO: In future figure out better way of handling which view should be cleared
        try: self.calendar_frame.place_forget()
        except: pass

        try: self.day_workout_frame.place_forget()
        except: pass

        try: self.homepage_frame.pack_forget()
        except: pass

        try: self.body_parts_frame.place_forget()
        except: pass

        try: self.workout_difficulty_frame.place_forget()
        except: pass

        try: self.generate_workout_button_frame.place_forget()
        except: pass

    def __load_calendar_view(self):
        # Clean page
        self.__clean_all_active_widgets()

        self.__load_back_button("homepage_frame", "calendar_frame")

        self.calendar_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=0,
            border_color=ORANGE_COLOR,
            border_width=2,
            fg_color=BACKGROUND_COLOR,
        )
        self.calendar_frame.place(x=16, y=70, relwidth=0.95, relheight=0.4)

        # create the grid
        self.calendar_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Draw calendar header
        self.calendar_lbl_arr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i in range(7):
            customtkinter.CTkLabel(
                master=self.calendar_frame,
                font=('Hoefler Text Black', 25),
                text=f"{self.calendar_lbl_arr[i]}"
            ).grid(row=0, column=i, padx=16, pady=5)
        # Draw dates
        first_date_of_month = datetime.today().replace(day=1)
        last_day_of_month = calendar.monthrange(first_date_of_month.year, first_date_of_month.month)[1]
        last_date_of_month = datetime.today().replace(day=last_day_of_month)

        first_date_of_month_day = first_date_of_month.strftime("%a")
        additional_loops = self.calendar_lbl_arr.index(first_date_of_month_day)

        # Draw calendar dates
        self.all_dates_arr = self.__draw_calendar_dates(additional_loops, last_day_of_month)

        # Highlight training dates of the user for current month
        found_workouts = self.db.get_user_workouts_for_current_month(1)
        self.__highlight_trained_days(found_workouts)

    def __highlight_trained_days(self, user_workouts):
        for workout in user_workouts:
            workout_exercises = workout[1]
            workout_date = workout[2]

            parsed_date = self.__parse_string_to_date(workout_date)

            if parsed_date.month == datetime.today().month:
                self.all_dates_arr[parsed_date.day - 1].configure(fg_color=ORANGE_COLOR, state=customtkinter.NORMAL, hover_color="white")

    def __parse_string_to_date(self, date):
        format = '%Y-%m-%d'
        return datetime.strptime(date, format).date()

    def __draw_calendar_dates(self, additional_loops, last_day_of_month):
        all_dates_arr = []
        row_cnt = 1
        column_cnt = 0
        lamp = additional_loops
        for i in range(last_day_of_month + additional_loops):

            curr_index_text = i - lamp
            if additional_loops > 0:
                curr_index_text = ""
                additional_loops -= 1
            else:
                curr_index_text += 1

            curr_date = customtkinter.CTkButton(
                master=self.calendar_frame,
                font=('Arial', 40),
                text=f"{curr_index_text}",
                width=20,
                height=20,
                fg_color=BACKGROUND_COLOR
            )
            # If not empty we style the button
            if str(curr_index_text) != "":
                curr_date.configure(
                    border_width=2,
                    border_color=ORANGE_COLOR,
                    fg_color=BACKGROUND_COLOR,
                    state=customtkinter.DISABLED,
                    command=lambda day=curr_index_text: self.__load_day_workout_frame(day),
                )
            curr_date.grid(row=row_cnt, column=column_cnt, padx=8, pady=5, sticky="ew")

            if str(curr_index_text) != "":
                all_dates_arr.append(curr_date)

            column_cnt += 1
            if column_cnt == 7:
                column_cnt = 0
                row_cnt += 1

        return all_dates_arr

    def __load_day_workout_frame(self, day_date):
        self.__load_back_button("homepage_frame", "day_workout_frame")
        print(f"day_date -> {day_date}")
        self.day_workout_frame = customtkinter.CTkScrollableFrame(
            master=self.background, corner_radius=0,
            fg_color=BACKGROUND_COLOR,
            scrollbar_button_hover_color=ORANGE_COLOR,
            scrollbar_button_color=GRAY_COLOR
        )
        self.day_workout_frame.place(x=16, y=440, relwidth=0.95, relheight=0.37)
        # self.day_workout_frame.pack()

        # create the grid
        self.day_workout_frame.columnconfigure((0), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Add frame to dictionary
        self.previous_frame_dict["day_workout_frame"] = self.day_workout_frame

        # TODO: Put first argument the logged user id
        found_workout = self.db.get_user_day_workout(1, day_date)
        if found_workout is None: self.__show_no_workout_message()
        print(found_workout[2])
        workout_date = datetime.strptime(found_workout[2], '%Y-%m-%d').strftime('%d-%b-%Y')
        self.day_workout_frame.configure(label_text=workout_date, label_font=('Hoefler Text Black', 25), label_fg_color=ORANGE_COLOR)
        self.__show_day_workout_exercises(found_workout)

    def __show_day_workout_exercises(self, workout):
        exercises = workout[1]
        exercises_ids_arr = exercises.split(",")

        for i in range(len(exercises_ids_arr)):
            curr_exercise = self.db.get_exercise_name_by_id(int(exercises_ids_arr[i]))
            print(curr_exercise)
            customtkinter.CTkButton(
                master=self.day_workout_frame,
                text=f"{curr_exercise}",
                corner_radius=20,
                hover_color=ORANGE_COLOR,
                text_color="black",
                fg_color='gray',
                font=('Hoefler Text Black', 20),
            ).grid(row=i, column=0, padx=10, pady=10)

    def __show_no_workout_message(self):
        no_workout_found = customtkinter.CTkLabel(
            master=self.day_workout_frame,
            text="No Workout found for this day !!!",
            font=('Hoefler Text Black', 30),
            text_color="red"
        )
        no_workout_found.grid(row=0, column=0, padx=20, pady=20)

    def __load_generate_workout_button_frame(self):
        self.generate_workout_button_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=0,
            fg_color=BACKGROUND_COLOR
        )
        self.generate_workout_button_frame.place(x=70, y=550, relwidth=0.8, relheight=0.15)

        # create the grid
        self.generate_workout_button_frame.columnconfigure((0), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        generate_workout = customtkinter.CTkButton(
            master=self.generate_workout_button_frame,
            text="Generate",
            font=('Hoefler Text Black', 25),
            width=400,
            height=50,
            fg_color=BACKGROUND_COLOR,
            hover_color=ORANGE_COLOR,
            border_color=ORANGE_COLOR,
            border_width=2,
            command=lambda: self.__generate_workout(),
        )
        generate_workout.grid(row=0, column=0)

    def __generate_workout(self):
        selected_body_parts = self.__get_selected_body_parts()
        selected_difficulty = self.difficulty_state

        self.__get_custom_generated_workout(selected_body_parts, selected_difficulty)

    def __get_custom_generated_workout(self, body_parts, difficulty):
        # found_exercises = self.db.

        pass
    def __get_selected_body_parts(self):
        curr_bp_array = []
        [curr_bp_array.append(bp.cget("text")) for bp in self.body_parts_bnt_arr if bp.cget("fg_color") == ORANGE_COLOR]

        return curr_bp_array

    def __load_exercises_count_frame(self):
        self.exercises_count_frame = customtkinter.CTkFrame(master=self.background, corner_radius=20, border_color=ORANGE_COLOR,
                                                       border_width=2)
        self.exercises_count_frame.place(x=30, y=530, relwidth=0.35, relheight=0.2)

        # create the grid
        self.exercises_count_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Header
        self.exercise_count_header = customtkinter.CTkLabel(
            master=self.exercises_count_frame, text="Exercises Count", font=('Hoefler Text Black', 18)
        )
        self.exercise_count_header.grid(row=0, column=0, columnspan=3, pady=20)

        # Counter variable
        self.exercise_counter = 1
        # Minus button
        self.exercise_count_minus = customtkinter.CTkButton(
            master=self.exercises_count_frame,
            text=f"-",
            corner_radius=40,
            hover_color=ORANGE_COLOR,
            text_color="black",
            fg_color='gray',
            width=30,
            font=('Hoefler Text Black', 30),
            command=lambda: self.__decrement_exercise_count(),
        )
        self.exercise_count_minus.grid(row=1, column=0, pady=20)

        # Counter Label
        self.exercise_count_label = customtkinter.CTkLabel(
            master=self.exercises_count_frame,
            corner_radius=20,
            text_color="white",
            font=('Arial', 40),
            text=f"{self.exercise_counter}"
        )
        self.exercise_count_label.grid(row=1, column=1, pady=20)

        # Plus button
        self.exercise_count_plus = customtkinter.CTkButton(
            master=self.exercises_count_frame,
            text=f"+",
            corner_radius=40,
            hover_color=ORANGE_COLOR,
            text_color="black",
            fg_color='gray',
            width=30,
            font=('Hoefler Text Black', 30),
            command=lambda: self.__increment_exercise_count(),
        )
        self.exercise_count_plus.grid(row=1, column=2, pady=20)

    def __decrement_exercise_count(self):
        if self.exercise_counter >= 1:
            self.exercise_counter -= 1
            self.exercise_count_label.configure(text=str(self.exercise_counter))

    def __increment_exercise_count(self):
        if self.exercise_counter < 30:
            self.exercise_counter += 1
            self.exercise_count_label.configure(text=str(self.exercise_counter))

    def __load_body_parts_frame(self):
        self.body_parts_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=20,
            border_color=ORANGE_COLOR,
            border_width=2
        )
        self.body_parts_frame.place(x=30, y=70, relwidth=0.9, relheight=0.33)

        # create the grid
        self.body_parts_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Add frame to dictionary
        self.previous_frame_dict["body_parts_frame"] = self.body_parts_frame

        # Body Parts Label
        body_parts_label = customtkinter.CTkLabel(
            master=self.body_parts_frame,
            text="Choose Body Parts",
            font=('Hoefler Text Black', 25)
        )
        body_parts_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        # Image
        body_img = ImageTk.PhotoImage(Image.open("images/body.png").resize((60, 60)))

        image_body_lbl = customtkinter.CTkLabel(
            master=self.body_parts_frame, text="", image=body_img
        )
        image_body_lbl.grid(row=0, column=2, columnspan=1, pady=(20, 20))

        result = self.db.get_all_body_parts()
        curr_col_cnt = 0
        curr_row_cnt = 1

        self.body_parts_bnt_arr = []
        for i in range(len(result)):
            body_part = result[i]

            self.body_parts_bnt_arr.append(
                customtkinter.CTkButton(
                    master=self.body_parts_frame,
                    text=f"{body_part[1]}",
                    corner_radius=20,
                    hover_color=ORANGE_COLOR,
                    text_color="black",
                    fg_color='gray',
                    font=('Hoefler Text Black', 15),
                    command=lambda c=i: self.__change_btn_state(c),
                )
            )
            self.body_parts_bnt_arr[i].grid(row=curr_row_cnt, column=curr_col_cnt, padx=3, pady=10)
            curr_col_cnt += 1
            if curr_col_cnt % 3 == 0:
                curr_row_cnt += 1
                curr_col_cnt = 0

    def __load_workout_difficulty_frame(self):
        self.workout_difficulty_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=20,
            border_color=ORANGE_COLOR,
            border_width=2
        )
        self.workout_difficulty_frame.place(x=30, y=390, relwidth=0.9, relheight=0.15)

        # Create the grid
        self.workout_difficulty_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        # # self.workout_difficulty_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        difficulty_img = ImageTk.PhotoImage(Image.open("images/speedometer1.png").resize((40, 40)))

        # Difficulty Label
        difficulty_label = customtkinter.CTkLabel(
            master=self.workout_difficulty_frame, text="Workout Difficulty", font=('Hoefler Text Black', 25),
        )
        difficulty_label.grid(row=0, column=0, columnspan=2, pady=20)

        difficulty_img_lbl = customtkinter.CTkLabel(
            master=self.workout_difficulty_frame,
            text="",
            image=difficulty_img,
            compound="right"
        )
        difficulty_img_lbl.grid(row=0, column=2, columnspan=1, pady=20)

        # Difficulty Options
        self.difficulty_state = 1
        # Beginner
        self.difficulty_beginner = customtkinter.CTkRadioButton(
            master=self.workout_difficulty_frame,
            text="Beginner",
            font=('Hoefler Text Black', 20),
            text_color="#2BC4E9",
            hover_color="#2BC4E9",
            fg_color="white",
            # variable=self.difficulty_state,
            value=1,
            command=lambda: self.__change_difficulty_button_states("Beginner")
        )
        self.difficulty_beginner.grid(row=1, column=0, padx=10)

        # Intermediate
        self.difficulty_intermediate = customtkinter.CTkRadioButton(
            master=self.workout_difficulty_frame,
            text="Intermediate",
            font=('Hoefler Text Black', 20),
            text_color=GRAY_COLOR,
            hover_color="#fb4f1b",
            fg_color="white",
            # variable=self.difficulty_state,
            value=2,
            command=lambda: self.__change_difficulty_button_states("Intermediate")
        )
        self.difficulty_intermediate.grid(row=1, column=1, padx=10)

        # Advanced
        self.difficulty_advanced = customtkinter.CTkRadioButton(
            master=self.workout_difficulty_frame,
            text="Advanced",
            font=('Hoefler Text Black', 20),
            text_color=GRAY_COLOR,
            hover_color="#d52522",
            fg_color="white",
            # variable=self.difficulty_state,
            value=3,
            command=lambda: self.__change_difficulty_button_states("Advanced")
        )
        self.difficulty_advanced.grid(row=1, column=2, padx=10)

    def __change_btn_state(self, btn_index):
        curr_btn = self.body_parts_bnt_arr[btn_index]
        curr_btn_color = curr_btn.cget("fg_color")
        new_color = ""
        if curr_btn_color == ORANGE_COLOR: new_color = GRAY_COLOR
        else: new_color = ORANGE_COLOR

        curr_btn.configure(fg_color=new_color)

    def __change_difficulty_button_states(self, selected_state):
        beginner = ""
        intermediate = ""
        advanced = ""
        if selected_state == "Beginner":
            self.difficulty_state = 1
            beginner = "#2BC4E9"
            intermediate = GRAY_COLOR
            advanced = GRAY_COLOR
        elif selected_state == "Intermediate":
            self.difficulty_state = 2
            beginner = GRAY_COLOR
            intermediate = "#fb4f1b"
            advanced = GRAY_COLOR
        else:
            self.difficulty_state = 3
            beginner = GRAY_COLOR
            intermediate = GRAY_COLOR
            advanced = "#d52522"

        self.difficulty_beginner.configure(text_color=beginner)
        self.difficulty_intermediate.configure(text_color=intermediate)
        self.difficulty_advanced.configure(text_color=advanced)
