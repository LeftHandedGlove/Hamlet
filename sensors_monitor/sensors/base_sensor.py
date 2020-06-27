import multiprocessing
import time
import traceback

from hamlet_common.python_utils import print_msg                                # pylint: disable=import-error
from hamlet_common.mysql_database_connection import MySQLDatabaseConnection     # pylint: disable=import-error

class BaseSensor(multiprocessing.Process):
    unknown = 'UNKNOWN'
    operational = 'OPERATIONAL'
    failed = 'FAILED'

    def __init__(self, poll_rate_hz, db_table, monitor_error_queue, monitor_index):
        super(BaseSensor, self).__init__()
        # Variables set by inheriting classes
        self._name = ""
        self._sensor_data = dict()
        
        self.__state = self.unknown
        self.__poll_rate_hz = poll_rate_hz
        self.__poll_time_s = 1 / poll_rate_hz
        self.__db_table = db_table
        self.__monitor_error_queue = monitor_error_queue
        self.__monitor_index = monitor_index
        self.__db_conn = MySQLDatabaseConnection()

    def run(self):
        # Connect to the database
        self.__db_conn.open_connection()
        # Loop forever getting data
        try:
            while True:
                # Get the start time for consistant sleeping
                start_time = time.time()
                # Start the separate sensor reader process which is required for timeouts
                reader_data_queue = multiprocessing.Queue()
                sensor_reader_process = multiprocessing.Process(target=self.read_sensor_data, args=(reader_data_queue,))
                sensor_reader_process.start()
                sensor_reader_process.join(timeout=self.__poll_time_s)
                sensor_reader_process.terminate()
                # Interpret what happened inside the process
                if sensor_reader_process.exitcode is None:
                    print_msg("{0} timed out when getting data!".format(self.name))
                    self.state = "FAILED"
                elif sensor_reader_process.exitcode != 0:
                    print_msg("Something went wrong when getting {0} sensor data!".format(self.name))
                    self.state = "FAILED"
                else:
                    self.state = "OPERATIONAL"
                    read_sensor_data = reader_data_queue.get(block=False)
                    for attribute, value in read_sensor_data.items():
                        self._sensor_data[attribute] = value
                # Report the data
                for attribute, value in self._sensor_data.items():
                    sql_query = ("UPDATE {table} "
                                 "SET value = {val}, state = '{state}' "
                                 "WHERE attribute = '{attr}'"
                                 .format(table=self.__db_table, val=value, state=self.state, attr=attribute))
                    self.__db_conn.command(sql_query)
                # Determine how much time to sleep
                loop_time_s = time.time() - start_time
                if  loop_time_s < self.__poll_time_s:
                    time.sleep(self.__poll_time_s - loop_time_s)
                else:
                    print_msg("The {0} sensor process is falling behind!".format(self.name))
        except Exception as e:
            traceback.print_exc()
            print_msg(e)
            print_msg("The {0} sensor process has crashed!".format(self.name))
            queue_data = (self.__monitor_index, self.__poll_rate_hz)
            self.__monitor_error_queue.put(queue_data, block=False)
        
        
    def read_sensor_data(self, mp_value):
        raise NotImplementedError

