#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from IController import IController


class BugManagerUI(object):
    _BUTTON_PADDING_X = 5
    _BUTTON_PADDING_Y = 5

    _mRootWindow = None
    _mController = None

    def __init__(self):
        pass

    def create(self, controller):
        if isinstance(controller, IController):
            self._mController = controller

        # root window
        root = Tk()
        root.geometry('100x600')

        ##########################
        # frame for sync
        frame_sync = Frame(root, bg='red')
        frame_sync.pack(fill=X,
                        padx=BugManagerUI._BUTTON_PADDING_X,
                        pady=BugManagerUI._BUTTON_PADDING_Y)

        # button sync
        btn_sync = Button(frame_sync, text='Sync', command=lambda:self._mController.cmd_sync())
        btn_sync.pack(fill=X,
                      padx=BugManagerUI._BUTTON_PADDING_X,
                      pady=BugManagerUI._BUTTON_PADDING_Y)

        # button sync all
        btn_sync_all = Button(frame_sync, text='Sync All', command=lambda:self._mController.cmd_sync_all())
        btn_sync_all.pack(fill=X,
                          padx=BugManagerUI._BUTTON_PADDING_X,
                          pady=BugManagerUI._BUTTON_PADDING_Y)

        ##############################
        # frame for edit
        frame_edit = Frame(root, bg='blue')
        frame_edit.pack(fill=X,
                        padx=BugManagerUI._BUTTON_PADDING_X,
                        pady=BugManagerUI._BUTTON_PADDING_Y)

        # button view
        btn_view = Button(frame_edit, text='View', command=lambda: self._mController.cmd_view())
        btn_view.pack(fill=X,
                      padx=BugManagerUI._BUTTON_PADDING_X,
                      pady=BugManagerUI._BUTTON_PADDING_Y)

        # button edit
        btn_edit = Button(frame_edit, text='Edit', command=lambda: self._mController.cmd_edit())
        btn_edit.pack(fill=X,
                      padx=BugManagerUI._BUTTON_PADDING_X,
                      pady=BugManagerUI._BUTTON_PADDING_Y)

        # save to member var
        self._mRootWindow = root

    def show(self):
        self._mRootWindow.mainloop()
