class User():

    def __init__(self, id, first_name, last_name, username, password):
        self.__id = id,
        self.__first_name = first_name,
        self.__last_name = last_name,
        self.__username = username,
        self.__password = password

    def get_id(self):
        return self.__id[0]

    def get_name(self):
        return f"{self.__first_name[0]} {self.__last_name[0]}"

    def get_username(self):
        return self.__username[0]

