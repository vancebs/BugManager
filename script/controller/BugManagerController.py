#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkMessageBox
from script.view.SyncProgressView import SyncProgressView
from script.controller.SyncProgressController import SyncProgressController
from script.controller.command.CmdSync import CmdSync
from script.controller.command.CmdOpen import CmdOpen
from script.controller.command.CmdView import CmdView
from script.controller.command.CmdEdit import CmdEdit
from script.controller.command.CmdCreate import CmdCreate


class BugManagerController(object):
    def cmd_open(self, view):
        print ('cmd_open')
        cmd = CmdOpen(view)
        cmd.start()

    def cmd_sync(self, view, force_update=False):
        print ('cmd_sync start (force_update: %d) ...' % force_update)

        # create & show progress dialog
        progress_view = SyncProgressView(view, SyncProgressController(view))
        progress_view.reset()
        progress_view.show()

        # define callbacks
        def on_project_progress(progress, max_progress):
            progress_view.set_projects_progress(progress, max_progress)

        def on_sync_data_progress(progress, max_progress):
            progress_view.set_parser_bug_raw_progress(progress, max_progress)

        def on_sync_raw_progress(progress, max_progress):
            progress_view.set_fetch_bug_raw_progress(progress, max_progress)

        # run command
        cmd = CmdSync(
            on_project_progress=on_project_progress,
            on_sync_data_progress=on_sync_data_progress,
            on_sync_raw_progress=on_sync_raw_progress,
            force_update=force_update)
        cmd.start(True, self._on_cmd_sync_finished, progress_view)

    def _on_cmd_sync_finished(self, progress_view):
        progress_view.dismiss(1000)  # dismiss progress view
        print ('cmd_sync done')

    def cmd_view(self, view):
        print ('cmd_view')
        cmd = CmdView(view)
        cmd.start()

    def cmd_edit(self, view):
        print ('cmd_edit')
        cmd = CmdEdit(view)
        cmd.start()

    def cmd_create(self, view):
        print ('cmd_create')
        cmd = CmdCreate(view)
        cmd.start()

