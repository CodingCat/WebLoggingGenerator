# pylint: disable-all
# flake8: noqa

import sys
import socket
import getopt
import threading
import subprocess

target = ''
port = 0

def usage():
    print '''
        netcat.py -t <host> -p <port>
        -l, --listen                (listen on specified host/port)
        -u, --upload=<destination>  (upload file upon connection)
    '''

def server_loop():
    global target

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    print('listen on %s:%s' % (target, port))
    server.listen(10)

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(
            target=client_handler,
            args=(client_socket,)
        )
        client_thread.start()

def client_handler(client_socket):
    try:
        while True:
            print("send")
            client_socket.send('Hello World Hello World\n')
            time.sleep(5)
    except:
        client_socket.send('Failed')


def main():
    global port, target

    args = (sys.argv[1:])
    target = args[0]
    port = int(args[1])

    server_loop()

main()

"""
echo -ne 'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n' | python netcat.py -t www.google.com -p 80
also
python netcat.py -l -p 9999 -c        # first  terminal
python netcat.py -t localhost -p 9999 # second terminal
"""
