#!/bin/env python

import datetime
import sys
from cisco import *
from cli import *

MAX_NUMBER = 20
DEFAULT_NUMBER = 5

def log(msg):
    current_time = str(datetime.datetime.now())
    print(current_time + ':: ' + msg)

def get_number_of_interfaces():
    if len(sys.argv) > 1:
        intf_num = int(sys.argv[1])
    else:
        intf_num = DEFAULT_NUMBER
    if intf_num > MAX_NUMBER:
        intf_num = MAX_NUMBER
    return intf_num

def set_interfaces(num):
    base_name = 'Lo{}'
    log('Getting the output of "show interface brief"')
    output = cli("show interface brief | i Lo")
    log('The output is:')
    for line in output.splitlines():
        log('   ' + line)
    for i in range(int(num)):
        name = base_name.format(str(1001 + i))
        if name in output:
            log('Interface {} already exists'.format(name))
            continue
        log('Interface {} not found'.format(name))
        cmd = 'conf t ; int {}'.format(name)
        log('Creating interface {}'.format(name))
        cli(cmd)

if __name__ == '__main__':
    num = get_number_of_interfaces()
    log('Creating {} loopback interfaces.'.format(str(num)))
    set_interfaces(num)