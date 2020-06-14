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
        self.__cursor = None

    def open_connection(self):
        self.__connection = mysql.connector.connect(
            host=self.__address,
            user=self.__username,
            password=self.__password,
            database=self.__database
        )
        self.__cursor = self.__connection.cursor()
        atexit.register(self.close_connection)

    def close_connection(self):
        self.__connection.close()
        self.__connection = None
        self.__cursor = None
        atexit.unregister(self.close_connection)


class SystemStateMonitorDB(HamletMySQLDataBase):
    def __init__(self):
        super(SystemStateMonitorDB, self).__init__("localhost", "hamlet", "hamlet", "system_state")

    def add_system_to_database_tables(self):
        self.__cursor.execute()

    def update_table(self, table, columns, values):
        pass
        # Construct the query string
        query = ""






