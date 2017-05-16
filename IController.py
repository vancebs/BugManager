#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import abstractmethod, ABCMeta


class IController(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cmd_sync(self):
        pass

    @abstractmethod
    def cmd_sync_all(self):
        pass

    @abstractmethod
    def cmd_view(self):
        pass

    @abstractmethod
    def cmd_edit(self):
        pass