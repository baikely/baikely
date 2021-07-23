from multiprocessing import Process, Queue, Event
from ui.main import run as run_ui
from testprocess.main import run as run_testprocess
from ultrasonic.main import run as run_ultrasonic

def main():
    queue = Queue()
    exit_event = Event()

    testprocess = Process(target=run_testprocess, args=(queue, exit_event))
    testprocess.start()

    ultrasonic = Process(target=run_ultrasonic, args=(queue, exit_event))
    ultrasonic.start()

    run_ui(queue)
    exit_event.set()

if __name__ == "__main__":
    main()