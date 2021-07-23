from multiprocessing import Queue

def run(queue: Queue):
    print("Started ultrasonic.")
    
    # Notify the UI about a measurement with something like
    # queue.put({"type": "ultrasonic", "data": 123})