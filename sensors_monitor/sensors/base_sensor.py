import multiprocessing
import ctypes

from hamlet_common.python_utils import print_msg    # pylint: disable=import-error

class BaseSensor(multiprocessing.Process):
    unknown = 'UNKNOWN'
    operational = 'OPERATIONAL'
    failed = 'FAILED'

    def __init__(self, poll_rate_ms, read_timeout_ms, error_queue, data_queue):
        super(BaseSensor, self).__init__()
        self.name = ""
        self.state = self.unknown
        self.__poll_rate_ms = poll_rate_ms
        self.__read_timeout_ms = read_timeout_ms
        self.__error_queue = error_queue
        self.__monitor_data_queue = data_queue

    def run(self):
        try:
            while True:
                reader_data_value = multiprocessing.Value(ctypes.c_float, 0.0)
                sensor_reader_process = multiprocessing.Process(target=self.read_sensor_data, args=(reader_data_value,))
                sensor_reader_process.start()
                sensor_reader_process.join(timeout=(self.__read_timeout_ms / 1000))
                sensor_reader_process.terminate()
                if sensor_reader_process.exitcode is None:
                    print_msg("Sensor '{0}' timed out after {1} ms!".format(self.name, self.__read_timeout_ms))
                    state = self.failed
                elif sensor_reader_process.exitcode != 0:
                    print_msg("Something went wrong when getting '{0}' data!".format(self.name))
                    state = self.failed
                else:
                    value = reader_data_value.value
                    state = self.operational
                
                self.__monitor_data_queue.put()
        except Exception as e:
            pass


        timeout_process = multiprocessing.Process(target=self.read_sensor_data)
        
        

    def read_sensor_data(self, mp_value):
        raise NotImplementedError

