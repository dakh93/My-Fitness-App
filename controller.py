import customtkinter
from PIL import ImageTk, Image
from datetime import datetime
import calendar
import random
from custom_popup import CustomPopup
import colors
import fonts

import exception
from stopwatch import Stopwatch
from user import User

WIDTH = 600
HEIGHT = 900

fonts.Hoefler = 'Hoefler Text Black'

EXERCISE_MIN_COUNT = 4
EXERCISE_MAX_COUNT = 10

AUTO_BODY_PARTS_MIN = 3
AUTO_BODY_PARTS_MAX = 7

AUTO_DIFFICULTY_MIN = 1
AUTO_DIFFICULTY_MAX = 3


class Controller:
    def __init__(self, database):
        self.app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        self.app.geometry(f"{WIDTH}x{HEIGHT}")
        self.app.title("My Fitness App")
        self.app.resizable(width=True, height=True)

        # Load DB
        self.db = database

        # Previous frame
        self.previous_frame_dict = {}

        # Loading background frame
        self.__load_background_frame()

        # Loading login page
        self.__load_login_page()

        # Start app
        self.app.mainloop()

    def __load_login_page(self):
        # Welcome image
        welcome_img = ImageTk.PhotoImage(Image.open("images/welcome.png").resize((150, 150)))

        self.welcome_lbl = customtkinter.CTkLabel(
            master=self.background,
            text="",
            image=welcome_img
        )
        self.welcome_lbl.place(x=220, y=10)

        self.tab_views = customtkinter.CTkTabview(
            master=self.background,
            width=450,
            height=500,
            border_width=2,
            border_color=colors.ORANGE_COLOR,
            corner_radius=20,
            fg_color=colors.BACKGROUND_COLOR
        )
        self.tab_views.place(relx=.5, rely=.5, anchor="c")
        self.tab_views.add("Login")
        self.tab_views.add("Register")

        # ===== LOGIN TAB FRAME ==== #
        self.login_frame = customtkinter.CTkFrame(
            master=self.tab_views.tab("Login"),
            width=400, height=500,
            fg_color=colors.BACKGROUND_COLOR
        )
        # self.login_frame.place(relx=.5, rely=.5, anchor="c")
        self.login_frame.pack(side=customtkinter.TOP, expand=True)

        self.previous_frame_dict["login_frame"] = self.login_frame

        # Header
        self.login_title = customtkinter.CTkLabel(
            master=self.login_frame,
            text="Log into your Account",
            font=(fonts.Hoefler, 30)
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
        self.button = customtkinter.CTkButton(
            master=self.login_frame,
            fg_color=colors.ORANGE_COLOR,
            text="Login",
            command=lambda: self.__login(self.username_input.get(), self.password_input.get()),
            width=300, height=40,
            font=(fonts.Hoefler, 25)
        )
        self.button.grid(row=3, column=1, pady=(30, 80))

        # ===== REGISTER TAB ==== #
        self.register_frame = customtkinter.CTkFrame(
            master=self.tab_views.tab("Register"),
            width=400, height=500,
            fg_color=colors.BACKGROUND_COLOR
        )
        # self.register_frame.place(relx=.5, rely=.5, anchor="c")
        self.register_frame.pack(side=customtkinter.TOP, expand=True)
        # Header
        self.register_header = customtkinter.CTkLabel(
            master=self.register_frame,
            text="Register",
            font=(fonts.Hoefler, 50)
        )
        self.register_header.grid(row=0, column=0, padx=(50, 50), pady=(50, 50))

        # Username
        self.register_username_input = customtkinter.CTkEntry(
            master=self.register_frame,
            placeholder_text="Username",
            width=250, height=20,
            font=('Georgia', 25)
        )
        self.register_username_input.grid(row=1, column=0, pady=(0, 30))

        # First Name
        self.register_first_name_input = customtkinter.CTkEntry(
            master=self.register_frame,
            placeholder_text="First name",
            width=250, height=20,
            font=('Georgia', 25)
        )
        self.register_first_name_input.grid(row=2, column=0, pady=(0, 30))

        # Last Name
        self.register_last_name_input = customtkinter.CTkEntry(
            master=self.register_frame,
            placeholder_text="Last name",
            width=250, height=20,
            font=('Georgia', 25)
        )
        self.register_last_name_input.grid(row=3, column=0, pady=(0, 30))

        # Password input
        self.register_password_input = customtkinter.CTkEntry(
            master=self.register_frame,
            placeholder_text="Password", show="*", width=250,
            height=20, font=('Georgia', 25)
        )
        self.register_password_input.grid(row=4, column=0, pady=(0, 30))

        # Register button
        self.register_button = customtkinter.CTkButton(
            master=self.register_frame,
            fg_color=colors.ORANGE_COLOR,
            text="Register",
            command=lambda: self.__register_user(
                self.register_username_input,
                self.register_first_name_input,
                self.register_last_name_input,
                self.register_password_input
            ),
            width=350, height=40,
            font=(fonts.Hoefler, 25)
        )
        self.register_button.grid(row=5, column=0, pady=(0, 30))

    def check_empty_field(*args):
        if args:
            for field in args[1]:
                if field.get(): pass
                else:
                    field.focus_set()
                    raise Exception(exception.EMPTY_FIELD)

    def __register_user(self, username, first_name, last_name, password):
        try:
            # Check if any filed is empty
            self.check_empty_field([username, first_name, last_name, password])
            # Check if user with same name exists in db
            self.check_if_user_exists(username.get())
            # Add user to database
            self.db.add_user(username.get(), first_name.get(), last_name.get(), password.get())

            # Clear inputs
            self.register_username_input.delete(0, "end")
            self.register_first_name_input.delete(0, "end")
            self.register_last_name_input.delete(0, "end")
            self.register_password_input.delete(0, "end")

            self.tab_views.place_forget()
            self.welcome_lbl.place_forget()
            self.__load_login_page()

        except Exception as e:
            popup = CustomPopup(self.background, e)

    def check_if_user_exists(self, username):
        return self.db.get_user_by_username(username)


    def __load_background_frame(self):
        self.background = customtkinter.CTkFrame(master=self.app, fg_color=colors.BACKGROUND_COLOR)
        self.background.pack(fill=customtkinter.BOTH, expand=True)

    def __load_background_image(self):
        return ImageTk.PhotoImage(Image.open("images/background.jpg"))

    def __login(self, username, password):
        # Check credentials
        try:
            # Throws exception if user or password are incorrect
            # Return user in format: (id, firstName, lastName, username, password)
            self.__currently_logged_user = self.db.get_user(username, password)

            # Hide login frame
            self.login_frame.pack_forget()

            # Show user home page
            self.__load_user_home_page()
        except Exception as e:
            login_error = customtkinter.CTkLabel(
                master=self.login_frame,
                text=f"{e}",
                font=(fonts.Hoefler, 25),
                text_color="red"
            )
            login_error.grid(row=4, column=1)

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
            fg_color=colors.BACKGROUND_COLOR
        )
        self.back_button_frame.place(x=10, y=0)

        # Image
        back_button_img = ImageTk.PhotoImage(Image.open("images/back-arrow.png").resize((40, 40)))

        self.back_button = customtkinter.CTkButton(
            master=self.back_button_frame,
            text="",
            height=30, width=50,
            fg_color=colors.BACKGROUND_COLOR,
            image=back_button_img,
            command=lambda: self.__go_back(previous_frame_name),
        )
        self.back_button.grid(row=0, column=0)

    def __logout(self):
        # Clean all active widgets
        self.__close_additional_windows()
        self.background.forget()
        self.__load_background_frame()
        self.__load_login_page()

    def __load_user_home_page(self):
        self.__clean_all_active_widgets()
        # ===== HOMEPAGE FORM FRAME ==== #
        self.homepage_frame = customtkinter.CTkFrame(
            master=self.background,
            width=250, height=300,
            corner_radius=20, fg_color=colors.BACKGROUND_COLOR,
         )
        self.homepage_frame.pack()

        self.logout_btn = customtkinter.CTkButton(
            master=self.background,
            text="Logout",
            fg_color=colors.RED_COLOR,
            font=(fonts.Hoefler, 20),
            command=lambda : self.__logout()
        )
        self.logout_btn.place(x=450, y=20)
        # Add frame to dictionary
        self.previous_frame_dict["homepage_frame"] = self.homepage_frame

        # Header
        homepage_img = ImageTk.PhotoImage(Image.open("images/hello.png").resize((60, 60)))
        self.homepage_image = customtkinter.CTkLabel(
            master=self.homepage_frame,
            text=" ",
            image=homepage_img,
        )
        self.homepage_image.grid(
            row=0, column=1,
            padx=(30, 30), pady=(20, 0),
            columnspan=2
        )

        self.homepage_title = customtkinter.CTkLabel(
            master=self.homepage_frame,
            text=f"{self.__currently_logged_user.get_name()}! \r Ready for workout ??",
            font=(fonts.Hoefler, 30),
        )
        self.homepage_title.grid(
            row=1, column=1,
            pady=(2, 20), padx=(30, 30),
            columnspan=2
         )
        # SELECT WORKOUT
        # Custom Image
        custom_img = ImageTk.PhotoImage(Image.open("images/custom.png").resize((60, 60)))
        self.select_workout_btn = customtkinter.CTkButton(
            master=self.homepage_frame,
            text="Custom Workout",
            height=150, width=200,
            font=(fonts.Hoefler, 30),
            fg_color=colors.BACKGROUND_COLOR,
            hover_color=colors.BLUE_COLOR,
            image=custom_img,
            border_width=2,
            border_color=colors.BLUE_COLOR,
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
            font=(fonts.Hoefler, 30),
            fg_color=colors.BACKGROUND_COLOR,
            hover_color=colors.GREEN_COLOR,
            border_width=2,
            border_color=colors.GREEN_COLOR,
            image=automatic_img,
            command=lambda: self.__generate_workout("auto"),
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


    def __load_middle_controls_frame(self):
        self.footer_controls_frame = customtkinter.CTkFrame(
            master=self.background, corner_radius=0,
            fg_color=colors.BACKGROUND_COLOR
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
            fg_color=colors.BACKGROUND_COLOR,
            command=lambda: self.__load_calendar_view(),
            )
        calendar_btn.grid(row=0, column=0)

        # Dumbell Image
        dumbell_img = ImageTk.PhotoImage(Image.open("images/workout.png").resize((100, 100)))

        dumbell_btn = customtkinter.CTkButton(
            master=self.footer_controls_frame,
            image=dumbell_img,
            text="",
            fg_color=colors.BACKGROUND_COLOR,
            command=lambda: self.__go_to_homepage(),
        )
        dumbell_btn.grid(row=0, column=1)

        # Timer Image
        timer_img = ImageTk.PhotoImage(Image.open("images/timer.png").resize((60, 60)))

        stopwatch_btn = customtkinter.CTkButton(
            master=self.footer_controls_frame,
            image=timer_img,
            text="",
            fg_color=colors.BACKGROUND_COLOR,
            command=lambda: self.__load_stopwatch_view()
        )
        stopwatch_btn.grid(row=0, column=2)

    def __go_to_homepage(self):
        self.__clean_all_active_widgets()

        self.__load_user_home_page()

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

        try: self.ready_workout_frame.place_forget()
        except: pass

        try: self.stopwatch_frame.place_forget()
        except: pass

        try: self.tab_views.place_forget()
        except: pass

        try: self.welcome_lbl.place_forget()
        except: pass

    def __load_calendar_view(self):
        # Clean page
        self.__clean_all_active_widgets()

        self.__load_back_button("homepage_frame", "calendar_frame")

        self.calendar_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=0,
            border_color=colors.ORANGE_COLOR,
            border_width=2,
            fg_color=colors.BACKGROUND_COLOR,
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
                font=(fonts.Hoefler, 25),
                text=f"{self.calendar_lbl_arr[i]}"
            ).grid(row=0, column=i, padx=14, pady=5)
        # Draw dates
        first_date_of_month = datetime.today().replace(day=1)
        last_day_of_month = calendar.monthrange(first_date_of_month.year, first_date_of_month.month)[1]
        last_date_of_month = datetime.today().replace(day=last_day_of_month)

        first_date_of_month_day = first_date_of_month.strftime("%a")
        additional_loops = self.calendar_lbl_arr.index(first_date_of_month_day)

        # Draw calendar dates
        self.all_dates_arr = self.__draw_calendar_dates(additional_loops, last_day_of_month)

        # Highlight training dates of the user for current month
        found_workouts = self.db.get_user_workouts_for_current_month(self.__currently_logged_user.get_id())
        self.__highlight_trained_days(found_workouts)

    def __load_stopwatch_view(self):
        # Clean page
        self.__clean_all_active_widgets()

        self.__load_back_button("homepage_frame", "stopwatch_frame")

        self.stopwatch_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=0,
            fg_color=colors.BACKGROUND_COLOR
        )
        self.stopwatch_frame.place(x=30, y=200, relwidth=0.9, relheight=0.6)

        # create the grid
        self.stopwatch_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')

        self.stopwatch_lbl = customtkinter.CTkLabel(
            master=self.stopwatch_frame,
            text="STOPWATCH",
            font=(fonts.Hoefler, 50),
        )
        self.stopwatch_lbl.grid(row=0, column=0, columnspan=3, pady=50)

        self.stopwatch = Stopwatch(self.stopwatch_frame)

    def __highlight_trained_days(self, user_workouts):

        for workout in user_workouts:
            workout_exercises = workout[1]
            workout_date = workout[2]

            parsed_date = self.__parse_string_to_date(workout_date)

            if parsed_date.month == datetime.today().month:
                self.all_dates_arr[parsed_date.day - 1].configure(fg_color=colors.ORANGE_COLOR, state=customtkinter.NORMAL, hover_color="white")

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
                fg_color=colors.BACKGROUND_COLOR
            )
            # If not empty we style the button
            if str(curr_index_text) != "":
                curr_date.configure(
                    border_width=2,
                    border_color=colors.ORANGE_COLOR,
                    fg_color=colors.BACKGROUND_COLOR,
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
        # Deleting scrollable frame with day exercises otherwise they stack on each other
        try: self.day_workout_frame.place_forget()
        except: pass

        self.day_workout_frame = customtkinter.CTkScrollableFrame(
            master=self.background, corner_radius=0,
            fg_color=colors.BACKGROUND_COLOR,
            scrollbar_button_hover_color=colors.ORANGE_COLOR,
            scrollbar_button_color=colors.GRAY_COLOR
        )
        self.day_workout_frame.place(x=16, y=440, relwidth=0.95, relheight=0.37)
        # self.day_workout_frame.pack()

        # create the grid
        self.day_workout_frame.columnconfigure((0), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Add frame to dictionary
        self.previous_frame_dict["day_workout_frame"] = self.day_workout_frame

        found_workout = self.db.get_user_day_workout(self.__currently_logged_user.get_id(), day_date)
        if found_workout is None: self.__show_no_workout_message()
        workout_date = datetime.strptime(found_workout[2], '%Y-%m-%d').strftime('%d-%b-%Y')
        self.day_workout_frame.configure(label_text=workout_date, label_font=(fonts.Hoefler, 25), label_fg_color=colors.ORANGE_COLOR)
        self.__show_day_workout_exercises(found_workout)

    def __show_day_workout_exercises(self, workout):
        exercises = workout[1]
        exercises_ids_arr = exercises.split(",")

        for i in range(len(exercises_ids_arr)):
            curr_exercise = self.db.get_exercise_name_by_id(int(exercises_ids_arr[i]))
            customtkinter.CTkButton(
                master=self.day_workout_frame,
                text=f"{curr_exercise}",
                corner_radius=20,
                hover_color=colors.ORANGE_COLOR,
                text_color="black",
                fg_color='gray',
                font=(fonts.Hoefler, 20),
            ).grid(row=i, column=0, padx=10, pady=10)

    def __show_no_workout_message(self):
        no_workout_found = customtkinter.CTkLabel(
            master=self.day_workout_frame,
            text="No Workout found for this day !!!",
            font=(fonts.Hoefler, 30),
            text_color="red"
        )
        no_workout_found.grid(row=0, column=0, padx=20, pady=20)

    def __load_generate_workout_button_frame(self):
        self.generate_workout_button_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=0,
            fg_color=colors.BACKGROUND_COLOR
        )
        self.generate_workout_button_frame.place(x=70, y=550, relwidth=0.8, relheight=0.15)

        # create the grid
        self.generate_workout_button_frame.columnconfigure((0), weight=1, uniform='a')
        # self.body_parts_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        generate_workout = customtkinter.CTkButton(
            master=self.generate_workout_button_frame,
            text="Generate",
            font=(fonts.Hoefler, 25),
            width=400,
            height=50,
            fg_color=colors.BACKGROUND_COLOR,
            hover_color=colors.ORANGE_COLOR,
            border_color=colors.ORANGE_COLOR,
            border_width=2,
            command=lambda: self.__generate_workout("custom"),
        )
        generate_workout.grid(row=0, column=0)

    def __generate_workout(self, custom_or_auto):

        self.generated_workout_window = customtkinter.CTkToplevel(self.app)
        self.generated_workout_window.geometry(f"{WIDTH}x{HEIGHT-100}")
        self.generated_workout_window.config(background=colors.BACKGROUND_COLOR)
        self.generated_workout_window.title("Workout")
        self.generated_workout_window.grab_set()

        try:
            # Create a Label in New window
            if custom_or_auto == "custom":

                selected_body_part_names = self.__get_selected_body_parts()

                selected_body_parts_ids = []
                [selected_body_parts_ids.append(self.db.get_body_part_id_by_name(bp_name)) for bp_name in selected_body_part_names]

                selected_difficulty = self.difficulty_state.get()

                # Get generated workout as list in format for each index: (114, 'barbell decline wide-grip pullover', 1)
                generated_workout = self.__get_custom_generated_workout(selected_body_parts_ids, selected_difficulty)

            else:
                # BODY PARTS GENERATING
                all_body_parts = self.db.get_all_body_parts()
                body_parts_cnt = random.randint(AUTO_BODY_PARTS_MIN, AUTO_BODY_PARTS_MAX)

                final_generated_body_parts = []
                for bp in range(body_parts_cnt):
                    curr_selected_body_part = random.choice(all_body_parts)
                    if curr_selected_body_part[0] not in final_generated_body_parts:
                        final_generated_body_parts.append(curr_selected_body_part[0])

                # DIFFICULTY GENERATING
                all_difficulties = self.db.get_all_difficulties()
                final_selected_difficulty = random.choice(all_difficulties)[0]

                generated_workout = self.__get_custom_generated_workout(final_generated_body_parts, final_selected_difficulty)

            # self.generated_workout_frame()
            self.ready_workout_frame = customtkinter.CTkScrollableFrame(
                master=self.generated_workout_window,
                corner_radius=0,
                scrollbar_button_hover_color=colors.ORANGE_COLOR,
                scrollbar_button_color=colors.GRAY_COLOR,
                fg_color=colors.BACKGROUND_COLOR
            )
            self.ready_workout_frame.place(x=30, y=40, relwidth=0.9, relheight=0.4)

            # create the grid
            self.ready_workout_frame.columnconfigure((0), weight=1, uniform='a')
            # self.ready_workout_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

            curr_col_cnt = 0
            curr_row_cnt = 1

            self.ready_workout_arr = []
            for i in range(len(generated_workout)):
                body_part = generated_workout[i]

                self.ready_workout_arr.append(
                    customtkinter.CTkButton(
                        master=self.ready_workout_frame,
                        text=f"{body_part[1]}",
                        corner_radius=20,
                        hover_color=colors.ORANGE_COLOR,
                        text_color="black",
                        fg_color='gray',
                        font=(fonts.Hoefler, 20),
                    )
                )
                self.ready_workout_arr[i].grid(row=curr_row_cnt, column=curr_col_cnt, padx=3, pady=10)
                curr_row_cnt +=1

            self.generated_workout_window.after(2, lambda: self.generated_workout_window.focus_force())

            # SAVE WORKOUT BUTTON
            self.save_workout = customtkinter.CTkButton(
                self.generated_workout_window,
                text="Save Workout in Calendar",
                fg_color=colors.GREEN_COLOR,
                font=(fonts.Hoefler, 20),
                command=lambda : self.__save_workout_to_db(generated_workout))
            self.save_workout.place(x=30, y=390, relwidth=0.9, relheight=0.05)

            self.stopwatch_frame = customtkinter.CTkFrame(
                master=self.generated_workout_window,
                corner_radius=0,
                fg_color=colors.BACKGROUND_COLOR
            )
            self.stopwatch_frame.place(x=30, y=470, relwidth=0.9, relheight=0.3)

            # create the grid
            self.stopwatch_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')

            self.stopwatch = Stopwatch(self.stopwatch_frame)

            self.close_window_btn = customtkinter.CTkButton(
                self.generated_workout_window,
                text="Close",
                fg_color=colors.ORANGE_COLOR,
                font=(fonts.Hoefler, 20),
                command=lambda : self.__close_additional_windows())
            self.close_window_btn.place(x=30, y=720, relwidth=0.9, relheight=0.05)
        except Exception as error:
            popup = CustomPopup(self.app, error)
            self.generated_workout_window.destroy()

    def __close_additional_windows(self):
        try:
            self.generated_workout_window.grab_release()
            self.generated_workout_window.destroy()
        except:
            pass

    def __save_workout_to_db(self, workout):
        self.db.save_workout_for_the_day(workout, self.__currently_logged_user.get_id())
        self.save_workout.configure(
            text="Workout saved successfully!",
            fg_color= colors.BACKGROUND_COLOR,
            state=customtkinter.DISABLED,
            border_color=colors.GREEN_COLOR,
            border_width=2
        )

    def __get_custom_generated_workout(self, body_parts_ids, difficulty):
        # Get exercises depending on filters
        # tuple format: (997, 'lever t-bar reverse grip row', 1)
        found_exercises = self.db.get_exercises_by_body_parts_and_difficulty(body_parts_ids, difficulty)

        exercises_count = random.randint(EXERCISE_MIN_COUNT, EXERCISE_MAX_COUNT)

        generated_workout = []
        for i in range(exercises_count):
            random_body_part_id = random.choice(body_parts_ids)
            random_exercise = random.choice(found_exercises)
            while random_exercise[1] == random_body_part_id:
                random_exercise = random.choice(found_exercises)
            generated_workout.append(random_exercise)

        return generated_workout

    def __get_selected_body_parts(self):
        curr_bp_array = []
        [curr_bp_array.append(bp.cget("text")) for bp in self.body_parts_bnt_arr if bp.cget("fg_color") == colors.ORANGE_COLOR]

        if len(curr_bp_array) < 1: raise Exception(exception.BODY_PARTS_NOT_SELECTED)

        return curr_bp_array

    def __load_body_parts_frame(self):
        self.body_parts_frame = customtkinter.CTkFrame(
            master=self.background,
            corner_radius=20,
            border_color=colors.ORANGE_COLOR,
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
            font=(fonts.Hoefler, 25)
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
                    hover_color=colors.ORANGE_COLOR,
                    text_color="black",
                    fg_color='gray',
                    font=(fonts.Hoefler, 15),
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
            border_color=colors.ORANGE_COLOR,
            border_width=2
        )
        self.workout_difficulty_frame.place(x=30, y=390, relwidth=0.9, relheight=0.15)

        # Create the grid
        self.workout_difficulty_frame.columnconfigure((0, 1, 2), weight=1, uniform='a')
        # self.workout_difficulty_frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        difficulty_img = ImageTk.PhotoImage(Image.open("images/speedometer1.png").resize((40, 40)))

        # Difficulty Label
        difficulty_label = customtkinter.CTkLabel(
            master=self.workout_difficulty_frame, text="Workout Difficulty", font=(fonts.Hoefler, 25),
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
        self.difficulty_state = customtkinter.IntVar(value=1)
        # Beginner
        self.difficulty_beginner = customtkinter.CTkRadioButton(
            master=self.workout_difficulty_frame,
            text="Beginner",
            font=(fonts.Hoefler, 20),
            text_color="#2BC4E9",
            hover_color="#2BC4E9",
            fg_color="white",
            variable=self.difficulty_state,
            value=1,
            command=lambda: self.__change_difficulty_button_states("Beginner")
        )
        self.difficulty_beginner.grid(row=1, column=0, padx=10)

        # Intermediate
        self.difficulty_intermediate = customtkinter.CTkRadioButton(
            master=self.workout_difficulty_frame,
            text="Intermediate",
            font=(fonts.Hoefler, 20),
            text_color=colors.GRAY_COLOR,
            hover_color="#fb4f1b",
            fg_color="white",
            variable=self.difficulty_state,
            value=2,
            command=lambda: self.__change_difficulty_button_states("Intermediate")
        )
        self.difficulty_intermediate.grid(row=1, column=1, padx=10)

        # Advanced
        self.difficulty_advanced = customtkinter.CTkRadioButton(
            master=self.workout_difficulty_frame,
            text="Advanced",
            font=(fonts.Hoefler, 20),
            text_color=colors.GRAY_COLOR,
            hover_color="#d52522",
            fg_color="white",
            variable=self.difficulty_state,
            value=3,
            command=lambda: self.__change_difficulty_button_states("Advanced")
        )
        self.difficulty_advanced.grid(row=1, column=2, padx=10)

    def __change_btn_state(self, btn_index):
        curr_btn = self.body_parts_bnt_arr[btn_index]
        curr_btn_color = curr_btn.cget("fg_color")
        new_color = ""
        if curr_btn_color == colors.ORANGE_COLOR: new_color = colors.GRAY_COLOR
        else: new_color = colors.ORANGE_COLOR

        curr_btn.configure(fg_color=new_color)

    def __change_difficulty_button_states(self, selected_state):
        beginner = ""
        intermediate = ""
        advanced = ""
        if selected_state == "Beginner":
            beginner = "#2BC4E9"
            intermediate = colors.GRAY_COLOR
            advanced = colors.GRAY_COLOR
        elif selected_state == "Intermediate":
            beginner = colors.GRAY_COLOR
            intermediate = "#fb4f1b"
            advanced = colors.GRAY_COLOR
        else:
            beginner = colors.GRAY_COLOR
            intermediate = colors.GRAY_COLOR
            advanced = "#d52522"

        self.difficulty_beginner.configure(text_color=beginner)
        self.difficulty_intermediate.configure(text_color=intermediate)
        self.difficulty_advanced.configure(text_color=advanced)
