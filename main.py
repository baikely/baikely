from multiprocessing import Process, Queue
from ui.main import run as run_ui
from testprocess.main import run as run_testprocess
from ultrasonic.main import run as run_ultrasonic

def main():
    queue = Queue()

    testprocess = Process(target=run_testprocess, args=(queue,))
    testprocess.start()

    ultrasonic = Process(target=run_ultrasonic, args=(queue,))
    ultrasonic.start()

    run_ui(queue)

if __name__ == "__main__":
    main()