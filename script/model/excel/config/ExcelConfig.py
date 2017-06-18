#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlwings as xw

from script.model.excel.config.Key import Key
from script.model.excel.config.StyledValue import StyledValue
from script.model.excel.config.Value import Value


class ExcelConfig(object):
    @staticmethod
    def load_value(sheet, row, col):
        if not isinstance(sheet, xw.Sheet):
            raise TypeError('Invalid type of parameter [sheet] or [value]')
        value = StyledValue(sheet.range(row, col).value)
        return None if value.value is None else value

    @staticmethod
    def save_value(sheet, row, col, value):
        if not isinstance(sheet, xw.Sheet):
            raise TypeError('Invalid type of parameter [sheet]')
        sheet.range(row, col).value = value.value

    def save(self, sheet, row, col, key):
        # clear old content
        sheet.cells.clear()

        # save keys & values
        self._save(sheet, row, col, key)

    def _save(self, sheet, row, col, key):
        # no child
        if len(key.children) <= 0 or type(key.children[0]) == Value or type(key.children[0]) == StyledValue:
            # now we should save the values
            r = row + 1
            for value in key.values:
                self.on_save_value(sheet.range(r, col), value)
                r += 1

            # return the col
            col_child = col
        else:
            col_child = col - 1

            # save children
            for child in key.children:
                col_child = self._save(sheet, row + 1, col_child + 1, child)

        # save key to sheet
        self.on_save_key(sheet.range(row, col), key)

        # return the last child 's col
        return col_child

    def load(self, sheet, row, col):
        # find the max continue row as the end of sub key row
        max_col_count = 0
        max_r = 0
        max_c = 0
        col_count = 0
        r = row
        c = col
        while True:
            col_count = 0
            c = col
            while True:
                if not ExcelConfig.is_empty(sheet.range(r, c).value):
                    c += 1
                    col_count += 1
                else:
                    if col_count > max_col_count:
                        max_col_count = col_count
                        max_r = r
                        max_c = c
                    break

            if c == col:
                break
            r += 1

        if max_col_count <= 0:
            raise ValueError('Format of config sheet is invalid')

        row_key_end = max_r
        col_end = max_c

        root = Key(sheet.range(row, col).value)
        if root.name is None:
            raise ValueError('Format of config sheet is invalid')

        # load keys & values
        self._load_key(sheet, root, row + 1, row_key_end, col, col_end)

        return root

    def _load_key(self, sheet, parent, row, row_end, col_begin, col_end):
        if row > row_end:
            # all keys are loaded. now we should load values
            while True:
                value = self.on_load_value(sheet.range(row, col_begin))
                if value is not None:
                    parent.add_value(value)
                    row += 1
                else:
                    break  # reach end of value
            return

        last_key = None
        last_c = 0
        for c in range(col_begin, col_end + 1):
            key = self.on_load_key(sheet.range(row, c))
            if key is not None:
                parent.add_child(key)
                if last_key is not None:
                    self._load_key(sheet, last_key, row + 1, row_end, last_c, c - 1)

                last_key = key
                last_c = c

        if last_key is not None:
            self._load_key(sheet, last_key, row + 1, row_end, last_c, col_end)

    def on_save_value(self, cell, value):
        value.save(cell)

    def on_save_key(self, cell, key):
        key.save(cell)

    def on_load_value(self, cell):
        value = StyledValue()
        value.load(cell)

        return value if value.value is not None else None

    def on_load_key(self, cell):
        key = Key()
        key.load(cell)

        return key if key.name is not None else None

    @staticmethod
    def is_empty(value):
        if value is None:
            return True

        value = str(value).strip()
        if value == '':
            return True

        return False
