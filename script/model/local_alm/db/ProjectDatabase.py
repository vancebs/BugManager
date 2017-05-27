#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.model.local_alm.cfg.Config import Config
from script.model.local_alm.db.Database import Database


class ProjectDatabase(Database):
    _VERSION = 2

    TABLE_BUGS = 'bugs'
    TABLE_RAW = 'raw'
    TABLE_DATA = 'data'
    TABLE_COMMENT = 'comment'

    INDEX_DATA_ID_NAME = 'data_id_name_index'

    COL_BUGS_BUG_ID = 'bug_id'
    COL_BUGS_MODIFIED_TIME = 'modified_time'
    COL_BUGS_DIRTY = 'dirty'

    COL_RAW_BUG_ID = 'bug_id'
    COL_RAW_MODIFIED_TIME = 'modified_time'
    COL_RAW_DATA = 'data'
    COL_RAW_DIRTY = 'dirty'

    COL_DATA_ID = 'id'
    COL_DATA_BUG_ID = 'bug_id'
    COL_DATA_NAME = 'name'
    COL_DATA_VALUE = 'value'

    COL_COMMENT_BUG_ID = 'bug_id'
    COL_COMMENT_COMMENT_0 = 'comment0'
    COL_COMMENT_COMMENT_1 = 'comment1'
    COL_COMMENT_COMMENT_2 = 'comment2'
    COL_COMMENT_COMMENT_3 = 'comment3'

    def __init__(self, project):
        Database.__init__(self, Config.project_db_path(project), ProjectDatabase._VERSION)

    def _on_create(self, db):
        pass

    def _on_upgrade(self, db, current_ver, target_ver):
        print ('upgrading project database [%d => %d] [%s] ...' % (current_ver, target_ver, self._mDbPath))

        # 0 => 1
        if current_ver == 0:
            # init database
            db.execute('CREATE TABLE ' + ProjectDatabase.TABLE_BUGS + ' ('
                       + ProjectDatabase.COL_BUGS_BUG_ID + ' INTEGER PRIMARY KEY,'
                       + ProjectDatabase.COL_BUGS_MODIFIED_TIME + ' REAL,'
                       + ProjectDatabase.COL_BUGS_DIRTY + ' INTEGER'
                       + ')')
            db.execute('CREATE TABLE ' + ProjectDatabase.TABLE_RAW + ' ('
                       + ProjectDatabase.COL_RAW_BUG_ID + ' INTEGER PRIMARY KEY,'
                       + ProjectDatabase.COL_RAW_MODIFIED_TIME + ' REAL,'
                       + ProjectDatabase.COL_RAW_DATA + ' BLOB,'
                       + ProjectDatabase.COL_RAW_DIRTY + ' INTEGER'
                       + ')')
            db.execute('CREATE TABLE ' + ProjectDatabase.TABLE_DATA + ' ('
                       + ProjectDatabase.COL_DATA_ID + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
                       + ProjectDatabase.COL_DATA_BUG_ID + ' INTEGER,'
                       + ProjectDatabase.COL_DATA_NAME + ' TEXT,'
                       + ProjectDatabase.COL_DATA_VALUE + ' TEXT'
                       + ')')
            db.execute('CREATE UNIQUE INDEX ' + ProjectDatabase.INDEX_DATA_ID_NAME + ' ON '
                       + ProjectDatabase.TABLE_DATA + '('
                       + ProjectDatabase.COL_DATA_BUG_ID
                       + ',' + ProjectDatabase.COL_DATA_NAME
                       + ')')

            current_ver += 1

        # 1 => 2
        if current_ver == 1:
            # add comment table
            db.execute('CREATE TABLE ' + ProjectDatabase.TABLE_COMMENT + ' ('
                       + ProjectDatabase.COL_COMMENT_BUG_ID + ' TEXT PRIMARY KEY,'
                       + ProjectDatabase.COL_COMMENT_COMMENT_0 + ' TEXT,'
                       + ProjectDatabase.COL_COMMENT_COMMENT_1 + ' TEXT,'
                       + ProjectDatabase.COL_COMMENT_COMMENT_2 + ' TEXT,'
                       + ProjectDatabase.COL_COMMENT_COMMENT_3 + ' TEXT'
                       + ')')

            current_ver += 1

        print ('\tdone')
        return current_ver

