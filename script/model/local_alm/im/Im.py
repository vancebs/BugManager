#!/usr/bin/python
# -*- coding: UTF-8 -*-

from subprocess import Popen
import subprocess


class Im(object):
    @staticmethod
    def execute(cmd):
        # run command
        p = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

        (out, err) = p.communicate()
        return p.returncode, out, err
