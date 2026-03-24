from .parts import AcceleratorPedal, BrakePedal, BrakeSystem, Engine, SteeringWheel, Wheel, WheelPosition
from .vehicle import Vehicle


class Car(Vehicle):
    def __init__(
        self,
        model_name,
        engine,
        steering_wheel,
        brake_system,
        accelerator_pedal,
        brake_pedal,
        wheels=None,
    ):
        self.model_name = model_name
        self.engine = engine
        self.steering_wheel = steering_wheel
        self.brake_system = brake_system
        self.accelerator_pedal = accelerator_pedal
        self.brake_pedal = brake_pedal
        self.wheels = wheels or []
        self.gear = "P"
        self.speed_kph = 0.0

    def start(self):
        return self.engine.start()

    def stop(self):
        if self.speed_kph > 0:
            raise RuntimeError("The car must be fully stopped before turning off.")

        self.release_controls()
        self.gear = "P"
        return self.engine.stop()

    def shift(self, gear):
        valid_gears = {"P", "R", "N", "D"}
        if gear not in valid_gears:
            raise ValueError("Unsupported gear: {0}".format(gear))

        if gear == "P" and self.speed_kph > 0:
            raise RuntimeError("Cannot shift into P while the car is moving.")

        self.gear = gear
        return "{0} shifted to {1}.".format(self.model_name, self.gear)

    def accelerate(self, pressure, seconds=1.0):
        if not self.engine.is_running:
            raise RuntimeError("Start the engine before accelerating.")
        if self.gear != "D":
            raise RuntimeError("Shift into D before accelerating.")

        accelerator_pressure = self.accelerator_pedal.press(pressure)
        self.brake_pedal.release()
        self.brake_system.release()

        engine_rpm = self.engine.request_power(accelerator_pressure)
        speed_delta = accelerator_pressure * 0.35 * seconds
        self.speed_kph = min(220.0, self.speed_kph + speed_delta)

        distance_meters = self.speed_kph * 1000 / 3600 * seconds
        for wheel in self.wheels:
            wheel.roll(distance_meters)

        return (
            "{0} accelerated with {1}% throttle. "
            "Speed is now {2:.1f} km/h at {3} rpm.".format(
                self.model_name,
                accelerator_pressure,
                self.speed_kph,
                engine_rpm,
            )
        )

    def brake(self, pressure, seconds=1.0):
        brake_pressure = self.brake_pedal.press(pressure)
        self.accelerator_pedal.release()
        braking_force = self.brake_system.apply(brake_pressure)

        speed_delta = braking_force * 0.4 * seconds
        self.speed_kph = max(0.0, self.speed_kph - speed_delta)

        if self.speed_kph == 0:
            self.engine.idle()

        return (
            "{0} braked with {1}% pressure. "
            "Speed is now {2:.1f} km/h.".format(self.model_name, brake_pressure, self.speed_kph)
        )

    def turn(self, angle_delta):
        angle = self.steering_wheel.turn(angle_delta)
        return "Steering wheel angle changed to {0} degrees.".format(angle)

    def straighten(self):
        angle = self.steering_wheel.center()
        return "Steering wheel returned to {0} degrees.".format(angle)

    def release_controls(self):
        self.accelerator_pedal.release()
        self.brake_pedal.release()
        self.brake_system.release()
        self.steering_wheel.center()

    def status(self):
        wheel_summary = ", ".join(
            "{0}:{1:.1f} turns".format(wheel.position, wheel.total_rotations) for wheel in self.wheels
        )
        return (
            "Car<{0}> gear={1}, speed={2:.1f} km/h, "
            "engine_running={3}, rpm={4}, steering_angle={5}, wheels=[{6}]".format(
                self.model_name,
                self.gear,
                self.speed_kph,
                self.engine.is_running,
                self.engine.rpm,
                self.steering_wheel.angle,
                wheel_summary,
            )
        )


def build_demo_car(model_name="Demo Car"):
    wheels = [
        Wheel(WheelPosition.FRONT_LEFT),
        Wheel(WheelPosition.FRONT_RIGHT),
        Wheel(WheelPosition.REAR_LEFT),
        Wheel(WheelPosition.REAR_RIGHT),
    ]

    return Car(
        model_name=model_name,
        engine=Engine(name="I4 Engine", horsepower=180),
        steering_wheel=SteeringWheel(),
        brake_system=BrakeSystem(),
        accelerator_pedal=AcceleratorPedal(name="Accelerator"),
        brake_pedal=BrakePedal(name="Brake"),
        wheels=wheels,
    )

