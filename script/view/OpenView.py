#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import Listbox
from ttk import *
from Tkconstants import *
from View import View
from script.controller.OpenController import OpenController
from ModalDialogView import ModalDialogView


class OpenView(ModalDialogView):
    def __init__(self, parent, controller):
        ModalDialogView.__init__(self, parent, controller)

    def on_create_view(self, root, controller):
        if not isinstance(controller, OpenController):
            raise TypeError('Invalid type of parameter controller')

        #################
        # frame for operations
        frame_operation = Frame(root)
        frame_operation.pack(fill=X,
                             padx=View.BUTTON_PADDING_X,
                             pady=View.BUTTON_PADDING_Y,
                             side=TOP)

        # button new
        btn_new = Button(frame_operation, text='New', command=lambda: controller.cmd_new(self))
        btn_new.pack(fill=X,
                     padx=View.BUTTON_PADDING_X,
                     pady=View.BUTTON_PADDING_Y,
                     side=LEFT)

        # button open
        btn_open = Button(frame_operation, text='Open', command=lambda: controller.cmd_open(self))
        btn_open.pack(fill=X,
                      padx=View.BUTTON_PADDING_X,
                      pady=View.BUTTON_PADDING_Y,
                      side=LEFT)

        # button remove
        btn_remove = Button(frame_operation, text='Remove', command=lambda: controller.cmd_remove(self))
        btn_remove.pack(fill=X,
                        padx=View.BUTTON_PADDING_X,
                        pady=View.BUTTON_PADDING_Y,
                        side=LEFT)

        ######################
        # list
        list_box = Listbox(root, selectmode=SINGLE)
        controller.init_list(list_box)
        list_box.pack(fill=X,
                      padx=View.BUTTON_PADDING_X,
                      pady=View.BUTTON_PADDING_Y,
                      side=TOP)
