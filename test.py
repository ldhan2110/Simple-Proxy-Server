import os
import sys
import threading
import socket

BACKLOG = 50
MAX_DATA_RECV = 999999
BLOCKED = []
BLOCKED_MESSAGE = ""

def main():
    Load_BLOCKED()
    print(BLOCKED)

    print ("Proxy Server is running on local host  : 8888")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", 8888))
    server.listen(BACKLOG)
    while 1:
        connect, client_addr = server.accept()
        threading._start_new_thread(proxy_thread_handle,(connect,client_addr))
    server.close()


def Load_BLOCKED():
        f = open('blacklist.conf','r')
        while 1:
            domain = f.readline()
            BLOCKED.append(domain)
            if not domain:
                break
        f.close()


def proxy_thread_handle(connect, client_addr):

    #xu ly URL
    request = connect.recv(MAX_DATA_RECV)
    request = str(request,'utf-8','ignore')         #chuyen ve string  de xu ly
    first_line = request.split('\n')[0]
    url = first_line.split(' ')[1]
    print(url)
    http_pos = url.find("://")
    if (http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]                 #lay link URL

    port_pos = temp.find(":")                       #tim vi tri port


    web_server_pos = temp.find("/")                 #tim domain cua web server
    if web_server_pos == -1:
        web_server_pos = len(temp)

    web_server = ""
    port = -1
    if (port_pos == -1 or web_server_pos < port_pos):  # default port
        port = 80
        web_server = temp[:web_server_pos]
    else:
        port = int((temp[(port_pos + 1):])[:web_server_pos - port_pos - 1])
        web_server = temp[:port_pos]

    if (web_server in BLOCKED):
        f = open('403.html','r')
        BLOCKED_MESSAGE = f.read()
        connect.sendall(BLOCKED_MESSAGE.encode('utf-8'))
        connect.close
        f.close()
        return

    request = bytearray(request,'utf-8')

    sub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sub.connect((web_server, port))
    sub.send(request)

    while 1:
        data = sub.recv(MAX_DATA_RECV)
        if (len(data) > 0):
            connect.send(data)
        else:
            break
    sub.close()
    connect.close()





if __name__ == '__main__':
    main()