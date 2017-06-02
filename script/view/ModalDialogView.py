#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from View import View
from abc import abstractmethod, ABCMeta


class ModalDialogView(View):
    __metaclass__ = ABCMeta

    def __init__(self, parent, controller):
        self.mParentView = parent
        self.mRootView = self.on_create_view(parent, controller)

    @abstractmethod
    def on_create_view(self, parent, controller):
        pass

    def dismiss(self):
        pass

    def show(self):
        self.mRootView.transient(self.mParentView)
        self.mRootView.focus_set()
        self.mRootView.grab_set()
        self.mRootView.wait_window()



