from multiprocessing import Process, Queue, Event
from ui.main import run as run_ui
from testprocess.main import run as run_testprocess
from ui.ultrasonic import UltrasonicSensor
from gpiozero.exc import BadPinFactory

def main():
    try:
        sensors = [
            UltrasonicSensor(20, 21, 240, 300)
        ]
    except BadPinFactory:
        print("Couldn't load a default pin factory. You're probably not running this on a Pi.")
        sensors = []


    queue = Queue()
    exit_event = Event()

    testprocess = Process(target=run_testprocess, args=(queue, exit_event))
    testprocess.start()

    run_ui(queue, sensors)
    exit_event.set()

if __name__ == "__main__":
    main()