#!/usr/bin/env python3

import random
import socket
import sys
import time


def main():
    if len(sys.argv) < 5:
        print("usage: {} <ip> <port> <sleep> <jitter>".format(sys.argv[0]))
        sys.exit(1)

    c2ip = sys.argv[1]
    c2port = int(sys.argv[2])
    stime = int(sys.argv[3])
    jitter = float(sys.argv[3])

    if c2port <= 0:
        print("{}: invalid port '{}'".format(sys.argv[0], sys.argv[2]))
        sys.exit(1)
    elif stime < 0:
        print("{}: invalid sleep parameter '{}'".format(sys.argv[0], sys.argv[3]))
        sys.exit(1)
    elif jitter < 0:
        print("{}: invalid jitter parameter '{}'".format(sys.argv[0], sys.argv[4]))
        sys.exit(1)

    while True:
        r = (random.random() - 0.5)
        time.sleep(stime + int(jitter * r))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((c2ip, c2port))
            s.sendall(b'beacon: hello\n')
            msg = s.recv(64)
            print(msg)


if __name__ == '__main__':
    main()
