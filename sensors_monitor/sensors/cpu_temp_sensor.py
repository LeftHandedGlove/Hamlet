import subprocess
import multiprocessing
import time
import traceback

from hamlet_common.python_utils import print_msg                                # pylint: disable=import-error
from hamlet_common.mysql_database_connection import MySQLDatabaseConnection     # pylint: disable=import-error

from base_sensor import BaseSensor


class CPUTemperatureSensor(BaseSensor):
    def __init__(self, poll_rate_hz, db_table, monitor_error_queue, monitor_index):
        super(CPUTemperatureSensor, self).__init__(poll_rate_hz, db_table, monitor_error_queue, monitor_index)
        self._name = 'CPU Temperature C'
        self._sensor_data = {
            'CPU Temperature C': 00.0
        }

    def read_sensor_data(self, data_queue):
        result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE, text=True)
        raw_output = result.stdout
        cpu_temp = raw_output.replace('temp=', '').replace('\'C', '').strip()
        self._sensor_data['CPU Temperature C'] = float(cpu_temp)
        data_queue.put(self._sensor_data, block=False)

