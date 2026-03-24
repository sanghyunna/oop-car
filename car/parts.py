from math import pi


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


class WheelPosition:
    FRONT_LEFT = "front-left"
    FRONT_RIGHT = "front-right"
    REAR_LEFT = "rear-left"
    REAR_RIGHT = "rear-right"


class Engine:
    def __init__(self, name, horsepower):
        self.name = name
        self.horsepower = horsepower
        self.is_running = False
        self.rpm = 0

    def start(self):
        if self.is_running:
            return f"{self.name} is already running."

        self.is_running = True
        self.rpm = 800
        return f"{self.name} started at {self.rpm} rpm."

    def stop(self):
        if not self.is_running:
            return f"{self.name} is already stopped."

        self.is_running = False
        self.rpm = 0
        return f"{self.name} stopped."

    def request_power(self, pedal_pressure):
        if not self.is_running:
            raise RuntimeError("The engine must be running before accelerating.")

        pedal_pressure = int(clamp(pedal_pressure, 0, 100))
        self.rpm = min(6500, 800 + pedal_pressure * 45)
        return self.rpm

    def idle(self):
        self.rpm = 800 if self.is_running else 0
        return self.rpm


class SteeringWheel:
    def __init__(self, max_angle=540):
        self.max_angle = max_angle
        self.angle = 0

    def turn(self, angle_delta):
        self.angle = int(clamp(self.angle + angle_delta, -self.max_angle, self.max_angle))
        return self.angle

    def center(self):
        self.angle = 0
        return self.angle


class Wheel:
    def __init__(self, position, diameter_inch=18):
        self.position = position
        self.diameter_inch = diameter_inch
        self.total_rotations = 0.0

    def roll(self, distance_meters):
        diameter_meters = self.diameter_inch * 0.0254
        circumference = pi * diameter_meters
        rotations = 0.0 if circumference == 0 else distance_meters / circumference
        self.total_rotations += rotations
        return self.total_rotations


class BrakeSystem:
    def __init__(self):
        self.brake_force = 0

    def apply(self, pedal_pressure):
        self.brake_force = int(clamp(pedal_pressure, 0, 100))
        return self.brake_force

    def release(self):
        self.brake_force = 0
        return self.brake_force


class Pedal:
    def __init__(self, name):
        self.name = name
        self.pressure = 0

    def press(self, pressure):
        self.pressure = int(clamp(pressure, 0, 100))
        return self.pressure

    def release(self):
        self.pressure = 0
        return self.pressure


class AcceleratorPedal(Pedal):
    pass


class BrakePedal(Pedal):
    pass
