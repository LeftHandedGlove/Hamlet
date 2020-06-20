import mysql.connector
import atexit
import yaml
import time
import os


class MySQLDatabaseConnection:
    def __init__(self, address, username, password, database):
        self.__connection = None
        self.__address = address
        self.__username = username
        self.__password = password
        self.__database = database
        self.cursor = None

    def open_connection(self):
        print("Opening connection to database...")
        print("  Database: {0}".format(self.__database))
        print("  Address:  {0}".format(self.__address))
        print("  User:     {0}".format(self.__username))
        print("  Password: {0}".format(self.__password))
        self.__connection = mysql.connector.connect(
            host=self.__address,
            user=self.__username,
            password=self.__password,
            database=self.__database
        )
        self.cursor = self.__connection.cursor()
        atexit.register(self.close_connection)

    def close_connection(self):
        print("Closing connection to database")
        self.__connection.close()
        self.__connection = None
        self.cursor = None
        atexit.unregister(self.close_connection)


class DatabaseManager:
    def __init__(self, database_config_path, check_interval=1):
        self.__db_config_path = database_config_path
        self.__check_interval = check_interval
        self.__running = False

    def start(self):
        print("Starting Database Manager")
        self.__import_database_config()
        self.__db_connection = MySQLDatabaseConnection(
            self.__db_address, 
            self.__db_user, 
            self.__db_password, 
            self.__db_name)
        self.__db_connection.open_connection()
        self.__setup_database()
        self.__running = True
        self.run_constantly()
        atexit.register(self.stop)

    def stop(self):
        print("Stopping Database Manager")
        self.__running = False
        self.__db_connection.close_connection()
        atexit.unregister(self.stop)

    def run_once(self):
        self.__remove_old_data()

    def run_constantly(self):
        # Run the main function until told to stop
        while(self.__running):
            self.run_once()

    def __import_database_config(self):
        print("Loading Database Config: {0}".format(self.__db_config_path))
        # Parse the database config file
        with open(self.__db_config_path) as yaml_file:
            db_config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            print(db_config_data)
        # Extract the database info
        self.__db_name = db_config_data['name']
        self.__db_address = db_config_data['address']
        self.__db_user = db_config_data['user']
        self.__db_password = db_config_data['password']
        self.__db_tables = db_config_data['tables']

    def __setup_database(self):
        print("Setting up database: {0}".format(self.__db_name))
        # Iterate over all of the tables
        for table in self.__db_tables.keys():
            # Make sure the table exists
            self.__db_connection.cursor.execute("SHOW TABLES LIKE '{0}'".format(table))
            all_results = self.__db_connection.cursor.fetchall()
            if len(all_results) == 0:
                print("Unable to find table '{0}', creating it".format(table))
                create_table_sql = "CREATE TABLE {0}(".format(table)
                for col_name, col_config in self.__db_tables[table]['columns'].items():
                    create_table_sql += "{0} {1},".format(col_name, col_config)
                create_table_sql = create_table_sql[:-1] + ")"
                self.__db_connection.cursor.execute(create_table_sql)
    
    def __remove_old_data(self):
        pass

    def __update_services_data(self):
        pass



if __name__ == "__main__":
    database_manager = DatabaseManager(os.path.abspath('database_outline.yaml'))
    database_manager.start()
    
    
