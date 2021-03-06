#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter.ttk import *
from tkinter.constants import *
from script.view.View import View
from script.controller.ConfigExcelController import ConfigExcelController
from script.view.ModalDialogView import ModalDialogView


class ConfigExcelView(ModalDialogView):
    def __init__(self, parent, controller):
        ModalDialogView.__init__(self, parent, controller)

    def on_create_view(self, root, controller):
        if not isinstance(controller, ConfigExcelController):
            raise TypeError('Invalid type of parameter controller')

        ##############


        ##############
        # frame of bottom bar
        frame_bottom_bar = Frame(root)
        frame_bottom_bar.pack(fill=X,
                              padx=View.BUTTON_PADDING_X,
                              pady=View.BUTTON_PADDING_Y,
                              side=TOP)

        # button create
        btn_create = Button(
            frame_bottom_bar,
            text='Create',
            command=lambda: controller.cmd_new_excel(self, self.get_create_info()))
        btn_create.pack(fill=X,
                        padx=View.BUTTON_PADDING_X,
                        pady=View.BUTTON_PADDING_Y,
                        side=LEFT)

        # button cancel
        btn_cancel = Button(frame_bottom_bar, text='Cancel', command=lambda: controller.cmd_cancel(self))
        btn_cancel.pack(fill=X,
                        padx=View.BUTTON_PADDING_X,
                        pady=View.BUTTON_PADDING_Y,
                        side=LEFT)

    def get_create_info(self):
        return dict()


