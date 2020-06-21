import mysql.connector
import atexit
import yaml
import time
import os
import subprocess


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

    def command(self, sql_query):
        self.cursor.execute(sql_query)
        try:
            result = self.cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            # The command didn't return any data
            result = None
        return result

    def create_table(self, table_name, column_config_dict):
        create_table_sql = "CREATE TABLE {0}(".format(table_name)
        for col_name, col_sql_str in column_config_dict.items():
            create_table_sql += "{0} {1},".format(col_name, col_sql_str)
        create_table_sql = create_table_sql[:-1] + ")"
        self.cursor.execute(create_table_sql)

    def drop_table(self, table_name):
        self.cursor.execute("DROP TABLE {0}".format(table_name))


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
        self.__run_constantly()
        atexit.register(self.stop)

    def stop(self):
        print("Stopping Database Manager")
        self.__running = False
        self.__db_connection.close_connection()
        atexit.unregister(self.stop)

    def __run_once(self):
        self.remove_old_data()

    def __run_constantly(self):
        print("Entering main loop")
        # Run the main function until told to stop
        try:
            while(self.__running):
                self.__run_once()
        except KeyboardInterrupt:
            print("Interrupted by keyboard.")
            self.stop()
        except Exception as e:
            print("Something unexpected happened!")
            print(e)
            raise e

    def __import_database_config(self):
        print("Loading Database Config: {0}".format(self.__db_config_path))
        # Parse the database config file
        with open(self.__db_config_path) as yaml_file:
            db_config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
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
            all_results = self.__db_connection.command("SHOW TABLES LIKE '{0}'".format(table))
            if len(all_results) == 0:
                # If the table doesn't exist then create it
                print("Unable to find '{0}' table, creating it".format(table))
                self.__db_connection.create_table(table, self.__db_tables[table]['columns'])
            else:
                # If the table does exist then verify it has the right columns, 
                # if it doesn't then drop the table and recreate it.
                expected_columns = list(self.__db_tables[table]['columns'].keys())
                should_recreate_table = False
                all_results = self.__db_connection.command(
                    "SELECT column_name FROM information_schema.columns " +
                    "WHERE table_schema='{0}' AND table_name='{1}'".format(
                        self.__db_name, table))
                # Iterate over each result and remove it from the expected tables list
                for results_row in all_results:
                    col_name = results_row[0]
                    if col_name in expected_columns:
                        expected_columns.remove(col_name)
                    else:
                        # If a column exists that wasn't expected then recreate the table
                        print("Unexpected column '{0}' found in '{1}' table!".format(col_name, table))
                        should_recreate_table = True
                if len(expected_columns) != 0:
                    # If a column wasn't in the results then recreate the table
                    print("Not enough columns found in '{0}' table!".format(table))
                    should_recreate_table = True
                if should_recreate_table:
                    print("Dropping and recreating '{0}' table".format(table))
                    self.__db_connection.drop_table(table)
                    self.__db_connection.create_table(table, self.__db_tables[table]['columns'])
                else:
                    print("The '{0}' table seems to be okay".format(table))

    def remove_old_data(self):
        for table in self.__db_tables:
            data_lifetime = self.__db_tables[table]['data_lifetime']
            if data_lifetime is not None:
                self.__db_connection.command("DELETE FROM {0} WHERE timestamp < (NOW() - INTERVAL {1})".format(table, data_lifetime))

    
if __name__ == "__main__":
    database_manager = DatabaseManager(os.path.abspath('database_outline.yaml'))
    database_manager.start()
    
    
