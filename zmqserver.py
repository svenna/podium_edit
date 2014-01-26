import zmq
import sys


def main(address, port, transport="tcp://"):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("%s%s:%s" % (transport, address, port))

        while True:
                msg = socket.recv()
                print "Got ", msg
                socket.send(msg)
                

if __name__ == '__main__':
        main("127.0.0.1", "5000")
