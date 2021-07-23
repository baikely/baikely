from multiprocessing import Queue
from time import sleep

def run(queue: Queue):
    while True:
        queue.put({"type": "test", "test": "Approved™"})
        sleep(1)