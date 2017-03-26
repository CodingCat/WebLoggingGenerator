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

    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(10)

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(
            target=client_handler,
            args=(client_socket,)
        )
        client_thread.start()


def run_command(cmd):
    command = cmd.rstrip()

    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True
        )
    except:
        output = 'Failed to execute command\r\n'

    return output


def client_handler(client_socket):
    try:
        while True:
            client_socket.send('Hello World Hello World')
    except:
        client_socket.send('Failed')


def main():
    global listen, port, target

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu:', [
            'help', 'listen', 'target', 'port'
        ])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, 'Unhandled Option'

    if listen:
        server_loop()

main()

"""
echo -ne 'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n' | python netcat.py -t www.google.com -p 80
also
python netcat.py -l -p 9999 -c        # first  terminal
python netcat.py -t localhost -p 9999 # second terminal
"""
