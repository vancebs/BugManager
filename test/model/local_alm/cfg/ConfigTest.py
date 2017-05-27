#!/usr/bin/python
# -*- coding: UTF-8 -*-

from unittest import TestCase
from script.model.local_alm.cfg.Config import Config


class ConfigTest(TestCase):
    def test_config(self):
        cfg = Config()

        cfg.set_config('proj1', 'a', 'value 1')
        cfg.set_config('proj1', 'b', 'value 22')
        cfg.set_config('proj1', 'c', 'value 3')
        cfg.set_config('proj1', 'd', 'value 4')
