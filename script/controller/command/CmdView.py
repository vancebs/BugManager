#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkSimpleDialog
from ICommand import ICommand
from script.model.local_alm.im.ImHandler import ImHandler


class CmdView(ICommand):
    def __init__(self, parent_view, bug_id=None):
        ICommand.__init__(self)
        self._mParentView = parent_view
        self._mBugId = bug_id

    def on_start(self):
        bug_id = self._mBugId
        if bug_id is None:
            bug_id = tkSimpleDialog.askinteger('View bug', 'Input bug ID to View.')

        if bug_id is not None:
            ImHandler.view_bug_gui(bug_id)

    def on_cancel(self):
        pass
