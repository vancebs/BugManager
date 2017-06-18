#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.controller.BugManagerController import BugManagerController
from script.view.BugManagerView import BugManagerView


class BugManager(object):
    def launch(self):
        controller = BugManagerController()
        ui = BugManagerView(controller)
        ui.show()

if __name__ == "__main__":
    bm = BugManager()
    bm.launch()
