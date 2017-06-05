#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlwings as xw


class ExcelConfig(object):
    ROW_CONFIG_NAME = 3
    COL_CONFIG_NAME_BEGIN = 1

    ROW_CONFIG_BEGIN = 4

    SHEET_CONFIG = 'Config'

    # Projects
    NAME_PROJECTS = 'Projects'
    NAME_BRANCHES = 'Branches'
    NAME_ALIAS_PROJECTS = 'Alias Projects'

    # Teams
    NAME_TEAMS = 'Teams'
    NAME_ALIAS_TEAMS = 'Alias Teams'

    # Users
    NAME_USERS = 'Assigned Users'
    NAME_USER_ALIAS_TEAMS = 'User Alias Teams'

    # Bug View
    NAME_TYPES = 'Types'
    NAME_COLUMNS = 'Columns'

    # Names list
    CONFIG_NAMES = (
        NAME_PROJECTS,
        NAME_BRANCHES,
        NAME_ALIAS_PROJECTS,
        NAME_TEAMS,
        NAME_ALIAS_TEAMS,
        NAME_USERS,
        NAME_USER_ALIAS_TEAMS,
        NAME_TYPES,
        NAME_COLUMNS
    )

    def __init__(self, path_or_book):
        if isinstance(path_or_book, xw.Book):
            self._mBook = path_or_book
        elif isinstance(path_or_book, str):
            self._mBook = xw.Book(path_or_book)
        else:
            raise TypeError('path_or_book is not in right type')

        self._mConfig = dict()
        self._mConfigColumnMap = dict()

    def load(self):
        print ('load')
        sheet = self._mBook.sheets[ExcelConfig.SHEET_CONFIG]
        if sheet is None:
            raise StandardError('Excel should have sheet %s' % ExcelConfig.SHEET_CONFIG)

        # TODO remove later
        sheet = xw.Sheet(sheet)

        # get config map
        col = ExcelConfig.COL_CONFIG_NAME_BEGIN
        while True:
            v = sheet.range(ExcelConfig.ROW_CONFIG_NAME, col).value
            if v is None:
                break  # reach end
            v = v.strip()
            if v == '':
                break  # reach end

            # save column id
            self._mConfigColumnMap[v] = col

            # next column
            col += 1

        cell1 = sheet.range(2, 1)
        cell2 = sheet.range(2, 2)
        cell3 = sheet.range(2, 3)

        # read config
        for name in self._mConfigColumnMap.keys():
            cfg = ExcelConfig._on_load_config(sheet, name, ExcelConfig.ROW_CONFIG_BEGIN, self._mConfigColumnMap[name])
            if cfg is not None:
                self._mConfig[name] = cfg

        return self._mConfig

    def save(self, config):
        self._mBook.save()

    def get_config(self):
        return self._mConfig

    def close(self):
        self._mBook.close()

    def _get_config_column(self, name):
        return self._mConfigColumnMap[name]

    @staticmethod
    def _on_load_config(sheet, name, begin_row, col):
        loader = ExcelConfig.CONFIG_LOADER[name]
        if loader is not None:
            return loader(sheet, begin_row, col)
        else:
            return None

    @staticmethod
    def _on_load_config_projects(sheet, begin_row, col):
        row = begin_row
        while True:
            v = sheet.range(row, col).value
            if v is None:
                break
            v = v.strip()
            if v == '':
                break

    @staticmethod
    def _on_load_config_branches(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_alias_projects(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_teams(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_alias_teams(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_users(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_user_alias_teams(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_types(sheet, begin_row, col):
        pass

    @staticmethod
    def _on_load_config_columns(sheet, begin_row, col):
        pass

    # loader map
    CONFIG_LOADER = {
        NAME_PROJECTS: _on_load_config_projects,
        NAME_BRANCHES: _on_load_config_branches,
        NAME_ALIAS_PROJECTS: _on_load_config_alias_projects,
        NAME_TEAMS: _on_load_config_teams,
        NAME_ALIAS_TEAMS: _on_load_config_alias_teams,
        NAME_USERS: _on_load_config_users,
        NAME_USER_ALIAS_TEAMS: _on_load_config_user_alias_teams,
        NAME_TYPES: _on_load_config_types,
        NAME_COLUMNS: _on_load_config_columns
    }

