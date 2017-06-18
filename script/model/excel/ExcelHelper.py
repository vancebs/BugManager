#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlwings as xw
import os
import shutil
import tkMessageBox


class ExcelHelper(object):
    EXT = '.xlsm'
    PATH_TEMPLATE_GENERAL = './template/general.xlsm'

    CREATE_OVERRIDE_YES = 0
    CREATE_OVERRIDE_NO = 1
    CREATE_OVERRIDE_ASK = 2

    @staticmethod
    def create_from_template(path, override=CREATE_OVERRIDE_ASK, template=None):
        if template is None:
            template = ExcelHelper.PATH_TEMPLATE_GENERAL

        # check path's ext
        if not str(path).endswith(ExcelHelper.EXT):
            path = '%s%s' % (path, ExcelHelper.EXT)

        # check file already exists
        if os.path.exists(path):
            if override == ExcelHelper.CREATE_OVERRIDE_YES:
                os.remove(path)  # remove the file
            elif override == ExcelHelper.CREATE_OVERRIDE_ASK:
                # not support override. TODO: may implement later
                yes = tkMessageBox.askyesno('Warning', 'File already exists. Override???')
                if yes:
                    os.remove(path)  # remove the file
                else:
                    return None
            elif override == ExcelHelper.CREATE_OVERRIDE_NO:
                return None
            else:
                return None

        # copy from template
        shutil.copy(template, path)

        return xw.Book(path)

    @staticmethod
    def get_app():
        apps = xw.apps
        if apps.count < 1:
            return xw.App(visible=True, add_book=False)
        else:
            return apps[0]

    @staticmethod
    def get_opened_workbook(path):
        app = ExcelHelper.get_app()
        for book in app.books:
            if os.path.realpath(path) == os.path.realpath(book.fullname):
                return book
        return None

    @staticmethod
    def open_workbook(path):
        # get from opened workbooks
        book = ExcelHelper.get_opened_workbook(path)
        if book:
            # already opened just active the workbook
            book.activate(True)
            return book
        else:
            # open the workbook
            app = ExcelHelper.get_app()
            return app.books.open(path)

    @staticmethod
    def close_workbook(path):
        # get from opened workbooks
        book = ExcelHelper.get_opened_workbook(path)
        if book:
            book.close()


