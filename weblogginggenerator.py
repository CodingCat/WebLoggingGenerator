# pylint: disable-all
# flake8: noqa

import sys
import socket
import getopt
import threading
import subprocess
import random

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

def compose_log_entry():
    last_digit = random.randint(1, 254)
    ip = '10.0.0.%d' % last_digit
    actions = ['GET', 'POST']
    action_index = random.randint(0, 1)
    urls = ['index.html', 'about.html', 'product.html']
    url_index = random.randint(0, 1)
    user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)']
    user_agent_index = random.randint(0, 2)
    s = '%s %s %s %s' % (ip, actions[action_index], urls[url_index], user_agents[user_agent_index])
    print('generate %s' % s)
    return s


def client_handler(client_socket):
    try:
        while True:
            print("send")
            client_socket.send(compose_log_entry())
            print("sent")
            #time.sleep(5)
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
