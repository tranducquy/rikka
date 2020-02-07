#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import json
import sys
import jpxpy.realtime_index
from logging import config, getLogger


def logger_init(name='test'):
    config.dictConfig(json.loads(open("log.json", encoding='UTF-8').read()))
    return getLogger(name)


def main_unit():
    loop_sec = 60
    logger = logger_init()
    while True:
        mothers(logger)
        time.sleep(loop_sec)


def mothers(logger):
    short_stop_value = 816.00
    long_stop_value = 0.0
    # logger.info(f"rikka: long_stop_value:[{long_stop_value}],short_stop_value:[{short_stop_value}]")
    try:
        mothers = jpxpy.realtime_index.get_realtime_index_mothers()
        close_price_time = mothers["close_price_time"]
        close_price = mothers["close_price"]
        if close_price and long_stop_value != 0 and long_stop_value < close_price:
            logger.info(f"LONG ORDER close_price:[{close_price},({close_price_time})]")
        elif close_price and short_stop_value != 0 and short_stop_value > close_price:
            logger.info(f"SHORT ORDER close_price:[{close_price},({close_price_time})]")
        else:
            logger.info(f"NONE ORDER close_price:[{close_price}({close_price_time})]"
                        f",stop_order_value:[{long_stop_value}],stop_short_value:[{short_stop_value}]")
    except Exception as err:
        logger.error(err)
    pass


def topix_reit():
    pass


def daemonize():
    pid = os.fork()
    if pid > 0:
        pid_file = open('/tmp/rikka_daemon.pid', 'w')
        pid_file.write(str(pid) + "\n")
        pid_file.close()
        sys.exit()
    if pid == 0:
        main_unit()


if __name__ == '__main__':
    # while True:
    #     daemonize()
    main_unit()
