from multiprocessing import Queue, Event
from time import sleep

def run(queue: Queue, exit_event: Event):
    print("Started test process.")
    while not exit_event.is_set():
        queue.put({"type": "test", "test": "Approved™"})
        sleep(10)