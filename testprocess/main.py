from multiprocessing import Queue
from time import sleep

def run(queue: Queue):
    print("Started test process.")
    while True:
        queue.put({"type": "test", "test": "Approved™"})
        sleep(10)