#!/usr/bin/python
# -*- coding: UTF-8 -*-

from IController import IController


class BugManagerController(IController):
    def __init__(self):
        pass

    def cmd_sync(self):
        print ('cmd_sync')

    def cmd_sync_all(self):
        print ('cmd_sync_all')

    def cmd_view(self):
        print ('cmd_view')

    def cmd_edit(self):
        print ('cmd_edit')