#!/usr/bin/python
# -*- coding: UTF-8 -*-

from unittest import TestCase

from script.model.local_alm.im.Im import Im
from script.model.local_alm.util.Util import Util
from script.model.local_alm.util.MultiThreadRunner import MultiThreadRunner
from threading import Lock


class ImTest(TestCase):
    _mLock = Lock()
    _mCount = 0

    BUG_LIST = (
        4300248,
        4399123,
        4733257,
        4758895,
        4772672,
        4785178,
        4812812,
        4814332,
        4814610
    )

    def test_im(self):
        t1 = Util.format_time_to_float(Util.current_time())
        for id in self.BUG_LIST:
            print ('[%d] %s' % (id, Im.execute('im viewissue --showRichContent %s' % id)))

        t2 = Util.format_time_to_float(Util.current_time())
        print ('total time: %s' % (t2 - t1))

        print ('test muti thread')
        self._mCount = 0
        mtr = MultiThreadRunner(5, self.thread_run)
        mtr.start(self.BUG_LIST)
        mtr.join()
        t3 = Util.format_time_to_float(Util.current_time())
        print ('total time: %s' % (t3 - t2))

        print ('remaining threads: %d' % mtr.get_running_thread_count())

    def thread_run(self, id, global_params):
        msg = '[%d] %s' % (id, Im.execute('im viewissue --showRichContent %s' % id))

        self._mLock.acquire()
        print ('[%d] %s' % (self._mCount, msg))
        self._mCount += 1
        self._mLock.release()



