#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ICommand import ICommand


class CmdConfigExcel(ICommand):
    def __init__(self, path, create_info):
        ICommand.__init__(self)
        self._mPath = path
        self._mCreateInfo = create_info

    def on_start(self):
        pass

    def on_cancel(self):
        pass

        # # TODO implement new later
        # # open workbook
        # book = ExcelHelper.open_workbook(path)
        #
        # # init
        # self._init_workbook(book)
