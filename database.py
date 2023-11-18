import sqlite3
import exception
from datetime import datetime
from exercise import Exercise
from body_part import BodyPart
from target_muscle import TargetMuscle


class Database:
    def __init__(self, database_name):
        self.__database_name = database_name

    def __connect(self):
        # TODO: VALIDATION
        self.db = sqlite3.connect(self.__database_name)
        self.cursor = self.db.cursor()
        # return self.cursor

    def __commit(self):
        # Commit changes
        self.db.commit()
        # Close connection
        self.db.close()

    def add_user(self, first_name, last_name, username, password):
        # TODO: VALIDATE FOR SAME USERNAME
        self.__connect()
        self.cursor.execute("""
            INSERT INTO users VALUES (:id, :first_name, :last_name, :username, :password)
        """,
            {
                'id': None,
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'password': password
            }
        )
        self.__commit()

    def get_user(self, username, password):
        self.__connect()
        self.cursor.execute("SELECT * FROM users AS u WHERE u.username == :username", {'username': username})
        result = self.cursor.fetchone()
        # If no user found
        if result is None: raise Exception(exception.USER_OR_PASSWORD_WRONG)
        # If password is wrong
        if result[4] != password: raise Exception(exception.USER_OR_PASSWORD_WRONG)

        return True

    def get_all_body_parts(self):
        self.__connect()
        self.cursor.execute("SELECT * FROM body_parts")
        result = self.cursor.fetchall()
        # If no user found
        if result is None: raise Exception(exception.BODY_PARTS_TABLE_EMPTY)

        return result
    def add_exercise(self, exercise):
        self.cursor.execute(
            """
                INSERT INTO exercises VALUES(:id, :body_part_id, :gif_url, :name, :target_id, :secondary_muscles, :instructions)
            """,
            {
                'id': None,
                'body_part_id': exercise.body_part_id,
                'gif_url': exercise.gif_url,
                'name': exercise.name,
                'target_id': exercise.target_id,
                'secondary_muscles': exercise.secondary_muscles,
                'instructions': exercise.instructions
            }
        )

    def __add_body_part(self, body_part):
        self.cursor.execute(
            """
                INSERT INTO body_parts VALUES(:id, :name)
            """,
            {
                'id': None,
                'name': body_part.name,
            }
        )

    def __add_target_muscle(self, target_muscle):
        self.cursor.execute(
            """
                INSERT INTO target_muscles VALUES(:id, :name)
            """,
            {
                'id': None,
                'name': target_muscle.name,
            }
        )

    def get_user_workouts_for_current_month(self, user_id):
        self.__connect()
        self.cursor.execute("SELECT * FROM users_workouts AS uw WHERE uw.user_id == :user_id", {'user_id': user_id})
        result = self.cursor.fetchall()

        # If user has no workouts for this month
        if result is None: raise Exception(exception.USER_HAS_NO_WORKOUTS)

        return result

    def get_user_day_workout(self, user_id, day_date):
        self.__connect()
        self.cursor.execute("SELECT * FROM users_workouts AS uw WHERE uw.user_id == :user_id", {'user_id': user_id})
        result = self.cursor.fetchall()

        # TODO: It is not needed to create validation if missing,
        #  otherwise we will not have button active in the calendar
        for workout in result:
            curr_date = self.__parse_string_to_date(workout[2]).day

            if curr_date == day_date: return workout

        return None

    def __parse_string_to_date(self, date):
        format = '%Y-%m-%d'
        return datetime.strptime(date, format).date()

    def get_exercise_name_by_id(self, id):
        self.__connect()
        self.cursor.execute("SELECT e.name FROM exercises AS e WHERE e.id == :exercise_id", {'exercise_id': id})
        result = self.cursor.fetchone()[0]

        return result

    def get_body_part_id_by_name(self, name):
        self.__connect()
        self.cursor.execute("SELECT bp.id FROM body_parts AS bp WHERE bp.name == :name", {'name': name})
        result = self.cursor.fetchone()[0]

        return result

    def get_exercises_by_body_parts_and_difficulty(self, body_parts, difficulty):
        body_parts_ids = []
        [body_parts_ids.append(self.get_body_part_id_by_name(bp_name)) for bp_name in body_parts]

        test = body_parts.join[]

        self.__connect()
        self.cursor.execute("SELECT e.id, e.name "
                            "FROM exercises AS e "
                            "WHERE e.body_part_id IN (:body_parts_arr) AND "
                            "e.difficulty == :difficulty", {'body_parts_arr': body_parts_ids, 'difficulty': difficulty})
        result = self.cursor.fetchall()
        [print(i) for i in result]
