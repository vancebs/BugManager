#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time


class TimeUtil(object):
    _DATETIME_FORMAT_CHINESE = '%Y-%m-%d %H:%M:%S'
    _DATETIME_FORMAT_ENGLISH = '%b %d, %Y %I:%M:%S %p'
    _DATETIME_FORMAT_TARGET = _DATETIME_FORMAT_ENGLISH
    _DATETIME_FORMATS = (_DATETIME_FORMAT_CHINESE, _DATETIME_FORMAT_ENGLISH)

    @staticmethod
    def format_time(time_src):
        time_formatted = None
        if isinstance(time_src, str) or isinstance(time_src, bytes):
            for f in TimeUtil._DATETIME_FORMATS:
                try:
                    time_formatted = time.strptime(time_src, f)
                    break
                except ValueError:
                    pass

            if time_formatted is None:
                print('unknown format: %s' % time_src)
                raise ValueError('unknown format: %s' % time_src)
        elif isinstance(time_src, time.struct_time):
            time_formatted = time_src
        elif isinstance(time_src, float):
            time_formatted = time.localtime(time_src)
        elif isinstance(time_src, int):  # treat int as float
            time_formatted = time.localtime(time_src)

        # return time
        return time_formatted

    @staticmethod
    def format_time_to_str(time_src):
        return time.strftime(TimeUtil._DATETIME_FORMAT_TARGET, TimeUtil.format_time(time_src))

    @staticmethod
    def format_time_to_float(time_src):
        return time.mktime(TimeUtil.format_time(time_src))

    @staticmethod
    def format_time_to_int(time_src):
        return int(time.mktime(TimeUtil.format_time(time_src)))

    @staticmethod
    def current_time():
        return time.localtime()

    @staticmethod
    def time_add(time_src, add):
        t = TimeUtil.format_time_to_float(time_src)
        a = TimeUtil.format_time_to_float(add)
        return TimeUtil.format_time(t + a)

    @staticmethod
    def time_sub(time_src, sub):
        t = TimeUtil.format_time_to_float(time_src)
        s = TimeUtil.format_time_to_float(sub)
        return TimeUtil.format_time(t - s)
