from threading import Thread

class AbstractWorker(Thread):
    """
    Generic template of worker. Hides internal implementation of protocol
    """
    def __init__(self, worker_id, queue, data):
        Thread.__init__(self)
        self.worker_id = worker_id
        self.data = data
        self.queue = queue
