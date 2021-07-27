from multiprocessing import Process, Queue, Event
from ui.main import run as run_ui
from TFLite_detection_webcam import run as run_cv
from ui.ultrasonic import UltrasonicSensor
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
import sys

def main():
    try:
        Device.pin_factory = PiGPIOFactory()
        sensors = [
            UltrasonicSensor(echo=0, trigger=5, max_distance=5, start_angle=180, end_angle=240),
            UltrasonicSensor(echo=6, trigger=13, max_distance=5, start_angle=240, end_angle=300),
            UltrasonicSensor(echo=19, trigger=26, max_distance=5, start_angle=300, end_angle=360)
        ]
    except:
        print("Error:", sys.exc_info()[0])
        print("Couldn't initialize ultrasonic sensors. You're probably not running this on a Pi.")
        sensors = []

    queue = Queue()
    exit_event = Event()

    cv = Process(target=run_cv, args=(queue, exit_event))
    cv.start()

    try:
        run_ui(queue, sensors)
    except KeyboardInterrupt:
        print("Stopping...")
        pass
    exit_event.set()

if __name__ == "__main__":
    main()
