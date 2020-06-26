# As this is the entry point for the script the system path should 
# include this so imports are relative to this file's parent directory
import sys
import os
if getattr(sys, 'frozen', False):
    sys.path.append(os.path.dirname(sys.executable))
else:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import atexit
import yaml

from hamlet_common.mysql_database_connection import MySQLDatabaseConnection
from hamlet_common.python_utils import print_msg

from sensors.cpu_temp_sensor import CPUTemperatureSensor

class SensorsMonitor:
    def __init__(self):
        self.__db_conn = None
        self.__sensors = [
            CPUTemperatureSensor()
        ]

    def start(self):
        print_msg("Starting Sensors Monitor")
        atexit.register(self.stop)
        self.__db_conn = MySQLDatabaseConnection()
        self.__db_conn.open_connection()
        # Drop and recreate sensor database table
        self.__db_conn.drop_table('sensors')
        self.__db_conn.create_table('sensors')
        # Fill table with default sensor values
        print_msg("Adding sensor entries to sensors table")
        for sensor in self.__sensors:
            for attribute in sensor.sensor_data.keys():
                print_msg("  Adding '{0}'".format(attribute))
                sql_query = ("INSERT INTO sensors (attribute) "
                             "VALUES ('{0}')"
                             .format(attribute))
                self.__db_conn.command(sql_query)
        self.__run_continuously()

    def stop(self):
        print_msg("Stopping Sensors Monitor")
        atexit.unregister(self.stop)
        self.__db_conn.close_connection()

    def __run_once(self):
        for sensor in self.__sensors:
            sensor.update_sensor_data()
            for attribute, value in sensor.sensor_data.items():
                sql_query = ("UPDATE sensors "
                             "SET value = {0}, state = '{1}' "
                             "WHERE attribute = '{2}'"
                             .format(value, sensor.state, attribute))
                self.__db_conn.command(sql_query)

    def __run_continuously(self):
        try:
            print_msg("Entering main loop")
            while True:
                self.__run_once()
        except KeyboardInterrupt:
            print_msg("Interrupted by keyboard")
        except Exception as e:
            print_msg("Something went wrong while running!")
            print_msg(e)
            self.stop()
            raise e


if __name__ == "__main__":
    sensors_monitor = SensorsMonitor()
    sensors_monitor.start()
