import subprocess

from base_sensor import BaseSensor


class CPUTemperatureSensor(BaseSensor):
    def __init__(self):
        self.name = "CPU Temperature"
        self.sensor_data = {
            "CPU Temperature (C)": 00.0
        }
        self.read_timeout_ms = 100

    def read_sensor_data(self):
        result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        raw_output = result.stdout
        cpu_temp = raw_output.replace('temp=', '').replace('\'C', '')
        self.sensor_data['cpu_temp'] = float(cpu_temp)
