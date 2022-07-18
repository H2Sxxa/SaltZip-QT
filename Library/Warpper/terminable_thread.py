"""stoppable_thread"""

import ctypes
import threading


class TerminableThread(threading.Thread):
    """a thread that can be stopped by forcing an exception in the execution context"""

    def terminate(self, exception_cls, repeat_sec=2.0):
        if self.is_alive() is False:
            return True
        killer = ThreadKiller(self, exception_cls, repeat_sec=repeat_sec)
        killer.start()


class ThreadKiller(threading.Thread):
    """separate thread to kill TerminableThread"""

    def __init__(self, target_thread, exception_cls, repeat_sec=2.0):
        threading.Thread.__init__(self)
        self.target_thread = target_thread
        self.exception_cls = exception_cls
        self.repeat_sec = repeat_sec
        self.daemon = True

    def run(self):
        """loop raising exception incase it's caught hopefully this breaks us far out"""
        while self.target_thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.target_thread.ident),
                                                       ctypes.py_object(self.exception_cls))
            self.target_thread.join(self.repeat_sec)