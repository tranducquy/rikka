#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import json
import sys
import pandas as pd
import urllib
from logging import config, getLogger
from datetime import datetime
import jpxpy.realtime_index


def logger_init(name='test'):
    config.dictConfig(json.loads(open("log.json", encoding='UTF-8').read()))
    return getLogger(name)


logger = logger_init()


def main_unit():
    loop_sec = 60
    max_notify_count = 5
    # [x] CSVから逆指値取得
    # [x] WEBから指数の現在値取得
    # [x] 比較
    # [ ] 通知
    # [ ] 通知後のカウントアップ
    # [ ] CSV書き込み
    # [x] sleep
    while True:
        df = pd.read_csv("entry.csv")
        # mothers
        index_name = "mothers"
        mothers_df = df[df['index_name'] == index_name]
        stop_long_value = mothers_df["stop_long"][0]
        stop_short_value = mothers_df["stop_short"][0]
        notify_count = mothers_df["notify_count"][0]
        close_price_time, close_price = get_closeprice(index_name)
        # TODO:通知でclose_priceの折れ線グラフを送りたい
        if stop_long_value != 0 and stop_long_value <= close_price:
            logger.info(f"long trigger[{notify_count}]:"
                        f"index[{index_name}],stop_long_value[{stop_long_value:.2f}], close_price[{close_price:.2f}]")
            notify_count += 1
        elif stop_short_value != 0 and stop_short_value <= close_price:
            logger.info(f"short trigger[{notify_count}]:index[{index_name}]"
                        f", stop_short_value[{stop_short_value:.2f}], close_price[{close_price:.2f}]")
            notify_count += 1
        else:
            logger.info(f"None Order close_price:[{close_price}]"
                        f", stop_long_value:[{stop_long_value}], stop_short_value:[{stop_short_value}]")

        time.sleep(loop_sec)


def nofify_stop_trigger():
    pass


def get_closeprice(index_name):
    close_price_time = None
    close_price = None
    try:
        if index_name == "mothers":
            rs = jpxpy.realtime_index.get_realtime_index_mothers()
        else:
            return None, None
        close_price_time = rs["close_price_time"]
        close_price = rs["close_price"]
    except Exception as err:
        logger.error(err)
    logger.info(f"{index_name}:{close_price:.2f}({close_price_time})")
    return close_price_time, close_price


def topix_reit():
    pass


def dow30():
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
