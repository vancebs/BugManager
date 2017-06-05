#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ICommand import ICommand
from script.view.SyncProgressView import SyncProgressView
from script.controller.SyncProgressController import SyncProgressController


class CmdCreate(ICommand):
    def __init__(self, parent_view):
        ICommand.__init__(self)
        self._mParentView = parent_view

    def on_cancel(self):
        pass

    def on_start(self):
        v = SyncProgressView(self._mParentView, SyncProgressController(self._mParentView))
        v.show()
