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
import multiprocessing
import time

from hamlet_common.mysql_database_connection import MySQLDatabaseConnection
from hamlet_common.python_utils import print_msg
from sensors.cpu_temp_sensor import CPUTemperatureSensor
from sensors.cpu_utilization_sensor import CPUUtilizationSensor

class SensorsMonitor:
    def __init__(self):
        self.__db_conn = None
        self.__table_name = 'sensors'
        self.__error_queue = multiprocessing.Queue()
        self.__data_queue = multiprocessing.Queue()
        self.__sensors = [
            CPUTemperatureSensor(
                poll_rate_hz=5, 
                monitor_error_queue=self.__error_queue, 
                db_table=self.__table_name, 
                monitor_index=0
            ),
            CPUUtilizationSensor(
                poll_rate_hz=5, 
                monitor_error_queue=self.__error_queue, 
                db_table=self.__table_name, 
                monitor_index=1
            )
        ]

    def start(self):
        print_msg("Starting Sensors Monitor")
        atexit.register(self.stop)
        self.__db_conn = MySQLDatabaseConnection()
        self.__db_conn.open_connection()
        # Drop and recreate sensor database table
        self.__db_conn.drop_table(self.__table_name)
        self.__db_conn.create_table(self.__table_name)
        # Fill table with default sensor values
        print_msg("Adding sensor entries to sensors table")
        for sensor in self.__sensors:
            for attribute in sensor.sensor_data.keys():
                print_msg("  Adding '{0}'".format(attribute))
                sql_query = ("INSERT INTO sensors (attribute) "
                             "VALUES ('{0}')"
                             .format(attribute))
                self.__db_conn.command(sql_query)
        # Start all of the sensor processes
        for sensor in self.__sensors:
            sensor.start()
        self.__run_continuously()

    def stop(self):
        print_msg("Stopping Sensors Monitor")
        atexit.unregister(self.stop)
        self.__db_conn.close_connection()

    def __run_once(self):
        # Wait until a service fails
        failed_process_index, failed_process_poll_rate = self.__error_queue.get(block=True)
        # Get the sensor class so it can be recreated
        failed_process_class = type(self.__sensors[failed_process_index])
        # Recreate the sensor process
        self.__sensors[failed_process_index] = failed_process_class(
            poll_rate_hz=failed_process_poll_rate, 
            db_table=self.__table_name, 
            monitor_error_queue=self.__error_queue, 
            monitor_index=failed_process_index
        )
        self.__sensors[failed_process_index].start()
        
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
