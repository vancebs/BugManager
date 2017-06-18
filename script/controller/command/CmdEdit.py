#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter.simpledialog
from script.controller.command.ICommand import ICommand
from script.model.local_alm.im.ImHandler import ImHandler


class CmdEdit(ICommand):
    def __init__(self, parent_view, bug_id=None):
        ICommand.__init__(self)
        self._mParentView = parent_view
        self._mBugId = bug_id

    def on_start(self):
        bug_id = self._mBugId
        if bug_id is None:
            bug_id = tkinter.simpledialog.askinteger('Edit bug', 'Input bug ID to EDIT.')

        if bug_id is not None:
            ImHandler.edit_bug_gui(bug_id)

    def on_cancel(self):
        pass
