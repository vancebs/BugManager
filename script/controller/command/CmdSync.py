#!/usr/bin/python
# -*- coding: UTF-8 -*-

from script.controller.command.ICommand import ICommand
from script.model.local_alm.spider.ProjectSpider import ProjectSpider
from script.model.local_alm.spider.GeneralSpider import GeneralSpider


class CmdSync(ICommand):
    def __init__(
            self,
            on_project_progress=None,
            on_sync_data_progress=None,
            on_sync_raw_progress=None,
            force_update=False):
        ICommand.__init__(self)
        self.on_project_progress = on_project_progress
        self.on_sync_data_progress = on_sync_data_progress
        self.on_sync_raw_progress = on_sync_raw_progress
        self.force_update = force_update
        self._mProjectSpiders = []

    def on_cancel(self):
        for spider in self._mProjectSpiders:
            spider.cancel()

    def on_start(self):
        # sync general database
        gs = GeneralSpider()
        gs.sync()

        # sync project database
        count = 0
        total = 1
        self._mProjectSpiders.append(ProjectSpider('/TCT/GApp/Gallery'))  # TODO get list

        # notify progress
        if self.on_project_progress is not None:
            self.on_project_progress(0, total)

        # start sync projects
        for spider in self._mProjectSpiders:
            spider.sync(
                on_sync_data_progress=self.on_sync_data_progress,
                on_sync_raw_progress=self.on_sync_raw_progress,
                total_fetch=self.force_update)
            self._mProjectSpiders.remove(spider)

            count += 1

            # notify progress
            if self.on_project_progress is not None:
                self.on_project_progress(count, total)

        # notify progress
        if self.on_project_progress is not None:
            self.on_project_progress(total, total)

