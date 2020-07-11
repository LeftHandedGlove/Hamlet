import zmq

def consumer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PULL)
    zmq_socket.bind('tcp://127.0.0.1:19700')
    while True:
        received_string = zmq_socket.recv_string()
        print(received_string)

consumer()