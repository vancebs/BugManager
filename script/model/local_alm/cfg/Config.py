#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.model.local_alm.util.Util import Util


class Config(object):
    # EARLY_SYNC_TIME = Util.format_time('2015-1-1 00:00:00')
    EARLY_SYNC_TIME = Util.format_time(0)

    PATH_DB_ROOT_DIR = 'database'
    PATH_DB_PROJECT_DIR = 'project'
    FILENAME_GENERAL_DB = 'General'
    EXT_DB = 'db'

    PROJECT_GENERAL = '__General'

    KEY_BUG_LAST_UPDATE_TIME = 'bug_last_update_time'
    KEY_FIELDS_LAST_UPDATE_TIME = 'fields_last_update_time'
    KEY_USERS_LAST_UPDATE_TIME = 'users_last_update_time'
    KEY_PROJECTS_LAST_UPDATE_TIME = 'projects_last_update_time'
    KEY_TYPES_LAST_UPDATE_TIME = 'types_last_update_time'

    @staticmethod
    def project_db_dir():
        return '%s/%s' % (Config.PATH_DB_ROOT_DIR, Config.PATH_DB_PROJECT_DIR)

    @staticmethod
    def project_db_path(project):
        if str(project).startswith('/'):
            return '%s%s.%s' % (Config.project_db_dir(), project, Config.EXT_DB)
        else:
            return '%s/%s.%s' % (Config.project_db_dir(), project, Config.EXT_DB)

    @staticmethod
    def general_db_dir():
        return Config.PATH_DB_ROOT_DIR

    @staticmethod
    def general_db_path():
        return '%s/%s.%s' % (Config.general_db_dir(), Config.FILENAME_GENERAL_DB, Config.EXT_DB)

    def __init__(self):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase

        self._mGeneralDatabase = GeneralDatabase()

    def _open_database(self):
        return self._mGeneralDatabase.open()

    def get_config(self, project, key, default, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._get_config_internal(project, key, default, db)
        else:
            return Config._get_config_internal(project, key, default, db)

    def set_config(self, project, key, value, db=None):
        if db is None:
            with self._open_database() as db:
                Config._set_config_internal(project, key, value, db)
        else:
            Config._set_config_internal(project, key, value, db)

    def get_general_config(self, key, default, db=None):
        return self.get_config(Config.PROJECT_GENERAL, key, default, db)

    def set_general_config(self, key, value, db=None):
        self.set_config(Config.PROJECT_GENERAL, key, value, db)

    # get last update time of fields list
    def get_fields_last_update_time(self, db=None):
        return self.get_general_config(Config.KEY_FIELDS_LAST_UPDATE_TIME, Config.EARLY_SYNC_TIME, db)

    # et last update time of fields list
    def set_fields_last_update_time(self, value, db=None):
        self.set_general_config(Config.KEY_FIELDS_LAST_UPDATE_TIME, Util.format_time_to_str(value), db)

    # get last update time of users list
    def get_users_last_update_time(self, db=None):
        return self.get_general_config(Config.KEY_USERS_LAST_UPDATE_TIME, Config.EARLY_SYNC_TIME, db)

    # set last update time of users list
    def set_users_last_update_time(self, value, db=None):
        self.set_general_config(Config.KEY_USERS_LAST_UPDATE_TIME, Util.format_time_to_str(value), db)

    # get last update time of users list
    def get_types_last_update_time(self, db=None):
        return self.get_general_config(Config.KEY_TYPES_LAST_UPDATE_TIME, Config.EARLY_SYNC_TIME, db)

    # set last update time of users list
    def set_types_last_update_time(self, value, db=None):
        self.set_general_config(Config.KEY_TYPES_LAST_UPDATE_TIME, Util.format_time_to_str(value), db)

    # get last update time of projects list
    def get_projects_last_update_time(self, db=None):
        return self.get_general_config(Config.KEY_PROJECTS_LAST_UPDATE_TIME, Config.EARLY_SYNC_TIME, db)

    # set last update time of projects list
    def set_projects_last_update_time(self, value, db=None):
        self.set_general_config(Config.KEY_PROJECTS_LAST_UPDATE_TIME, Util.format_time_to_str(value), db)

    # get last update time of a signal project
    def get_project_last_update_time(self, project, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._get_project_last_update_time_internal(project, db)
        else:
            return Config._get_project_last_update_time_internal(project, db)

    # set last update time of a signal project
    def set_project_last_update_time(self, project, value, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._set_project_last_update_time_internal(project, Util.format_time_to_float(value), db)
        else:
            return Config._set_project_last_update_time_internal(project, Util.format_time_to_float(value), db)

    def get_fields_dict(self, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._get_fields_dict_internal(db)
        else:
            return Config._get_fields_dict_internal(db)

    def get_users_dict(self, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._get_users_dict_internal(db)
        else:
            return Config._get_users_dict_internal(db)

    def get_recent_list(self, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._get_recent_list_internal(db)
        else:
            return Config._get_recent_list_internal(db)

    @staticmethod
    def _get_recent_list_internal(db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'SELECT '
            + GeneralDatabase.COL_RECENT_PATH
            + ' FROM '
            + GeneralDatabase.TABLE_RECENT
            + ' ORDER BY '
            + GeneralDatabase.COL_RECENT_ID
            + ' DESC'
        )

        # query
        c = db.cursor()
        c.execute(sql)

        # save result into a list
        l = []
        while True:
            row = c.fetchone()
            if row:
                l.append(row[0])
            else:
                break

        # close cursor
        c.close()

        return l


    def remove_recent(self, path, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._remove_recent_internal(path, db)
        else:
            return Config._remove_recent_internal(path, db)

    @staticmethod
    def _remove_recent_internal(path, db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'DELETE FROM '
            + GeneralDatabase.TABLE_RECENT
            + ' WHERE '
            + GeneralDatabase.COL_RECENT_PATH + '=?'
        )

        # do remove
        db.execute(sql, (path, ))
        db.commit()

    def add_recent(self, path, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._add_recent_internal(path, db)
        else:
            return Config._add_recent_internal(path, db)

    @staticmethod
    def _add_recent_internal(path, db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'INSERT OR IGNORE INTO ' + GeneralDatabase.TABLE_RECENT + ' ('
            + GeneralDatabase.COL_RECENT_PATH
            + ') VALUES (?)'
        )

        # do add
        db.execute(sql, (path, ))
        db.commit()

    def update_recent(self, path, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._update_recent_internal(path, db)
        else:
            return Config._update_recent_internal(path, db)

    @staticmethod
    def _update_recent_internal(path, db):
        Config._remove_recent_internal(path, db)
        Config._add_recent_internal(path, db)

    def has_recent(self, path, db=None):
        if db is None:
            with self._open_database() as db:
                return Config._has_recent_inteneral(path, db)
        else:
            return Config._has_recent_inteneral(path, db)

    @staticmethod
    def _has_recent_inteneral(path, db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'SELECT '
            + GeneralDatabase.COL_RECENT_ID
            + ' FROM '
            + GeneralDatabase.TABLE_RECENT
            + ' WHERE '
            + GeneralDatabase.COL_RECENT_PATH + '=?'
        )

        # query
        c = db.cursor()
        c.execute(sql, (path, ))
        has_recent = c.fetchone() is not None
        c.close()

        return has_recent

    @staticmethod
    def _get_config_internal(project, key, default, db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'SELECT '
            + GeneralDatabase.COL_CONFIG_VALUE
            + ' FROM '
            + GeneralDatabase.TABLE_CONFIG
            + ' WHERE '
            + GeneralDatabase.COL_CONFIG_PROJECT + '=?'
            + ' AND '
            + GeneralDatabase.COL_CONFIG_NAME + '=?'
        )

        result = default

        # read from database
        c = db.cursor()
        c.execute(sql, (project, key))
        row = c.fetchone()
        if row:
            result = row[0]

        # close cursor
        c.close()

        return result

    @staticmethod
    def _set_config_internal(project, key, value, db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql_insert = (
            'INSERT OR IGNORE INTO ' + GeneralDatabase.TABLE_CONFIG + ' ('
            + GeneralDatabase.COL_CONFIG_PROJECT
            + ',' + GeneralDatabase.COL_CONFIG_NAME
            + ',' + GeneralDatabase.COL_CONFIG_VALUE
            + ') VALUES (?,?,?)'
        )
        sql_update = (
            'UPDATE '
            + GeneralDatabase.TABLE_CONFIG
            + ' SET '
            + GeneralDatabase.COL_CONFIG_VALUE + '=?'
            + ' WHERE '
            + GeneralDatabase.COL_CONFIG_PROJECT + '=?'
            + ' AND '
            + GeneralDatabase.COL_CONFIG_NAME + '=?'
        )

        ret = db.execute(sql_insert, (project, key, value))
        if ret.rowcount <= 0:
            # update if no record inserted
            db.execute(sql_update, (value, project, key))

        db.commit()

    @staticmethod
    def _get_project_last_update_time_internal(project, db): # TODO
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'SELECT '
            + GeneralDatabase.COL_PROJECTS_LAST_UPDATE_TIME
            + ' FROM '
            + GeneralDatabase.TABLE_PROJECTS
            + ' WHERE '
            + GeneralDatabase.COL_PROJECTS_NAME + '=?'
        )

        # read from db
        result = Config.EARLY_SYNC_TIME
        c = db.cursor()
        c.execute(sql, (project,))
        row = c.fetchone()
        if row:
            result = row[0]

        # close cursor
        c.close()

        return result

    @staticmethod
    def _set_project_last_update_time_internal(project, last_update_time, db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'UPDATE '
            + GeneralDatabase.TABLE_PROJECTS
            + ' SET '
            + GeneralDatabase.COL_PROJECTS_LAST_UPDATE_TIME + '=?'
            + ' WHERE '
            + GeneralDatabase.COL_PROJECTS_NAME + '=?'
        )

        db.execute(sql, (last_update_time, project))
        db.commit()

    @staticmethod
    def _get_fields_dict_internal(db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'SELECT '
            + GeneralDatabase.COL_FIELDS_NAME
            + ',' + GeneralDatabase.COL_FIELDS_TYPE
            + ',' + GeneralDatabase.COL_FIELDS_DISPLAY_NAME
            + ' FROM '
            + GeneralDatabase.TABLE_FIELDS
        )

        # query from database
        c = db.cursor()
        c.execute(sql)
        row = c.fetchone()
        name_type = dict()
        name_display_name = dict()
        while row:
            r_name = row[0]
            r_type = row[1]
            r_display_name = row[2]
            name_type[r_display_name] = r_type
            name_display_name[r_display_name] = r_name
            row = c.fetchone()

        # close cursor
        c.close()

        return name_type, name_display_name

    @staticmethod
    def _get_users_dict_internal(db):
        from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
        sql = (
            'SELECT '
            + GeneralDatabase.COL_USERS_ASSIGNED_USER_NAME
            + ',' + GeneralDatabase.COL_USERS_EMAIL
            + ' FROM '
            + GeneralDatabase.TABLE_USERS
        )

        # query from database
        c = db.cursor()
        c.execute(sql)
        row = c.fetchone()
        assigned_email = dict()
        while row:
            assigned = row[0]
            email = row[1]
            assigned_email[assigned] = email
            row = c.fetchone()

        # close cursor
        c.close()

        return assigned_email
