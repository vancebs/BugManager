#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
import tkMessageBox
from IBugManagerController import IBugManagerController
from script.controller.command.CmdSync import CmdSync
from script.controller.command.CmdSyncAll import CmdSyncAll
from script.controller.command.CmdOpen import CmdOpen


class BugManagerController(IBugManagerController):
    def __init__(self):
        self._mSyncCmd = None

    def cmd_open(self, view):
        print ('cmd_open')
        cmd = CmdOpen(view)
        cmd.start()

    def cmd_sync(self, view):
        if self._mSyncCmd:
            yes = tkMessageBox.askyesno(title='Cancel', message='Cancel may loose data, Are you sure?')
            if yes:
                if self._mSyncCmd:
                    self._mSyncCmd.cancel()
        else:
            print ('cmd_sync start ...')
            view['text'] = 'Sync\nCancel'
            self._mSyncCmd = CmdSync()
            self._mSyncCmd.start(True, self._on_cmd_sync_finished, view)

    def _on_cmd_sync_finished(self, view):
        view['text'] = 'Sync'
        self._mSyncCmd = None
        print ('cmd_sync done')

    def cmd_sync_all(self, view):
        if self._mSyncCmd:
            yes = tkMessageBox.askyesno(title='Cancel', message='Cancel may loose data, Are you sure?')
            if yes:
                if self._mSyncCmd:
                    self._mSyncCmd.cancel()
        else:
            print ('cmd_sync_all start ...')
            view['text'] = 'Sync All\nCancel'
            self._mSyncCmd = CmdSyncAll()
            self._mSyncCmd.start(True, self._on_cmd_sync_all_finished, view)

    def _on_cmd_sync_all_finished(self, view):
        view['text'] = 'Sync All'
        self._mSyncCmd = None
        print ('cmd_sync_all done')

    def cmd_view(self, view):
        print ('cmd_view')

    def cmd_edit(self, view):
        print ('cmd_edit')
