#!/usr/bin/env python2
# coding=utf8

import liblo

def sendToXOSC(address, string, var):
        liblo.send(address, string, var)
