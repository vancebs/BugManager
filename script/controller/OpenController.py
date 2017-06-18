#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.model.local_alm.cfg.Config import Config
from tkinter.constants import *
from script.controller.command.CmdNewExcel import CmdNewExcel
from script.controller.command.CmdOpenExcel import CmdOpenExcel
from script.controller.command.CmdRemoveExcel import CmdRemoveExcel


class OpenController(object):
    def __init__(self):
        self.mConfig = Config()
        self.mListBox = None

    def cmd_open(self, view):
        print('cmd_open')
        list_box = self.mListBox

        # get selected item path
        selection = list_box.curselection()
        if len(selection) > 0:
            index = selection[0]
        else:
            print('\t No item selected.')
            return
        path = list_box.get(index)

        # open item by path
        cmd = CmdOpenExcel(path)
        cmd.start()

        # update UI
        self.reload_list()

    def cmd_new(self, view):
        print('cmd_new')

        # new excel
        cmd = CmdNewExcel(view)
        cmd.start()

        # reload list
        self.reload_list()

    def cmd_remove(self, view):
        print('cmd_remove')
        list_box = self.mListBox

        # get selected item path
        selection = list_box.curselection()
        if len(selection) > 0:
            index = selection[0]
        else:
            print('\t No item selected.')
            return
        path = list_box.get(index)

        # open item by path
        cmd = CmdRemoveExcel(path)
        cmd.start()

        # update
        self.reload_list()

    def init_list(self, list_box):
        self.mListBox = list_box
        cfg = self.mConfig

        # load list
        self.reload_list()

    def reload_list(self):
        list_box = self.mListBox
        cfg = self.mConfig

        # check
        if not list_box:
            return

        # clear all
        list_box.delete(0, list_box.size())

        # add items
        recent_list = cfg.get_recent_list()
        for item in recent_list:
            list_box.insert(END, item)

        # select first one by default
        if len(recent_list) > 0:
            list_box.select_set(0)

    def _open(self, path):
        print('open %s' + path)  # TODO

    def _remove(self, path):
        print('remove %s' % path)
