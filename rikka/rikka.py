#! /usr/bin/env python
# -*- coding: utf-8 -*-


import time
import os
import sys
import jpxpy.realtime_index


def main_unit():
    loop_sec = 60
    short_stop_value = 819.00
    long_stop_value = 0.0
    while True:
        mothers = jpxpy.realtime_index.get_realtime_index_mothers()
        low_price = mothers["low_price"]
        if short_stop_value > low_price:
            print("low")

        time.sleep(loop_sec)


def daemonize():
    pid = os.fork()
    if pid > 0:
        pid_file = open('/var/run/python_daemon.pid', 'w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        main_unit()


if __name__ == '__main__':
    while True:
        daemonize()


