#!/usr/bin/python
# -*- coding: UTF-8 -*-

from command.CmdConfigExcel import CmdConfigExcel


class ConfigExcelController(object):
    def __init__(self, path):
        self.mPath = path
        self._mIsSuccess = False

    def cmd_new_excel(self, root, create_info):
        cmd = CmdConfigExcel(self.mPath, create_info)
        cmd.start()

        # close window
        ConfigExcelController.close_window(root)
        self._mIsSuccess = True

    def cmd_cancel(self, root):
        # close window
        ConfigExcelController.close_window(root)
        self._mIsSuccess = False

    @staticmethod
    def close_window(view):
        view.after(0, view.destroy)

    def is_success(self):
        return self._mIsSuccess


