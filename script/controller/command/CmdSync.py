#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ICommand import ICommand
from script.model.local_alm.spider.ProjectSpider import ProjectSpider
from script.model.local_alm.spider.GeneralSpider import GeneralSpider


class CmdSync(ICommand):
    def __init__(self):
        ICommand.__init__(self)
        self._mProjectSpiders = []

    def on_cancel(self):
        for spider in self._mProjectSpiders:
            spider.cancel()

    def on_start(self):
        gs = GeneralSpider()
        gs.sync()

        self._mProjectSpiders.append(ProjectSpider('/TCT/GApp/Gallery'))

        for spider in self._mProjectSpiders:
            spider.sync()
            self._mProjectSpiders.remove(spider)

