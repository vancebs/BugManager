#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.controller.command.ICommand import ICommand
from script.model.local_alm.cfg.Config import Config
import os
import tkinter.messagebox


class CmdRemoveExcel(ICommand):
    def __init__(self, path):
        ICommand.__init__(self)
        self.mPath = path

    def on_cancel(self):
        pass

    def on_start(self):
        cfg = Config()
        path = self.mPath

        print('\t remove excel: %s' % path)
        # TODO improve later
        if os.path.exists(path):
            if tkinter.messagebox.askyesno('Remove excel', 'Remove excel file.\nAre you sure?'):
                os.remove(path)
                cfg.remove_recent(path)
        else:
            cfg.remove_recent(path)
