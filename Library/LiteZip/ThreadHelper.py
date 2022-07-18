import threading

class ResThread(threading.Thread):
    def __init__(self, target, args):
        threading.Thread.__init__(self)
        self.func = target
        self.args = args
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return str(e)