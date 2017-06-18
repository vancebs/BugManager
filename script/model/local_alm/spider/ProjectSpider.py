#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

from script.model.local_alm.cfg.Config import Config
from script.model.local_alm.db.ProjectDatabase import ProjectDatabase
from script.model.local_alm.im.Im import Im
from script.model.local_alm.im.ImHandler import ImHandler
from script.model.local_alm.util.TimeUtil import TimeUtil
from script.model.local_alm.util.MultiThreadRunner import MultiThreadRunner


class ProjectSpider(object):
    _DIVIDER = '==***=='
    _FROM_TIME_SHIFT = 30 * 60  # 30 min
    _COMMIT_THRESHOLD_FOR_RAW = 200
    _REG_MATCH_FIELD_NAME = re.compile('([\s\S]+?):([\s\S]*)')

    _SQL_INSERT_BUGS = (
        'INSERT OR IGNORE INTO '
        + ProjectDatabase.TABLE_BUGS + ' ('
        + ProjectDatabase.COL_BUGS_BUG_ID
        + ',' + ProjectDatabase.COL_BUGS_MODIFIED_TIME
        + ',' + ProjectDatabase.COL_BUGS_DIRTY
        + ') VALUES (?,?,?)'
    )

    _SQL_UPDATE_BUGS = (
        'UPDATE '
        + ProjectDatabase.TABLE_BUGS
        + ' SET '
        + ProjectDatabase.COL_BUGS_MODIFIED_TIME + '=?,'
        + ProjectDatabase.COL_BUGS_DIRTY + '=?'
        + ' WHERE '
        + ProjectDatabase.COL_BUGS_BUG_ID + '=?'
    )

    _SQL_QUERY_BUGS_DIRTY = (
        'SELECT '
        + ProjectDatabase.COL_BUGS_BUG_ID
        + ',' + ProjectDatabase.COL_BUGS_MODIFIED_TIME
        + ' FROM '
        + ProjectDatabase.TABLE_BUGS
        + ' WHERE '
        + ProjectDatabase.COL_BUGS_DIRTY + '=1'
    )

    _SQL_UPDATE_BUGS_DIRTY = (
        'UPDATE '
        + ProjectDatabase.TABLE_BUGS
        + ' SET '
        + ProjectDatabase.COL_BUGS_DIRTY + '=?'
        + ' WHERE '
        + ProjectDatabase.COL_BUGS_BUG_ID + "=?"
    )

    _SQL_INSERT_RAW = (
        'INSERT OR IGNORE INTO '
        + ProjectDatabase.TABLE_RAW + ' ('
        + ProjectDatabase.COL_RAW_BUG_ID
        + ',' + ProjectDatabase.COL_RAW_MODIFIED_TIME
        + ',' + ProjectDatabase.COL_RAW_DATA
        + ',' + ProjectDatabase.COL_RAW_DIRTY
        + ') VALUES (?,?,?,?)'
    )

    _SQL_UPDATE_RAW = (
        'UPDATE '
        + ProjectDatabase.TABLE_RAW
        + ' SET '
        + ProjectDatabase.COL_RAW_MODIFIED_TIME + '=?,'
        + ProjectDatabase.COL_RAW_DATA + '=?,'
        + ProjectDatabase.COL_RAW_DIRTY + '=?'
        + ' WHERE '
        + ProjectDatabase.COL_RAW_BUG_ID + '=?'
    )

    _SQL_CHECK_BUGS_DIRTY = (
        'UPDATE '
        + ProjectDatabase.TABLE_BUGS
        + ' SET '
        + ProjectDatabase.COL_BUGS_DIRTY + '=0'
        + ' WHERE '
        + ProjectDatabase.TABLE_BUGS + '.' + ProjectDatabase.COL_BUGS_BUG_ID + '=('
        + ' SELECT '
        + ProjectDatabase.COL_RAW_BUG_ID
        + ' FROM '
        + ProjectDatabase.TABLE_RAW
        + ' WHERE '
        + ProjectDatabase.TABLE_RAW + '.' + ProjectDatabase.COL_RAW_BUG_ID
        + '='
        + ProjectDatabase.TABLE_BUGS + '.' + ProjectDatabase.COL_BUGS_BUG_ID
        + ' AND '
        + ProjectDatabase.TABLE_RAW + '.' + ProjectDatabase.COL_RAW_MODIFIED_TIME
        + '='
        + ProjectDatabase.TABLE_BUGS + '.' + ProjectDatabase.COL_BUGS_MODIFIED_TIME
        + ')'
    )

    _SQL_QUERY_RAW_DIRTY = (
        'SELECT '
        + ProjectDatabase.COL_RAW_BUG_ID
        + ',' + ProjectDatabase.COL_RAW_DATA
        + " FROM "
        + ProjectDatabase.TABLE_RAW
        + ' WHERE '
        + ProjectDatabase.COL_RAW_DIRTY + '=1'
    )

    _SQL_INSERT_DATA = (
        'INSERT OR IGNORE INTO ' + ProjectDatabase.TABLE_DATA + ' ('
        + ProjectDatabase.COL_DATA_BUG_ID
        + ',' + ProjectDatabase.COL_DATA_NAME
        + ',' + ProjectDatabase.COL_DATA_VALUE
        + ') VALUES (?,?,?)'
    )

    _SQL_UPDATE_DATA = (
        'UPDATE '
        + ProjectDatabase.TABLE_DATA
        + ' SET '
        + ProjectDatabase.COL_DATA_VALUE + '=?'
        + ' WHERE '
        + ProjectDatabase.COL_DATA_BUG_ID + '=?'
        + ' AND '
        + ProjectDatabase.COL_DATA_NAME + '=?'
    )

    _SQL_DELETE_DATA = (
        'DELETE FROM '
        + ProjectDatabase.TABLE_DATA
        + ' WHERE '
        + ProjectDatabase.COL_DATA_BUG_ID + '=?'
        + ' AND '
        + ProjectDatabase.COL_DATA_NAME + '=?'
    )

    _SQL_QUERY_DATA_WITH_ALM_ID = (
        'SELECT '
        + ProjectDatabase.COL_DATA_NAME
        + ',' + ProjectDatabase.COL_DATA_VALUE
        + ' FROM '
        + ProjectDatabase.TABLE_DATA
        + ' WHERE '
        + ProjectDatabase.COL_DATA_BUG_ID + '=?'
    )

    _SQL_UPDATE_RAW_DIRTY = (
        'UPDATE '
        + ProjectDatabase.TABLE_RAW
        + ' SET '
        + ProjectDatabase.COL_RAW_DIRTY + '=?'
        + ' WHERE '
        + ProjectDatabase.COL_RAW_BUG_ID + "=?"
    )

    def __init__(self, project):
        self._mMultiThreadRunner = None
        self._mCanceled = False

        self._mConfig = Config()
        self._mProject = project
        self._mDatabase = ProjectDatabase(self._mProject)

        self._mDictFieldDisplayName2Type = None
        self._mDictFieldDisplayName2Name = None
        self._mDictUsersAssignedUserName2Email = None

    def cancel(self):
        if self._mMultiThreadRunner:
            self._mMultiThreadRunner.cancel()
        self._mCanceled = True

    def is_canceled(self):
        return self._mCanceled

    def sync(self, on_sync_raw_progress=None, on_sync_data_progress=None, total_fetch=False):
        self._mCanceled = False

        (self._mDictFieldDisplayName2Type, self._mDictFieldDisplayName2Name) = self._mConfig.get_fields_dict()
        self._mDictUsersAssignedUserName2Email = self._mConfig.get_users_dict()
        self.sync_bugs(total_fetch)
        self.sync_raw(on_sync_raw_progress)
        self.sync_data(on_sync_data_progress)

    def sync_bugs(self, total_fetch=False):
        print('sync bugs ...')

        # save query time
        query_time = TimeUtil.current_time()

        # get sync from time
        if total_fetch:
            sync_from_time = Config.EARLY_SYNC_TIME
        else:
            sync_from_time = self._mConfig.get_project_last_update_time(self._mProject)

        print('\t', 'fetch bug from last modified time [%s]' % TimeUtil.format_time_to_str(sync_from_time))

        with self._open_database() as db:
            # query from im
            (result, count) = ImHandler.sync_bugs(
                self._mProject, sync_from_time,
                lambda bug_id, modified_time:
                db.execute(self._SQL_INSERT_BUGS,
                           (bug_id, TimeUtil.format_time_to_float(modified_time), 1)).rowcount <= 0
                    and db.execute(self._SQL_UPDATE_BUGS, (TimeUtil.format_time_to_float(modified_time), 1, bug_id))
            )

            # check result
            if result:
                print('\t', '[%d] bugs updated.' % count)
                last_modified_time = TimeUtil.time_sub(query_time, ProjectSpider._FROM_TIME_SHIFT)
                self._mConfig.set_project_last_update_time(self._mProject, last_modified_time)
            else:
                print('\t', 'fetch bugs failed')

            db.commit()

        print('\t', 'done')
        return result

    def sync_raw(self, on_sync_raw_progress=None, thread_count=10):
        print('sync raw ...')
        if thread_count < 1:
            thread_count = 1

        with self._open_database() as db:
            # check dirty bugs in table [bugs]. And set not dirty if it is not really dirty
            db.execute(self._SQL_CHECK_BUGS_DIRTY)

            # query dirty bugs
            c = db.cursor()
            c.execute(self._SQL_QUERY_BUGS_DIRTY)
            rows = c.fetchall()
            c.close()

            # fetch detail for each dirty bugs
            count = 0
            total = len(rows)

            print('\t', '[%d] raw bug info should be fetched.' % total)

            # notify progress
            if on_sync_raw_progress is not None:
                on_sync_raw_progress(0, total)

            # do fetch raw
            if not self.is_canceled():
                # run in multi thread
                self._mMultiThreadRunner = MultiThreadRunner(
                    thread_count,
                    self._sync_raw_thread_run,
                    (db, on_sync_raw_progress, total))
                self._mMultiThreadRunner.start(rows)

                # get result queue and save data into database
                queue = self._mMultiThreadRunner.get_result_queue()
                while True:
                    result = queue.get()
                    if result:
                        count += 1
                        self.save_raw(result)

                        alm_id = result['alm_id']
                        modified_time = result['modified_time']
                        if not result:
                            print('\t', '[Failed] fetching bug# [%d/%d] id: %s, modified: %s' % (
                                count, total, alm_id, modified_time))
                        else:
                            print('\t', '[Success] fetching bug# [%d/%d] id: %s, modified: %s' % (
                                count, total, alm_id, modified_time))

                            # commit to free memory
                            if count % ProjectSpider._COMMIT_THRESHOLD_FOR_RAW == 0:
                                db.commit()
                    else:
                        # we reach the last item
                        break

            if self.is_canceled():
                print('\t', 'canceled!')

            # close database
            db.commit()

        # notify progress
        if on_sync_raw_progress is not None:
            on_sync_raw_progress(total, total)

        print('\t', 'done')
        return True

    def _sync_raw_thread_run(self, args, global_params):
        alm_id = args[0]
        modified_time = args[1]
        db = global_params[0]     # db
        on_sync_raw_progress = global_params[1]  # on_sync_raw_progress
        total = global_params[2]  # total progress

        # fetch issue detail
        (code, out, err) = ProjectSpider.fetch_raw(alm_id)

        result = dict()
        result['alm_id'] = alm_id
        result['db'] = db
        result['modified_time'] = modified_time
        result['code'] = code
        result['out'] = out
        result['err'] = err

        # notify progress
        if on_sync_raw_progress is not None:
            on_sync_raw_progress(self._mMultiThreadRunner.get_finished_task_count() + 1, total)

        return result

    def sync_data(self, on_sync_data_progress=None):
        print('sync data ...')

        with self._open_database() as db:
            c = db.cursor()
            c.execute(self._SQL_QUERY_RAW_DIRTY)
            rows = c.fetchall()
            c.close()

            count = 0
            total = len(rows)

            # notify progress of data
            if on_sync_data_progress is not None:
                on_sync_data_progress(0, total)

            for row in rows:
                if self.is_canceled():
                    print('canceled!')
                    break

                count += 1
                bug_id = row[0]
                data = row[1]

                # get new & old data
                new_data = self._parse_raw_data(data)
                old_data = ProjectSpider._read_old_data(bug_id, db)

                # compare new & old data. find out fields should be inserted, updated, deleted
                to_insert = []
                to_update = []
                to_delete = list(old_data.keys())
                for key in new_data.keys():
                    if key in old_data:
                        to_update.append(key)
                    else:
                        to_insert.append(key)
                    try:
                        to_delete.remove(key)
                    except ValueError:
                        # key not found in to_delete. it's OK
                        pass

                print('\t', 'parsing from raw# [%d] ID: %s, insert: %d, update: %d, delete: %d' %
                      (count, bug_id, len(to_insert), len(to_update), len(to_delete)))

                # update database
                for name in to_insert:
                    db.execute(self._SQL_INSERT_DATA, (bug_id, name, new_data[name]))
                for name in to_update:
                    db.execute(self._SQL_UPDATE_DATA, (new_data[name], bug_id, name))
                for name in to_delete:
                    db.execute(self._SQL_DELETE_DATA, (bug_id, name))

                # mark not dirty
                db.execute(self._SQL_UPDATE_RAW_DIRTY, (0, bug_id))

                # commit to free memory
                if count % ProjectSpider._COMMIT_THRESHOLD_FOR_RAW == 0:
                    db.commit()

                # notify progress of data
                if on_sync_data_progress is not None:
                    on_sync_data_progress(count, total)

            print('\t', '[%d] parser from raw finished.' % count)

            # close cursor & database
            db.commit()

        # notify progress of data
        if on_sync_data_progress is not None:
            on_sync_data_progress(total, total)

        print('\t', 'done')

    def _parse_raw_data(self, raw):
        # check parameter raw
        if not isinstance(raw, str):
            raise TypeError('Invalid type of parameter raw')

        # parser lines
        data = dict()
        l_name = None
        l_value = []
        lines = raw.splitlines(False)
        for line in lines:
            line = line.strip()
            if len(line) <= 0:
                # ignore empty lines
                continue

            # try get field name
            (name, value) = self._parse_line_field(line)
            if name is None:
                l_value.append(line)
            else:
                # we get a new field name. save last one first
                if l_name is not None and len(l_value) > 0:
                    # save into data dict if value is not empty
                    data[l_name] = '\n'.join(l_value)

                # save name to l_name & reset l_value
                l_name = name
                l_value = []

                # save value into l_value if exists
                if value is not None:
                    l_value.append(value)

        if l_name is not None and len(l_value) > 0:
            data[l_name] = '\n'.join(l_value)

        return data

    @staticmethod
    def _read_old_data(alm_id, db):
        data = dict()

        # query from database
        c = db.cursor()
        c.execute(ProjectSpider._SQL_QUERY_DATA_WITH_ALM_ID, (alm_id,))
        row = c.fetchone()
        while row:
            data[row[0]] = row[1]
            row = c.fetchone()

        # close cursor
        c.close()

        return data

    def _insert_data_field(self, db, bug_id, name, value):
        if len(value) <= 0:
            # skip fields without value
            return

        # print ('name: %s, value: %s' % (name, '\n'.join(value)))
        # insert field
        v = '\n'.join(value)
        ret = db.execute(self._SQL_INSERT_DATA, (bug_id, name, v))
        if ret.rowcount <= 0:
            db.execute(self._SQL_UPDATE_DATA, (v, bug_id, name))

    def _parse_line_field(self, line):
        r = ProjectSpider._REG_MATCH_FIELD_NAME.match(line)
        if r is None:
            return None, None
        else:
            groups = r.groups()
            if len(groups) <= 0:
                return None, None
            else:
                field_name = groups[0].strip()
                if field_name in self._mDictFieldDisplayName2Type:
                    if len(groups) == 1:
                        return field_name, None
                    else:
                        field_value = groups[1].strip()
                        if len(field_value) <= 0:
                            field_value = None
                        return field_name, field_value
                else:
                    return None, None

    @staticmethod
    def fetch_raw(alm_id):
        # fetch bug detail from im
        return Im.execute('im viewissue --showRichContent %s' % alm_id)

    def save_raw(self, args):
        self.save_raw_2(args['alm_id'], args['db'], args['modified_time'], args['code'], args['out'], args['err'])

    def save_raw_2(self, alm_id, db, modified_time, code, out, err):
        # insert bug detail into database
        if code == 0:  # im command success
            # mark bug not dirty
            db.execute(self._SQL_UPDATE_BUGS_DIRTY, (0, alm_id))

            # insert or update bug detail
            ret = db.execute(self._SQL_INSERT_RAW, (alm_id, modified_time, out, 1))
            if ret.rowcount <= 0:
                db.execute(self._SQL_UPDATE_RAW, (modified_time, out, 1, alm_id))
        else:
            print('failed to fetch bug %s\n%s' % (alm_id, err))
            return False

        return True

    def _open_database(self):
        return self._mDatabase.open()
