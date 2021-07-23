from gpiozero import DistanceSensor

class UltrasonicSensor:
    def __init__(self, echo: int, trigger: int, start_angle: float, end_angle: float):
        self.sensor = DistanceSensor(echo, trigger)
        self.start_angle = start_angle
        self.end_angle = end_angle
    
    def distance(self) -> float:
        return self.sensor.distance