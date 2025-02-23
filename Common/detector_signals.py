# file: detector_signals.py

from PyQt5.QtCore import QObject, pyqtSignal

class DetectorSignals(QObject):
    """
    A QObject that defines signals for keyword detection.
    """
    bruce_loading = pyqtSignal()
    bruce_responding = pyqtSignal()
    bruce_listening = pyqtSignal()
    bruce_quitting = pyqtSignal()
    
# Create ONE global instance that can be imported
detector_signals = DetectorSignals()
