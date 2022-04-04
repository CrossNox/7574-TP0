from threading import Event, Thread
import logging

class StoppableThread(Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = Event()

    def stop(self):
        logging.warning("Force stopping thread")
        self._stop_event.set()

    @property
    def stopped(self):
        return self._stop_event.is_set()
