import sys

address = "localhost"
port = 9000


def connect(address, port):
    pass

def send_data(repos, rev):
    pass

def main(repos, rev, address, port):
    connect(address, port)
    send_data(repos, rev)


if __name__ == '__main__':
    repos = sys.argv[1]
    rev = sys.argv[2]
    main(repos, rev, address, port)
