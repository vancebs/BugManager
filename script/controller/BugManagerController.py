#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
import tkMessageBox
from IBugManagerController import IBugManagerController
from script.controller.command.CmdSync import CmdSync
from script.controller.command.CmdSyncAll import CmdSyncAll


class BugManagerController(IBugManagerController):
    def __init__(self):
        self._mCmd = None

    def cmd_sync(self, view):
        if self._mCmd:
            yes = tkMessageBox.askyesno(title='Cancel', message='Cancel may loose data, Are you sure?')
            if yes:
                self._mCmd.cancel()
        else:
            print ('cmd_sync start ...')
            view['text'] = 'Sync\nCancel'
            self._mCmd = CmdSync()
            self._mCmd.start(True, self._on_cmd_sync_finished, view)

    def _on_cmd_sync_finished(self, view):
        view['text'] = 'Sync'
        self._mCmd = None
        print ('cmd_sync done')

    def cmd_sync_all(self, view):
        if self._mCmd:
            yes = tkMessageBox.askyesno(title='Cancel', message='Cancel may loose data, Are you sure?')
            if yes:
                self._mCmd.cancel()
        else:
            print ('cmd_sync_all start ...')
            view['text'] = 'Sync All\nCancel'
            self._mCmd = CmdSyncAll()
            self._mCmd.start(True, self._on_cmd_sync_all_finished, view)

    def _on_cmd_sync_all_finished(self, view):
        view['text'] = 'Sync All'
        self._mCmd = None
        print ('cmd_sync_all done')

    def cmd_view(self, view):
        print ('cmd_view')

    def cmd_edit(self, view):
        print ('cmd_edit')
