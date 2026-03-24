class Vehicle:
    def start(self):
        raise NotImplementedError("Subclasses must implement start().")

    def stop(self):
        raise NotImplementedError("Subclasses must implement stop().")

    def status(self):
        raise NotImplementedError("Subclasses must implement status().")
