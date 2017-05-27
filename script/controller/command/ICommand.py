#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from abc import abstractmethod, ABCMeta


class ICommand(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._mThread = None
        self._mIsRunning = False

    def start(self, async, on_finished, param):
        if async:
            self._mIsRunning = True
            self._mThread = threading.Thread(target=self._run, args=(on_finished, param))
            self._mThread.start()
        else:
            self._mIsRunning = True
            self.on_start()
            self._mIsRunning = False
            if on_finished:
                on_finished(param)

    def cancel(self):
        self.on_cancel()

    def running(self):
        return self._mIsRunning

    def _run(self, on_finished, param):
        self.on_start()
        if on_finished:
            on_finished(param)

        self._mThread = None
        self._mIsRunning = False

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_cancel(self):
        pass
