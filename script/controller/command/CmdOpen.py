#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ICommand import ICommand
from script.view.OpenView import OpenView
from script.controller.OpenController import OpenController


class CmdOpen(ICommand):
    def __init__(self, parent_view):
        ICommand.__init__(self)
        self._mParentView = parent_view

    def on_start(self):
        print('CmdOpen# on_start()')
        view = OpenView(self._mParentView, OpenController())
        view.show()

    def on_cancel(self):
        print('CmdOpen# on_cancel()')