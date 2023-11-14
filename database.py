import sqlite3
import exception

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
        self.cursor.execute("SELECT * FROM users as u WHERE u.username == :username", {'username': username})
        result = self.cursor.fetchone()
        if result is None:
            raise Exception(exception.NO_USER_FOUND)
        # TODO: first check if user exists
        # TODO: second check if password is same
        # TODO: return TRUE if both checks pass, otherwise FALSE
    # # Create table
    # # === USERS === #
    # cursor.execute("""
    #     CREATE TABLE users(
    #         id integer primary key autoincrement,
    #         first_name text,
    #         last_name text,
    #         username text,
    #         password text
    #     )
    # """)