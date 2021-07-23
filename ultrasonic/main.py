from multiprocessing import Queue, Event

# Runs when the program starts.
def run(queue: Queue, exit_event: Event):
    print("Started ultrasonic.")

    # Notify the UI about a measurement with something like
    # queue.put({"type": "ultrasonic", "data": 123})