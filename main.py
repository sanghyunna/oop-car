from car import build_demo_car


def main():
    car = build_demo_car("Demo Car")

    steps = [
        car.status(),
        car.start(),
        car.shift("D"),
        car.accelerate(30, seconds=2),
        car.turn(-90),
        car.accelerate(60, seconds=3),
        car.straighten(),
        car.brake(50, seconds=2),
        car.brake(100, seconds=3),
        car.shift("P"),
        car.stop(),
        car.status(),
    ]

    for step in steps:
        print(step)


if __name__ == "__main__":
    main()

