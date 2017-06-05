#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
from unittest import TestCase
from script.model.excel.ExcelConfig import ExcelConfig


class ExcelConfigTest(TestCase):
    DIR = 'excel'

    def test_load(self):
        if not os.path.exists(ExcelConfigTest.DIR):
            os.makedirs(ExcelConfigTest.DIR)
        path = '%s/test_load.xlsm' % ExcelConfigTest.DIR

        # copy from template
        if os.path.exists(path):
            os.remove(path)
        shutil.copy('../template/template.xlsm', path)

        # load
        cfg = ExcelConfig(path)
        cfg.load()

        # close
        cfg.close()




