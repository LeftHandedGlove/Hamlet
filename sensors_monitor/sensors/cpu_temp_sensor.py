import subprocess

# pylint: disable=import-error
from sensors.base_sensor import BaseSensor 
# pylint: enable=import-error


class CPUTemperatureSensor(BaseSensor):
    def __init__(self, poll_rate_hz, db_table, monitor_error_queue, monitor_index):
        super(CPUTemperatureSensor, self).__init__(poll_rate_hz, db_table, monitor_error_queue, monitor_index)
        self._name = 'CPU Temperature C'
        self.sensor_data = {
            'CPU Temperature C': 0.0
        }

    def read_sensor_data(self, data_queue):
        # Read from the CPU thermal zone file 
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
            raw_temp = str(temp_file.readline)
        raw_temp = raw_temp.strip()
        # Convert from milli-C into C
        cpu_temp = float(raw_temp) / 1000
        self.sensor_data['CPU Temperature C'] = cpu_temp
        # Send the data back to the parent process
        data_queue.put(self.sensor_data, block=False)

