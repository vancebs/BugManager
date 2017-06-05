#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ttk import *
from Tkconstants import *


class ProgressView(Frame):
    def __init__(self, title, master=None, **kw):
        Frame.__init__(self, master, **kw)

        frame_label = Frame(self)
        frame_label.pack(fill=X, side=TOP)

        label_title = Label(frame_label, text=title)
        label_title.pack(fill=X, side=LEFT)

        label_progress = Label(frame_label)
        label_progress.pack(fill=X, side=LEFT)

        progressbar = Progressbar(self, orient="horizontal")
        progressbar.pack(fill=X, side=TOP)

        # save as global
        self._mLabelProgress = label_progress
        self._mProgressBar = progressbar

    def set_progress(self, curr_progress, max_progress=None):
        if max_progress is not None:
            self._mProgressBar.config(maximum=max_progress)
        self._mProgressBar.config(value=curr_progress)
        self._mLabelProgress.config(
            text='(%d/%d)' % (self._mProgressBar['value'], self._mProgressBar['maximum']))
