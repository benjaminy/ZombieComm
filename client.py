#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: evanmega
# @Date:   2014-10-19 17:01:01
# @Last Modified by:   evanmega
# @Last Modified time: 2014-10-19 19:02:54

import socket

'''
simply connects to server and prints any data received
'''
if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080
    SIZE = 1024

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print 'successfully connected'
    except:
        print 'could not connect'
        os._exit(1)

    while True:
        data = s.recv(1024)
        print data
