#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.model.local_alm.cfg.Config import Config
from script.model.local_alm.db.GeneralDatabase import GeneralDatabase
from script.model.local_alm.im.ImHandler import ImHandler
from script.model.local_alm.util.Util import Util


class GeneralSpider(object):
    _SYNC_FREQUENCY = 24 * 60 * 60  # 1 day

    _SQL_INSERT_FIELDS = (
        'INSERT OR IGNORE INTO ' + GeneralDatabase.TABLE_FIELDS + ' ('
        + GeneralDatabase.COL_FIELDS_NAME
        + ',' + GeneralDatabase.COL_FIELDS_DISPLAY_NAME
        + ',' + GeneralDatabase.COL_FIELDS_TYPE
        + ') VALUES (?,?,?)'
    )

    _SQL_UPDATE_FIELDS = (
        'UPDATE '
        + GeneralDatabase.TABLE_FIELDS
        + ' SET '
        + GeneralDatabase.COL_FIELDS_DISPLAY_NAME + '=?,'
        + GeneralDatabase.COL_FIELDS_TYPE + '=?'
        + ' WHERE '
        + GeneralDatabase.COL_FIELDS_NAME + '=?'
    )

    _SQL_INSERT_USERS = (
        'INSERT OR IGNORE INTO ' + GeneralDatabase.TABLE_USERS + ' ('
        + GeneralDatabase.COL_USERS_NAME
        + ',' + GeneralDatabase.COL_USERS_EMAIL
        + ',' + GeneralDatabase.COL_USERS_FULLNAME
        + ',' + GeneralDatabase.COL_USERS_ASSIGNED_USER_NAME
        + ') VALUES (?,?,?,?)'
    )

    _SQL_UPDATE_USERS = (
        'UPDATE '
        + GeneralDatabase.TABLE_USERS
        + ' SET '
        + GeneralDatabase.COL_USERS_EMAIL + '=?,'
        + GeneralDatabase.COL_USERS_FULLNAME + '=?,'
        + GeneralDatabase.COL_USERS_ASSIGNED_USER_NAME + '=?'
        + ' WHERE '
        + GeneralDatabase.COL_USERS_NAME + '=?'

    )

    _SQL_INSERT_PROJECTS = (
        'INSERT OR IGNORE INTO '
        + GeneralDatabase.TABLE_PROJECTS + ' ('
        + GeneralDatabase.COL_PROJECTS_NAME
        + ',' + GeneralDatabase.COL_PROJECTS_IS_ACTIVE
        + ') VALUES (?,?)'
    )

    _SQL_UPDATE_PROJECTS = (
        'UPDATE '
        + GeneralDatabase.TABLE_PROJECTS
        + ' SET '
        + GeneralDatabase.COL_PROJECTS_IS_ACTIVE + '=?'
        + ' WHERE '
        + GeneralDatabase.COL_PROJECTS_NAME + '=?'
    )

    _SQL_INSERT_TYPES = (
        'INSERT OR IGNORE INTO '
        + GeneralDatabase.TABLE_TYPES + ' ('
        + GeneralDatabase.COL_TYPES_NAME
        + ') VALUES (?)'
    )

    # only one item, unnecessary to update
    # _SQL_UPDATE_TYPES =

    def __init__(self):
        self._mConfig = Config()
        self._mDatabase = GeneralDatabase()

    def _open_database(self):
        return self._mDatabase.open()

    def sync(self, force_update=False):
        self.sync_fields(force_update)
        self.sync_users(force_update)
        self.sync_types(force_update)
        self.sync_projects(force_update)

    def sync_fields(self, force_update=False):
        print ('sync fields ...')
        current_time = Util.current_time()

        # check force update
        if not force_update:
            # check frequency
            last_updated_time = self._mConfig.get_fields_last_update_time()
            delta_time = Util.time_sub(current_time, last_updated_time)
            if Util.format_time_to_float(delta_time) < GeneralSpider._SYNC_FREQUENCY:
                # unnecessary to sync if duration is less than frequency
                print ('\tcanceled. unnecessary to sync.')
                return

        # sync
        with self._open_database() as db:
            (result, count) = ImHandler.sync_fields(
                lambda name, display_name, field_type:
                    db.execute(GeneralSpider._SQL_INSERT_FIELDS, (name, display_name, field_type)).rowcount <= 0
                    and db.execute(GeneralSpider._SQL_UPDATE_FIELDS, (display_name, field_type, name)))

            # check result
            if result:
                print ('\t[%d] fields updated.' % count)

                # update last sync time
                self._mConfig.set_fields_last_update_time(current_time, db)
            else:
                print ('\tfetch fields failed')

        return result

    def sync_users(self, force_update=False):
        print ('sync users ...')
        current_time = Util.current_time()

        # check force update
        if not force_update:
            # check frequency
            last_updated_time = self._mConfig.get_users_last_update_time()
            delta_time = Util.time_sub(current_time, last_updated_time)
            if Util.format_time_to_float(delta_time) < GeneralSpider._SYNC_FREQUENCY:
                # unnecessary to sync if duration is less than frequency
                print ('\tcanceled. unnecessary to sync.')
                return

        # sync
        with self._open_database() as db:
            (result, count) = ImHandler.sync_users(
                lambda name, email, fullname, assigned_user_name:
                    db.execute(GeneralSpider._SQL_INSERT_USERS,
                               (name, email, fullname, assigned_user_name)).rowcount <= 0
                    and db.execute(GeneralSpider._SQL_UPDATE_USERS, (email, fullname, assigned_user_name, name)))

            # check result
            if result:
                print ('\t[%d] users updated.' % count)

                # update last sync time
                self._mConfig.set_users_last_update_time(current_time, db)
            else:
                print ('\tfetch users failed')

        return result

    def sync_projects(self, force_update=False):
        print ('sync projects ...')
        current_time = Util.current_time()

        # check force update
        if not force_update:
            # check frequency
            last_updated_time = self._mConfig.get_projects_last_update_time()
            delta_time = Util.time_sub(current_time, last_updated_time)
            if Util.format_time_to_float(delta_time) < GeneralSpider._SYNC_FREQUENCY:
                # unnecessary to sync if duration is less than frequency
                print ('\tcanceled. unnecessary to sync.')
                return

        # sync
        with self._open_database() as db:
            (result, count) = ImHandler.sync_projects(
                lambda name, is_active:
                    db.execute(GeneralSpider._SQL_INSERT_PROJECTS, (name, 0 if is_active == 'no' else 1)).rowcount <= 0
                    and db.execute(GeneralSpider._SQL_UPDATE_PROJECTS, (0 if is_active == 'no' else 1, name)))

            # check result
            if result:
                print ('\t[%d] projects updated.' % count)

                # update last sync time
                self._mConfig.set_projects_last_update_time(current_time, db)
            else:
                print ('\tfetch projects failed')

        return result

    def sync_types(self, force_update=False):
        print ('sync types ...')
        current_time = Util.current_time()

        # check force update
        if not force_update:
            # check frequency
            last_updated_time = self._mConfig.get_types_last_update_time()
            delta_time = Util.time_sub(current_time, last_updated_time)
            if Util.format_time_to_float(delta_time) < GeneralSpider._SYNC_FREQUENCY:
                # unnecessary to sync if duration is less than frequency
                print ('\tcanceled. unnecessary to sync.')
                return

        # sync
        with self._open_database() as db:
            (result, count) = ImHandler.sync_types(lambda name: db.execute(GeneralSpider._SQL_INSERT_TYPES, (name, )))

            # check result
            if result:
                print ('\t[%d] types updated.' % count)

                # update last sync time
                self._mConfig.set_types_last_update_time(current_time, db)
            else:
                print ('\tfetch types failed')

        return result