#     NAME_ROOT_KEY = 'Don\'t edit this sheet by yourself. It should be auto generated'
#     ROW_ROOT_KEY = 1
#     ROW_KEY = 2
#     ROW_SUB_KEY = 3
#     ROW_VALUE_BEGIN = 4
#     COL_BEGIN = 1
#
#     HEADER_KEY_ROW = '{header_key_row}'
#     HEADER_KEY_COL_BEGIN = '{header_key_col_begin}'
#     HEADER_KEY_COL_END = '{header_key_col_end}'
#     HEADER_KEY_SUB_KEYS = '{header_key_sub_keys}'
#
#     SHEET_CONFIG = 'Config'
#
#     # Projects
#     KEY_PROJECTS = 'Projects'
#     SUB_KEY_PROJECTS = 'Projects'
#     SUB_KEY_BRANCHES = 'Branches'
#     SUB_KEY_ALIAS_PROJECTS = 'Alias Projects'
#
#     # Teams
#     KEY_TEAMS = 'Teams'
#     SUB_KEY_TEAMS = 'Teams'
#     SUB_KEY_ALIAS_TEAMS = 'Alias Teams'
#
#     # Users
#     KEY_USERS = 'Users'
#     SUB_KEY_USERS = 'Assigned Users'
#     SUB_KEY_USER_ALIAS_TEAMS = 'User Alias Teams'
#
#     # Bug View
#     KEY_BUG_VIEW = 'Bug View'
#     SUB_KEY_TYPES = 'Types'
#     SUB_KEY_COLUMNS = 'Columns'
#
#     def __init__(self, path_or_book):
#         if isinstance(path_or_book, xw.Book):
#             self._mBook = path_or_book
#             self._mCfgSheet = self._mBook.sheets(ExcelConfig.SHEET_CONFIG)
#         elif isinstance(path_or_book, str):
#             self._mBook = xw.Book(path_or_book)
#             self._mCfgSheet = self._mBook.sheets(ExcelConfig.SHEET_CONFIG)
#         else:
#             raise TypeError('path_or_book is not in right type')
#
#         # create root key
#         self._mRootConfigKey = ExcelConfig.Key.create(
#             self._mCfgSheet, ExcelConfig.ROW_ROOT_KEY, ExcelConfig.COL_BEGIN, None, None, True)
#         if self._mRootConfigKey.name is None:
#             self._mRootConfigKey.name = ExcelConfig.NAME_ROOT_KEY
#
#     def load(self):
#         print ('load')
#         sheet = self._mCfgSheet
#         if not isinstance(sheet, xw.Sheet):
#             raise StandardError('Excel should have sheet %s' % ExcelConfig.SHEET_CONFIG)
#
#         # load keys
#         self._load_keys()
#
#         # load value
#         for key in self._mConfigs.values():
#             key.data = self._load_values(sheet, key)
#
#         return self._mConfigs
#
#     def save(self):
#         print ('save')
#
#         # save
#         self._mBook.save()
#
#     def _load_keys(self):
#         sheet = self._mCfgSheet
#         root_key = self._mRootConfigKey
#
#         col = ExcelConfig.COL_BEGIN
#         cur_key = None
#         while True:
#             key = ExcelConfig.Key.create(sheet, ExcelConfig.ROW_KEY, col)
#             sub_key = ExcelConfig.Key.create(sheet, ExcelConfig.ROW_SUB_KEY, col)
#
#             # check for column end
#             if sub_key is None:
#                 break  # reach the end of column
#
#             # update current key
#             if key is not None:
#                 cur_key = key
#
#                 # add current key to root key
#                 root_key.add_child(cur_key)
#
#             # key should not be None when reach here. Or the format of config sheet is wrong
#             if cur_key is None:
#                 raise ValueError('Invalid format of excel config')
#
#             # add sub key to cur_key
#             cur_key.add_child(sub_key)
#
#             # next column
#             col += 1
#
#     @staticmethod
#     def _load_values(sheet, key):
#         if not isinstance(sheet, xw.Sheet) or not isinstance(key, ExcelConfig.Key):
#             raise TypeError('Invalid type of parameter')
#
#         values = list()
#         row = key.children.values[0].row + 1
#         while True:
#             reach_end = False
#             for sub_key in key.children:
#                 value = ExcelConfig.Value.create(sheet, row, sub_key.col)
#                 if value is None:
#                     # check for row end
#                     reach_end = True
#                     break
#                 else:
#                     # save data
#                     values.append(value)
#
#             # check for row end
#             if reach_end:
#                 break
#
#             # next row
#             row += 1
#         return values
#
#     def get_config(self):
#         return self._mConfigs
#
#     def keys(self):
#         return self._mConfigs.keys()
#
#     def sub_keys(self, key_name):
#         sub_key = self._mConfigs.get(key_name)
#         if sub_key is None:
#             return None
#         else:
#             return sub_key.keys()
#
#     def get_data(self, key_name, sub_key_name):
#         if not isinstance(key_name, str) or not isinstance(sub_key_name, str):
#             raise ValueError('key should not be None and should be type of str.'
#                              ' key: %s, sub_key: %s' % (key_name, sub_key_name))
#
#         # get key
#         key = self._mConfigs.get(key_name)
#         if key is None:
#             # key not found
#             return None
#
#         # get sub key
#         sub_key = key.children[sub_key_name]
#         if sub_key is None:
#             # sub key not found
#             return None
#
#         # get data
#         data = sub_key.data
#         if data is None:
#             return []
#         elif isinstance(data, ExcelConfig.Value):
#             return [data]
#         elif isinstance(data, list):
#             return data
#         else:
#             raise TypeError('Invalid type of data')
#
#     def set_data(self, key_name, sub_key_name, data):
#         if not isinstance(key_name, str) or not isinstance(sub_key_name, str):
#             raise ValueError('key should not be None and should be type of str.'
#                              ' key: %s, sub_key: %s' % (key_name, sub_key_name))
#
#         # find key
#         key = self._mConfigs.get(key_name)
#         if key is None:
#             # key not exists, create one
#
#
#     def get_or_create_key(self, key_name, sub_key_name):
#         # find key
#         key = self._mConfigs.get(key_name)
#         if key is None:
#             # find a column to create new key
#             max_col = ExcelConfig.COL_BEGIN - 1
#             row = ExcelConfig.ROW_KEY
#             sheet = self._mCfgSheet
#             for temp_key in self._mConfigs.values():
#                 if temp_key.col_end > max_col:
#                     max_col = temp_key.col_end
#             max_col += 1  # point to new column
#
#             # create a new key
#             key = ExcelConfig.Key(sheet, row, max_col)
#
#         # find sub key
#         sub_key = key.children.get(sub_key_name)
#         if sub_key is None:
#             # find a column to create new sub key
#             max_col = key.col_begin - 1
#             row = ExcelConfig.ROW_SUB_KEY
#             sheet = self._mCfgSheet
#
# #TODO
#
#
#
#     def set(self, key, sub_key, values):
#         if key is None or sub_key is None:
#             raise ValueError('key and sub_key should not be None. key: %s, sub_key: %s' % (key, sub_key))
#
#         # get sub key map
#         sub_key_map = self._mConfigs.get(key)
#         if sub_key_map is None:
#             sub_key_map = dict()
#             self._mConfigs[key] = sub_key_map
#
#         # set sub key values
#         sub_key_map[sub_key] = values
#
#     def close(self):
#         self._mBook.close()
#
#     @staticmethod
#     def _load_sub_key_value(sheet, col, begin_row, end_row=-1):
#         values = []
#
#         if end_row <= 0:
#             # end row unknown. read until reach a blank cell
#             row = begin_row
#             while True:
#                 # read value
#                 value = sheet.range(row, col).value
#                 value = ExcelConfig._verify_value(value)
#
#                 # check for end
#                 if value is None:
#                     break
#
#                 # append value
#                 values.append(value)
#         else:
#             # end row is provided. just read all cells in range
#             for row in range(begin_row, end_row):
#                 # read value
#                 value = sheet.range(row, col).value
#                 value = ExcelConfig._verify_value(value)
#
#                 # append value
#                 if value is None:
#                     values.append('')
#                 else:
#                     values.append(value)
#
#         return values
