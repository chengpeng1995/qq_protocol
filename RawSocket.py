# -*- coding: utf-8 -*-

import socket

import select


class RawSocket:
    '''Python socket: http://blog.csdn.net/rebelqsp/article/details/22109925'''
    def __init__(self, ip, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        self.con = self.socket.connect(('14.215.138.105',8080))
        self.socket.setblocking(0)
    def __del__(self):
        self.socket.close()

    def connect(self):
        if not self.con:
            return True
        else:
            return False

    def sendall(self, data):
        try:
            return self.socket.sendall(data) == None
        except Exception, e:
            print u'数据发送失败: ', e
        return False

    def recv(self):
        buf = '0'
        infds,outfds,errfds = select.select([self.socket,],[],[],1)
        if len(infds) > 0:
            buf = self.socket.recv(1024)
            while True: #确保把包收全
                try:
                    tmp = self.socket.recv(1024)
                    buf += tmp
                except socket.error as e:
                    if e.args[0] == socket.errno.EWOULDBLOCK:
                        return buf
        else:
            return buf

    def close(self):
        return self.socket.close()

