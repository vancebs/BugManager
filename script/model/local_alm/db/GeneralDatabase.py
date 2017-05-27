#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.model.local_alm.cfg.Config import Config
from script.model.local_alm.db.Database import Database


class GeneralDatabase(Database):
    _VERSION = 2

    TABLE_FIELDS = 'fields'
    COL_FIELDS_ID = 'id'
    COL_FIELDS_NAME = 'name'
    COL_FIELDS_DISPLAY_NAME = 'display_name'
    COL_FIELDS_TYPE = 'type'
    INDEX_FIELDS_NAME = 'fields_name_index'

    TABLE_USERS = 'users'
    COL_USERS_ID = 'id'
    COL_USERS_NAME = 'name'
    COL_USERS_FULLNAME = 'fullname'
    COL_USERS_EMAIL = 'email'
    COL_USERS_ASSIGNED_USER_NAME = 'assigned_user_name'
    INDEX_USERS_NAME = 'users_name_index'

    TABLE_CONFIG = 'config'
    COL_CONFIG_ID = 'id'
    COL_CONFIG_PROJECT = 'project'
    COL_CONFIG_NAME = 'name'
    COL_CONFIG_VALUE = 'value'
    INDEX_CONFIG_PROJECT_NAME = 'config_project_name_index'

    TABLE_PROJECTS = 'projects'
    COL_PROJECTS_ID = 'id'
    COL_PROJECTS_NAME = 'name'
    COL_PROJECTS_IS_ACTIVE = 'isActive'
    COL_PROJECTS_FLAG_SYNC = 'flag_sync'
    COL_PROJECTS_LAST_UPDATE_TIME = 'last_update_time'
    INDEX_PROJECTS_NAME = 'projects_name_index'

    def __init__(self):
        Database.__init__(self, Config.general_db_path(), GeneralDatabase._VERSION)

    def _on_create(self, db):
        # should be implemented by child
        pass

    def _on_upgrade(self, db, current_ver, target_ver):
        print ('upgrading general database [%d => %d] ...' % (current_ver, target_ver))

        # 0 => 1
        if current_ver == 0:
            db.execute('CREATE TABLE ' + GeneralDatabase.TABLE_FIELDS + ' ('
                       + GeneralDatabase.COL_FIELDS_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
                       + GeneralDatabase.COL_FIELDS_NAME + ' TEXT,'
                       + GeneralDatabase.COL_FIELDS_DISPLAY_NAME + ' TEXT,'
                       + GeneralDatabase.COL_FIELDS_TYPE + ' TEXT'
                       + ')')
            db.execute('CREATE UNIQUE INDEX ' + GeneralDatabase.INDEX_FIELDS_NAME + ' ON '
                       + GeneralDatabase.TABLE_FIELDS + ' ('
                       + GeneralDatabase.COL_FIELDS_NAME
                       + ')')
            db.execute('CREATE TABLE ' + GeneralDatabase.TABLE_USERS + ' ('
                       + GeneralDatabase.COL_USERS_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
                       + GeneralDatabase.COL_USERS_NAME + ' TEXT,'
                       + GeneralDatabase.COL_USERS_EMAIL + ' TEXT,'
                       + GeneralDatabase.COL_USERS_FULLNAME + ' TEXT,'
                       + GeneralDatabase.COL_USERS_ASSIGNED_USER_NAME + ' TEXT'
                       + ')')
            db.execute('CREATE UNIQUE INDEX ' + GeneralDatabase.INDEX_USERS_NAME + ' ON '
                       + GeneralDatabase.TABLE_USERS + ' ('
                       + GeneralDatabase.COL_USERS_NAME
                       + ')')
            db.execute('CREATE TABLE ' + GeneralDatabase.TABLE_CONFIG + ' ('
                       + GeneralDatabase.COL_CONFIG_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
                       + GeneralDatabase.COL_CONFIG_PROJECT + ' TEXT,'
                       + GeneralDatabase.COL_CONFIG_NAME + ' TEXT,'
                       + GeneralDatabase.COL_CONFIG_VALUE + ' TEXT'
                       + ')')
            db.execute('CREATE UNIQUE INDEX ' + GeneralDatabase.INDEX_CONFIG_PROJECT_NAME + ' ON '
                       + GeneralDatabase.TABLE_CONFIG + ' ('
                       + GeneralDatabase.COL_CONFIG_PROJECT
                       + ',' + GeneralDatabase.COL_CONFIG_NAME
                       + ')')

            current_ver += 1

        # 1 => 2
        if current_ver == 1:
            db.execute('CREATE TABLE ' + GeneralDatabase.TABLE_PROJECTS + ' ('
                       + GeneralDatabase.COL_PROJECTS_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
                       + GeneralDatabase.COL_PROJECTS_NAME + ' TEXT,'
                       + GeneralDatabase.COL_PROJECTS_IS_ACTIVE + ' INTEGER,'
                       + GeneralDatabase.COL_PROJECTS_FLAG_SYNC + ' INTEGER DEFAULT 0,'  # no sync as default
                       + GeneralDatabase.COL_PROJECTS_LAST_UPDATE_TIME + ' REAL DEFAULT 0'
                       + ')')
            db.execute('CREATE UNIQUE INDEX ' + GeneralDatabase.INDEX_PROJECTS_NAME + ' ON '
                       + GeneralDatabase.TABLE_PROJECTS + ' ('
                       + GeneralDatabase.COL_PROJECTS_NAME
                       + ')')

            current_ver += 1

        print ('\tdone')
        return current_ver
