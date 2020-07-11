import zmq
import time

def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect('tcp://localhost:19700')
    count = 0
    while True:
        zmq_socket.send_string("String num: {0}".format(count))
        count += 1
        time.sleep(1)