#!/usr/bin/python
# -*- coding: UTF-8 -*-

from BugManagerUI import BugManagerUI
from BugManagerController import BugManagerController

if __name__ == "__main__":
    controller = BugManagerController()
    ui = BugManagerUI()
    ui.create(controller)
    ui.show()
