#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkconstants import *
from View import View
from ModalDialogView import ModalDialogView
from ProgressView import ProgressView


class SyncProgressView(ModalDialogView):
    def __init__(self, parent, controller):
        self.progress_projects = None
        self.progress_fetch_bug_raw = None
        self.progress_parser_bug_raw = None

        ModalDialogView.__init__(self, parent, controller)

    def on_create_view(self, root, controller):
        root.geometry('400x170')

        ######################
        # projects
        progress_projects = ProgressView('Projects', self)
        progress_projects.pack(fill=X,
                               padx=View.BUTTON_PADDING_X,
                               pady=View.BUTTON_PADDING_Y,
                               side=TOP)

        ##################
        # fetch bug raw
        progress_fetch_bug_raw = ProgressView('Fetch bug raw detail', root)
        progress_fetch_bug_raw.pack(fill=X,
                                    padx=View.BUTTON_PADDING_X,
                                    pady=View.BUTTON_PADDING_Y,
                                    side=TOP)

        ################
        # parser bug detail
        progress_parser_bug_raw = ProgressView('Parser bug detail', root)
        progress_parser_bug_raw.pack(fill=X,
                                     padx=View.BUTTON_PADDING_X,
                                     pady=View.BUTTON_PADDING_Y,
                                     side=TOP)

        # save global params
        self.progress_projects = progress_projects
        self.progress_fetch_bug_raw = progress_fetch_bug_raw
        self.progress_parser_bug_raw = progress_parser_bug_raw

    def reset(self):
        self.set_projects_progress(0, 0)
        self.set_fetch_bug_raw_progress(0, 0)
        self.set_parser_bug_raw_progress(0, 0)

    def set_projects_progress(self, progress, max_progress=None):
        self.after_idle(lambda: self.progress_projects.set_progress(progress, max_progress))

    def set_fetch_bug_raw_progress(self, progress, max_progress=None):
        self.after_idle(lambda: self.progress_fetch_bug_raw.set_progress(progress, max_progress))

    def set_parser_bug_raw_progress(self, progress, max_progress=None):
        self.after_idle(lambda: self.progress_parser_bug_raw.set_progress(progress, max_progress))
