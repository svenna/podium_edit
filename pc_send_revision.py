import zmq
import sys
import ConfigParser

config_file = "podium_pc_autoupdate.ini"

if __name__ == '__main__':
        conf = ConfigParser.ConfigParser()
        conf.read(config_file)
        address = conf.get("address", "server")
        port = conf.get("address", "port")
        repos, rev = sys.argv[1:]
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://%s:%s" % (address, port))
        socket.send_unicode("%s:%s" % (repos, rev))
        socket.close()
        context.destroy()
        sys.exit(0)
