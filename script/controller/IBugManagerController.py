#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import abstractmethod, ABCMeta


class IBugManagerController(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cmd_open(self, view):
        pass

    @abstractmethod
    def cmd_sync(self, view):
        pass

    @abstractmethod
    def cmd_sync_all(self, view):
        pass

    @abstractmethod
    def cmd_view(self, view):
        pass

    @abstractmethod
    def cmd_edit(self, view):
        pass
