from multiprocessing import Process, Queue, Event
from ui.main import run as run_ui
from testprocess.main import run as run_testprocess
from ui.ultrasonic import UltrasonicSensor
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
import sys

def main():
    try:
        Device.pin_factory = PiGPIOFactory()
        sensors = [
            UltrasonicSensor(echo=20, trigger=21, max_distance=5, start_angle=240, end_angle=300)
        ]
    except:
        print("Error:", sys.exc_info()[0])
        print("Couldn't initialize ultrasonic sensors. You're probably not running this on a Pi.")
        sensors = []

    queue = Queue()
    exit_event = Event()

    run_ui(queue, sensors)
    exit_event.set()

if __name__ == "__main__":
    main()
