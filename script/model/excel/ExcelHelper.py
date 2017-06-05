#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlwings as xw
import os


class ExcelHelper(object):
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
            #if os.path.samefile(path, book.fullname):
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


