#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os
import sqlite3


class Database(object):
    _PATTERN_DIR_NAME = re.compile(r'([\s\S]*)[/\\]([\s\S]+)')

    def __init__(self, db_path, version):
        self._mVersion = version
        self._mDbPath = db_path
        g = self._PATTERN_DIR_NAME.match(self._mDbPath)
        self._mDbDir = g.group(1)
        self._mDbFilename = g.group(2)

    # remove the database file
    def remove(self):
        if os.path.exists(self._mDbPath):
            os.remove(self._mDbPath)

    def open(self):
        # make dirs if not exists
        if os.path.exists(self._mDbDir):
            if os.path.isfile(self._mDbDir):
                raise IOError('invalid database dir on an existing file. dir: %s.' % self._mDbDir)
        else:
            os.makedirs(self._mDbDir)

        # open database
        new_db = not os.path.exists(self._mDbPath)
        db = sqlite3.connect(self._mDbPath)
        db.text_factory = str
        if new_db:
            # create version table
            Database._create_version_table(db)

            # call child implementation
            self._on_create(db)

            ver = 0  # version 0 for new database
        else:
            # get version from database
            ver = Database._get_db_version(db)

        # check for update
        if ver < self._mVersion:
            v = self._on_upgrade(db, ver, self._mVersion)
            # update version
            Database._set_db_version(db, v)
        db.commit()
        return db

    def _on_create(self, db):
        # should be implemented by child
        pass

    def _on_upgrade(self, db, current_ver, target_ver):
        # should be implemented by child
        pass

    @staticmethod
    def _create_version_table(db):
        db.execute('CREATE TABLE version (ver INTEGER)')
        db.execute('INSERT INTO version (ver) VALUES (?)', (0,))
        db.commit()

    @staticmethod
    def _get_db_version(db):
        c = db.cursor()
        c.execute('SELECT ver from version')
        row = c.fetchone()
        ver = 0
        if row:
            ver = row[0]
        c.close()
        return ver

    @staticmethod
    def _set_db_version(db, version):
        db.execute('UPDATE version set ver=?', (version,))
        db.commit()
