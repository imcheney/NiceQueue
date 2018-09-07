# -*- coding: utf-8 -*-

"""This implements a NiceQueue class."""

import Queue
from time import time as _time


class NiceQueue(Queue.Queue, object):
    """NiceQueue is a augmented version of original python's thread-safe Queue with peek and indexer operator ability

    additional abilities are these:

    indexer ([] operator): based on Queue's internal deque

    peek, peek_no_wait: based on Queue.get, Queue.get_no_wait

    put_left: based on Queue.put

    """

    def __init__(self, *args, **kwargs):
        super(NiceQueue, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        try:
            return self.queue[item]
        except IndexError:
            print 'Queue is empty!'
            return None

    def peek(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        self.not_empty.acquire()
        try:
            if not block:
                if not self._qsize():
                    raise Queue.Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = _time() + timeout
                while not self._qsize():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Queue.Empty
                    self.not_empty.wait(remaining)
            item = self.queue[0]
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

    def peek_no_wait(self):
        return self.peek(block=False)

    def put_left(self, item, block=True, timeout=None):
        """Put an item into the queue's left side

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        """
        self.not_full.acquire()
        try:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() == self.maxsize:
                        raise Queue.Full
                elif timeout is None:
                    while self._qsize() == self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = _time() + timeout
                    while self._qsize() == self.maxsize:
                        remaining = endtime - _time()
                        if remaining <= 0.0:
                            raise Queue.Full
                        self.not_full.wait(remaining)
            self._put_left(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
        finally:
            self.not_full.release()

    # Put a new item in the queue's left side
    def _put_left(self, item):
        self.queue.appendleft(item)

    # for developer
    def __repr__(self):
        return 'NiceQueue object: {} @ {}'.format(str(list(self.queue)), super(NiceQueue, self).__repr__())

    # for customer
    def __str__(self):
        return 'NiceQueue object: {}'.format(str(list(self.queue)))


if __name__ == '__main__':
    Q = NiceQueue()
    Q.put(10)
    print Q[0]
    print Q.peek()
    print Q.peek_no_wait()
    Q.put_left(20)
    print Q.peek_no_wait()
    print Q.__repr__()
    print str(Q)
