#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter.ttk import *
from tkinter.constants import *
from tkinter import Tk
from script.view.View import View
from script.controller.BugManagerController import BugManagerController


class BugManagerView(View):
    def __init__(self, controller):
        self._mController = None
        self._mRootWindow = None

        if isinstance(controller, BugManagerController):
            self._mController = controller
        else:
            raise TypeError('Invalid type of controller')

        # root window
        root = Tk()
        root.geometry('600x50')
        root.attributes("-toolwindow", 1)
        root.wm_attributes("-topmost", 1)

        ##########################
        # frame for file operation
        frame_file = Frame(root)
        frame_file.pack(fill=Y,
                        padx=View.BUTTON_PADDING_X,
                        pady=View.BUTTON_PADDING_Y,
                        side=LEFT)

        # button open
        btn_open = Button(frame_file, text='Open', command=lambda: self._mController.cmd_open(root))
        btn_open.pack(side=LEFT)

        ##########################
        # frame for sync
        frame_sync = Frame(root)
        frame_sync.pack(fill=Y,
                        padx=View.BUTTON_PADDING_X,
                        pady=View.BUTTON_PADDING_Y,
                        side=LEFT)

        # button sync
        btn_sync = Button(frame_sync, text='Sync', command=lambda: self._mController.cmd_sync(root, False))
        btn_sync.pack(side=LEFT)

        # button sync all
        btn_sync_all = Button(frame_sync, text='Sync All', command=lambda: self._mController.cmd_sync(root, True))
        btn_sync_all.pack(side=LEFT)

        ##############################
        # frame for edit
        frame_edit = Frame(root)
        frame_edit.pack(fill=Y,
                        padx=View.BUTTON_PADDING_X,
                        pady=View.BUTTON_PADDING_Y,
                        side=LEFT)

        # button view
        btn_view = Button(frame_edit, text='View', command=lambda: self._mController.cmd_view(root))
        btn_view.pack(side=LEFT)

        # button edit
        btn_edit = Button(frame_edit, text='Edit', command=lambda: self._mController.cmd_edit(root))
        btn_edit.pack(side=LEFT)

        # button create
        btn_create = Button(frame_edit, text='Create', command=lambda: self._mController.cmd_create(root))
        btn_create.pack(side=LEFT)

        # save to member var
        self._mRootWindow = root

    def show(self):
        self._mRootWindow.mainloop()

    def dismiss(self):
        pass
