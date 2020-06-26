import multiprocessing
from hamlet_common.python_utils import print_msg

class BaseSensor:
    unknown = 'UNKNOWN'
    operational = 'OPERATIONAL'
    failed = 'FAILED'

    def __init__(self):
        self.name = ""
        self.state = self.unknown
        self.sensor_data = dict()
        self.read_timeout_ms = 250

    def update_sensor_data(self):
        timeout_process = multiprocessing.Process(target=self.read_sensor_data)
        timeout_process.start()
        timeout_process.join(timeout=(self.read_timeout_ms / 1000))
        timeout_process.terminate()
        if timeout_process.exitcode is None:
            print_msg("Sensor '{0}' timed out after {1} ms!".format(self.name, self.read_timeout_ms))
            self.state = self.failed
        elif timeout_process.exitcode != 0:
            print_msg("Something went wrong when getting '{0}' data!".format(self.name))
            self.state = self.failed
        else:
            self.state = self.operational

    def read_sensor_data(self):
        raise NotImplementedError

