#!/bin/env python

import datetime
from cisco import *
from cli import *

def get_switchname():
    return cli("show switchname").strip()

def get_kickstart():
    output = cli("show version | i kickstart:")
    return output.strip().split(' ')[-1]

def get_software():
    output = cli("show version | i system:")
    return output.strip().split(' ')[-1]

def get_uptime():
    output = cli("show version | i 'Kernel uptime'")
    return output.replace('Kernel uptime is', '').strip()

if __name__ == "__main__":
    print("")
    print("---------- [Printing report] ----------")
    print("     {: <20} {}".format('Current time:', str(datetime.datetime.now())))
    print("     {: <20} {}".format('Switch uptime:', get_uptime()))
    print("     {: <20} {}".format('Switch name:', get_switchname()))
    print("     {: <20} {}".format('Kickstart version:', get_kickstart()))
    print("     {: <20} {}".format('Software version:', get_software()))
    print("--------------------------------------------")
    print("")
