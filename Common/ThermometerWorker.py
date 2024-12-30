# ThermometerWorker.py
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time, random

class ThermometerWorker(QObject):
    temperature_updated = pyqtSignal(float)  # Signal to send the temperature reading
    finished = pyqtSignal()  # Signal to indicate the thread is finished

    def __init__(self):
        super().__init__()
        self._running = True  # Control the thread execution

    def run(self):
        """Worker's main loop to read temperatures."""
        while self._running:
            # Simulate temperature reading (replace this with actual thermometer code)
            temperature = self.read_thermometer()
            self.temperature_updated.emit(temperature)  # Emit the new temperature
            time.sleep(1)  # Wait for a second between readings

    def read_thermometer(self):
        """Simulate reading temperature. Replace with actual thermometer logic."""
        return random.uniform(0.0, 101.9)  # Simulated temperature

    def stop(self):
        """Stop the worker loop."""
        self._running = False
