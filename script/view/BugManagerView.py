#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from script.controller.IBugManagerController import IBugManagerController


class BugManagerView(object):
    _BUTTON_PADDING_X = 5
    _BUTTON_PADDING_Y = 5

    def __init__(self):
        self._mController = None
        self._mRootWindow = None

    def create(self, controller):
        if isinstance(controller, IBugManagerController):
            self._mController = controller

        # root window
        root = Tk()
        root.geometry('600x60')

        ##########################
        # frame for sync
        frame_sync = Frame(root, bg='red')
        frame_sync.pack(fill=Y,
                        padx=BugManagerView._BUTTON_PADDING_X,
                        pady=BugManagerView._BUTTON_PADDING_Y,
                        side=LEFT)

        # button sync
        btn_sync = Button(frame_sync, text='Sync', command=lambda:self._mController.cmd_sync(btn_sync))
        btn_sync.pack(fill=Y,
                      padx=BugManagerView._BUTTON_PADDING_X,
                      pady=BugManagerView._BUTTON_PADDING_Y,
                      side=LEFT)

        # button sync all
        btn_sync_all = Button(frame_sync, text='Sync All', command=lambda:self._mController.cmd_sync_all(btn_sync_all))
        btn_sync_all.pack(fill=Y,
                          padx=BugManagerView._BUTTON_PADDING_X,
                          pady=BugManagerView._BUTTON_PADDING_Y,
                          side=LEFT)

        ##############################
        # frame for edit
        frame_edit = Frame(root, bg='blue')
        frame_edit.pack(fill=Y,
                        padx=BugManagerView._BUTTON_PADDING_X,
                        pady=BugManagerView._BUTTON_PADDING_Y,
                        side=LEFT)

        # button view
        btn_view = Button(frame_edit, text='View', command=lambda: self._mController.cmd_view(btn_view))
        btn_view.pack(fill=Y,
                      padx=BugManagerView._BUTTON_PADDING_X,
                      pady=BugManagerView._BUTTON_PADDING_Y,
                      side=LEFT)

        # button edit
        btn_edit = Button(frame_edit, text='Edit', command=lambda: self._mController.cmd_edit(btn_edit))
        btn_edit.pack(fill=Y,
                      padx=BugManagerView._BUTTON_PADDING_X,
                      pady=BugManagerView._BUTTON_PADDING_Y,
                      side=LEFT)

        # save to member var
        self._mRootWindow = root

    def show(self):
        self._mRootWindow.mainloop()
