import mysql.connector
import atexit
import yaml


class HamletMySQLDataBase:
    def __init__(self, address, username, password, database):
        self.__connection = None
        self.__address = address
        self.__username = username
        self.__password = password
        self.__database = database
        self.cursor = None

    def open_connection(self):
        self.__connection = mysql.connector.connect(
            host=self.__address,
            user=self.__username,
            password=self.__password,
            database=self.__database
        )
        self.cursor = self.__connection.cursor()
        atexit.register(self.close_connection)

    def close_connection(self):
        self.__connection.close()
        self.__connection = None
        self.cursor = None
        atexit.unregister(self.close_connection)


def import_database_config():
    with open('database_outline.yaml') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        print(data)
    return data


def setup_database(database_config):
    pass
    # Iterate through each expected table
        # If the table exists then alter it to the new expected configuration
        # If the table doesn't exist then create it


if __name__ == "__main__":
    database_config = import_database_config()
    setup_database(database_config)
    
