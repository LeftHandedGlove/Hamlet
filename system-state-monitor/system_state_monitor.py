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


class SystemStateMonitorDB(HamletMySQLDataBase):
    def __init__(self):
        super(SystemStateMonitorDB, self).__init__("localhost", "hamlet", "hamlet", "system_state")
        self.__expected_system_tables = {
            "temperature": "cpu_temp"
        }

    def add_system_to_database_tables(self):
        # Get all the tables in the system_state database
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'system_state'")
        all_tables_sql_results = self.cursor.fetchall()
        # Create a list of tables to create by removing the existing ones from the expected ones
        tables_to_create = self.__expected_system_tables.copy()
        for row_results in all_tables_sql_results:
            table_name = row_results[0]
            tables_to_create.remove(table_name)
        # Create tables that need to be created
        for table in tables_to_create:


        

    def update_table(self, table, columns, values):
        pass
        # Construct the query string
        query = ""


if __name__ == "__main__":
    sys_state_db = SystemStateMonitorDB()
    sys_state_db.open_connection()
    sys_state_db.add_system_to_database_tables()
