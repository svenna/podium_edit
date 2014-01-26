import zmq
import sys
import os


def main(address, port, transport="tcp://"):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("%s%s:%s" % (transport, address, port))

        for i in range(10):
                msg = "msg %s" % i
                socket.send(msg)
                print "Sending ", msg
                msg_in = socket.recv()

if __name__ == '__main__':
        main("127.0.0.1", "5000")
