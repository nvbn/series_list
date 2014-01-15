from Queue import Empty
from multiprocessing import Queue, Process
import threading


actors = {}


def current_actor():
    """Get current actor"""
    return threading.current_thread().actor


class Actor(Process):
    """Multiprocessing based actor"""
    use_nowait = False
    self_loop = False

    def __init__(self, name):
        super(Actor, self).__init__()
        self.input_queue = Queue()
        self._register(name)
        self._seed = 0

    def _register(self, name):
        """Register actor"""
        self.name = name
        actors[self.name] = self

    def run(self):
        """Receive messages in loop"""
        self._callbacks = {}
        threading.current_thread().actor = self
        if not self.self_loop:
            while True:
                self.loop_tick()

    def _get_input(self):
        """Get input from queue"""
        if self.use_nowait:
            return self.input_queue.get_nowait()
        else:
            return self.input_queue.get()

    def loop_tick(self):
        """Loop tick"""
        try:
            msg_type, seed, sender, msg = self._get_input()
        except Empty:
            return
        if msg_type == 'call':
            result = self.on_message(msg[0], **msg[1])
            actors[sender].respond(seed, result)
        elif msg_type == 'result':
            self._callbacks[seed](msg)
            del self._callbacks[seed]

    def _get_seed(self):
        """Get new seed each time"""
        self._seed += 1
        return self._seed

    def register_callback(self, callback):
        """Register callback and return seed"""
        seed = self._get_seed()
        self._callbacks[seed] = callback
        return seed

    def on_message(self, msg, **data):
        """On message received"""
        return getattr(self, msg)(**data)

    def send(self, msg, callback=lambda *args, **kwargs: None, **data):
        """Send message to actor"""
        actor = current_actor()
        seed = actor.register_callback(callback)
        self.input_queue.put(('call', seed, actor.name, (msg, data)))

    def respond(self, seed, result):
        """Respond to actor"""
        self.input_queue.put(('result', seed, current_actor().name, result))
