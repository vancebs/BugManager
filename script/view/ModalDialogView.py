#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import Toplevel
from View import View
from abc import abstractmethod, ABCMeta


class ModalDialogView(View, Toplevel):
    __metaclass__ = ABCMeta

    def __init__(self, parent, controller):
        Toplevel.__init__(self, parent)
        self.on_create_view(self, controller)

    @abstractmethod
    def on_create_view(self, root, controller):
        pass

    def dismiss(self, delay=None):
        if delay:
            self.after(delay, lambda: self.destroy())
        else:
            self.after_idle(lambda: self.destroy())

    def show(self, wait=False):
        self.transient(self.master)
        self.focus_set()
        self.grab_set()
        if wait:
            self.wait_window()



