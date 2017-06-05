#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import tkFileDialog
import tkMessageBox
import shutil
from ICommand import ICommand
from script.model.local_alm.cfg.Config import Config
from script.view.ConfigExcelView import ConfigExcelView
from script.controller.ConfigExcelController import ConfigExcelController


class CmdNewExcel(ICommand):
    _DEFAULT_EXCEL_DIR = './excel'
    _EXT = '.xlsm'

    def __init__(self, parent_view):
        ICommand.__init__(self)
        self._mParentView = parent_view

    def on_cancel(self):
        pass

    def on_start(self):
        # add path to recent
        cfg = Config()

        path = self._new()

        if path:
            cfg.add_recent(path)
            print ('\t new excel: %s' % path)

    def _new(self):
        # check whether default dir is created
        if not os.path.exists(CmdNewExcel._DEFAULT_EXCEL_DIR):
            os.makedirs(CmdNewExcel._DEFAULT_EXCEL_DIR)
        elif not os.path.isdir(CmdNewExcel._DEFAULT_EXCEL_DIR):
            print ('[Warning] default path already exists a file')

        path = tkFileDialog.asksaveasfilename(
            title='New excel',
            initialdir=CmdNewExcel._DEFAULT_EXCEL_DIR,
            filetypes=[('Excel (xlsm)', CmdNewExcel._EXT)])

        # user may cancel when select open file
        if path == '':
            return None

        # check path's ext
        if not str(path).endswith(CmdNewExcel._EXT):
            path = '%s%s' % (path, CmdNewExcel._EXT)

        # check file already exists
        if os.path.exists(path):
            # not support override. TODO: may implement later
            tkMessageBox.showerror('Error', 'File already exists.')
            return None

        # copy from template
        shutil.copy('./template/template.xlsm', path)

        # config excel
        controller = ConfigExcelController(path)
        view = ConfigExcelView(self._mParentView, controller)
        view.show(wait=True)

        if not controller.is_success():
            # remove file if config canceled by user
            os.remove(path)
            return None

        # return path
        return path
