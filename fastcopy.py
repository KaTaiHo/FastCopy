import logging
import os
import queue
import random
import threading
import time

from collections import namedtuple
from os import listdir, walk
from os.path import isfile, join

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 2
q = queue.Queue(maxsize=BUF_SIZE)
BUF_OBJECT_SIZE = 1024*1024*25

BufferObject = namedtuple("BufferObject", "buffer filepath index")


class ProducerThread(threading.Thread):
    def __init__(self, src, name=None):
        super(ProducerThread, self).__init__()
        self.name = name
        self.src = src

    def run(self):
        logging.debug("producer started!")
        for r, d, f in os.walk(self.src):
            for file in f:
                filepath = os.path.join(r, file)
                with open(filepath, "rb", buffering=0) as file:
                    current_loc = 0
                    file.seek(current_loc)
                    while current_loc < os.path.getsize(filepath):
                        buffer = BufferObject(
                            buffer=file.read(BUF_OBJECT_SIZE),
                            filepath=filepath, index=current_loc)
                        current_loc += BUF_OBJECT_SIZE
                        q.put(buffer)


class ConsumerThread(threading.Thread):
    def __init__(self, src, dest, name=None):
        super(ConsumerThread, self).__init__()
        self.name = name
        self.src = src
        self.dest = dest

    def run(self):
        logging.debug("consumer started!")

        src_size = self.get_dir_size(self.src)
        bytes_copied = 0

        while bytes_copied < src_size:
            while q.qsize() > 0:
                buffer = q.get()
                logging.debug('Got ' + str(buffer.filepath) + ' from q')
                filepath = buffer.filepath.replace(self.src, self.dest)
                dir_name = os.path.dirname(filepath)

                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                if not os.path.exists(filepath):
                    open(filepath, 'w').close()

                with open(filepath, "r+b", buffering=0) as file:
                    logging.debug('writing to:' + str(filepath))
                    file.seek(buffer.index)
                    file.write(buffer.buffer)
                    bytes_copied += len(buffer.buffer)
            time.sleep(random.random())

    def get_dir_size(self, start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size


if __name__ == "__main__":
    start = time.time()

    src = "enter path here"
    dest = "enter path here"

    p = ProducerThread(name='producer', src=src)
    c = ConsumerThread(name='consumer', src=src, dest=dest)

    p.start()
    time.sleep(1)
    c.start()
    time.sleep(1)

    p.join()
    c.join()

    end = time.time()
    print(end - start)
