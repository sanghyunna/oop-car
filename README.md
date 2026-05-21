# Dummy Car OOP Example

This repository contains a small vanilla Python example of object-oriented design
object-oriented design with a `Car` class and conceptual car parts.

## Structure

- `Vehicle`: shared base class for vehicles.
- `Car`: coordinates the driving flow and delegates to part objects.
- `Engine`: starts, stops, idles, and responds to accelerator input.
- `SteeringWheel`: manages steering angle.
- `Wheel`: tracks conceptual wheel rotation.
- `BrakeSystem`: converts brake pressure into braking force.
- `AcceleratorPedal` and `BrakePedal`: user controls.

## OOP ideas shown here

- Inheritance: `Car` inherits from `Vehicle`, and pedal types inherit from `Pedal`.
- Composition: `Car` owns an engine, steering wheel, wheels, and controls.
- Encapsulation: each part manages its own state and exposes small methods.
- Responsibility split: parts handle part behaviors; `Car` coordinates them.

## How to run

```bash
python main.py
```

This example is intentionally simple and is not meant to simulate real-world
vehicle physics.

![Codebase structure](https://gitstarter.kro.kr/api/readme-graph.svg?url=https%3A%2F%2Fgithub.com%2Fsanghyunna%2Foop-car)
