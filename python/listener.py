#!/usr/bin/env python3

import os
import socket
import sys


def main():
    if len(sys.argv) < 3:
        print("usage: {} <ip> <port>".format(sys.argv[0]))
        sys.exit(1)
    elif os.geteuid() != 0:
        print("{}: must be run as root".format(sys.argv[0]))
        sys.exit(1)

    c2ip = sys.argv[1]
    c2port = int(sys.argv[2])
    if c2port <= 0:
        print("{}: invalid port '{}'".format(sys.argv[0], sys.argv[2]))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((c2ip, c2port))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        msg = conn.recv(64)
        print(msg)
        conn.send(b'listener: hello\n')
        conn.close()


if __name__ == '__main__':
    main()

