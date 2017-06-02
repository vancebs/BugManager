#!/usr/bin/python
# -*- coding: UTF-8 -*-

from controller.BugManagerController import BugManagerController
from view.BugManagerView import BugManagerView


class BugManager(object):
    def launch(self):
        controller = BugManagerController()
        ui = BugManagerView(controller)
        ui.show()

if __name__ == "__main__":
    bm = BugManager()
    bm.launch()
