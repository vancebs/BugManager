#!/usr/bin/python
# -*- coding: UTF-8 -*-

from threading import *
from Queue import Queue
from Queue import Empty


class MultiThreadRunner(object):
    def __init__(self, thread_count, runner, global_params=None):
        if not runner:
            raise ValueError('runner should not be None')

        self._mThreadList = []
        self._mQueue = Queue()
        self._mResultQueue = Queue()
        self._mLock = Lock()
        self._mFinishedTaskCount = 0

        for i in range(thread_count):
            self._mThreadList.append([None, (runner, i, global_params)])

    def get_thread_count(self):
        return self._mThreadList.__len__()

    def get_running_thread_count(self):
        count = 0
        for t in self._mThreadList:
            if t[0] is not None:
                count += 1
        return count

    def start(self, params):
        # insert params into queue
        for p in params:
            self._mQueue.put_nowait(p)

        # create thread
        for t in self._mThreadList:
            if t[0] is not None and not t[0].isAlive():
                t[0] = None

            if t[0] is None:
                t[0] = Thread(target=self._thread_run, args=t[1])

        # start thread
        for t in self._mThreadList:
            t[0].start()

    def cancel(self):
        self._mQueue.queue.clear()

    def join(self):
        self._mQueue.join()

    def get_result_queue(self):
        return self._mResultQueue

    def _thread_run(self, runner, thread_id, global_params):
        try:
            while True:
                param = self._mQueue.get_nowait()
                self._mResultQueue.put(runner(param, global_params))
                self._mQueue.task_done()

                # finished task count ++
                self._mLock.acquire()
                self._mFinishedTaskCount += 1
                self._mLock.release()
        except Empty:
            self._mLock.acquire()

            self._mThreadList[thread_id][0] = None

            thread_count = self.get_running_thread_count()
            # print ('no more tasks, finish this thread: %d, Threads left: %d' % (thread_id, thread_count))

            # add a None item if all threads are finished
            if thread_count <= 0:
                # print ('no more thread. add None into result queue')
                self._mResultQueue.put(None)

            self._mLock.release()

    def get_finished_task_count(self):
        return self._mFinishedTaskCount
