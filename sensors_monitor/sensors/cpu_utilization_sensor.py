import subprocess
import re

# pylint: disable=import-error
from sensors.base_sensor import BaseSensor 
# pylint: enable=import-error


class CPUUtilizationSensor(BaseSensor):
    def __init__(self, poll_rate_hz, db_table, monitor_error_queue, monitor_index):
        super(CPUUtilizationSensor, self).__init__(poll_rate_hz, db_table, monitor_error_queue, monitor_index)
        self._name = 'CPU Utilization'
        self.sensor_data = {
            'CPU Utilization': 0.0
        }
    def read_sensor_data(self, data_queue):
        # Run top to get CPU data
        result = subprocess.run(["top", "-n", "1"], stdout=subprocess.PIPE, text=True)
        raw_output = result.stdout
        # Extract only the idle data
        match = re.search(r' (?P<idle>\d+\.\d) id, ', raw_output)
        idle_cpu = float(match.group('idle'))
        # Convert from idle to utilized
        utilized_cpu = 100 - idle_cpu
        self.sensor_data['CPU Utilization'] = utilized_cpu
        # Send the data back to the parent process
        data_queue.put(self.sensor_data, block=False)

