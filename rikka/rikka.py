#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import json
import sys
import pandas as pd
from logging import config, getLogger
from datetime import datetime as dt
import jpxpy.realtime_index
import investpy
import line
import line_token


def logger_init(name='test'):
    log_config = "log.json"
    config.dictConfig(json.loads(open(log_config, encoding='UTF-8').read()))
    return getLogger(name)


logger = logger_init()


def main_unit():
    loop_sec = 60
    max_notify_count = 5
    # TODO:通知でclose_priceの折れ線グラフを送りたい
    # TODO:DJI
    # TODO:N225
    while True:
        # mothers
        check_entry("mothers", max_notify_count)
        check_entry("topix_reit", max_notify_count)
        check_entry("topix", max_notify_count)
        check_entry("dji", max_notify_count)
        time.sleep(loop_sec)


def check_entry(index_name, max_notify_count):
    csv = "entry.csv"
    df = pd.read_csv(csv, index_col=0)
    temp_df = df[df.index == index_name]
    stop_long_value = temp_df["stop_long"][0]
    stop_short_value = temp_df["stop_short"][0]
    notify_count = temp_df["notify_count"][0]
    close_time, close_price = get_closeprice(index_name)
    if close_price is None:
        return
    line_agent = line.Line(line_token.line_token)
    if notify_count >= max_notify_count:
        logger.debug(f"notify_count:[{notify_count}], max_notify_count:[{max_notify_count}]")
        return
    if stop_long_value != 0 and stop_long_value <= close_price:
        notify_count += 1
        msg = f"long trigger[{notify_count}]:" \
              f"index[{index_name}],stop_long_value[{stop_long_value:.2f}], close_price[{close_price:.2f}]"
        logger.info(msg)
        line_agent.send_message(msg)
        df.loc[index_name, "notify_count"] = notify_count
        df.to_csv(csv)
    elif stop_short_value != 0 and stop_short_value <= close_price:
        notify_count += 1
        msg = f"short trigger[{notify_count}]:index[{index_name}]" \
              f", stop_short_value[{stop_short_value:.2f}], close_price[{close_price:.2f}]"
        logger.info(msg)
        line_agent.send_message(msg)
        df.loc[index_name, "notify_count"] = notify_count
        df.to_csv(csv)
    else:
        logger.debug(f"None Order index[{index_name}], close_price:[{close_price}]"
                     f", stop_long_value:[{stop_long_value}], stop_short_value:[{stop_short_value}]")


def get_closeprice(index_name):
    close_time = None
    close_price = None
    try:
        if index_name == "mothers":
            rs = jpxpy.realtime_index.get_realtime_index_mothers()
        elif index_name == "topix_reit":
            rs = jpxpy.realtime_index.get_realtime_index_topix_reit()
        elif index_name == "topix":
            rs = jpxpy.realtime_index.get_realtime_index_topix()
        elif index_name == "dji":
            # current_date = dt.now().strftime("%Y-%m-%d")
            # data = investpy.get_index_historical_data(index="Dow 30"
            #                                           , country="united states"
            #                                           , from_date=current_date
            #                                           , to_date=current_date)
            pass
        else:
            return None, None
        close_time = rs["close_time"]
        close_price = rs["close_price"]
        logger.info(f"{index_name}:{close_price:.2f}({close_time})")
    except Exception as err:
        # logger.debug(err)
        pass
    return close_time, close_price


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
