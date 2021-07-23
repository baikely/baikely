from multiprocessing import Process, Queue
from ui.main import run as run_ui
from testprocess.main import run as run_testprocess

def main():
    queue = Queue()
    testprocess = Process(target=run_testprocess, args=(queue,))
    testprocess.start()
    run_ui(queue)

if __name__ == "__main__":
    main()