#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import abstractmethod, ABCMeta


class View(object):
    __metaclass__ = ABCMeta

    BUTTON_PADDING_X = 5
    BUTTON_PADDING_Y = 5

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def dismiss(self):
        pass
