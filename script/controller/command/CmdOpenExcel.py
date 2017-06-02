#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ICommand import ICommand
from script.model.local_alm.cfg.Config import Config
from script.model.excel.ExcelHelper import ExcelHelper


class CmdOpenExcel(ICommand):
    def __init__(self, path):
        ICommand.__init__(self)
        self.mPath = path

    def on_cancel(self):
        pass

    def on_start(self):
        path = self.mPath
        cfg = Config()

        print ('\t open excel: %s' % path)
        self._open(path)

        # always move the opened item to top
        cfg.update_recent(path)

    def _open(self, path):
        ExcelHelper.open_workbook(path)
