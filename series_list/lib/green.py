import time
import threading
from .actors import Actor


class GreenActor(Actor):
    """Green actor"""
    self_loop = True
    use_nowait = True
    max_wait = 3
    max_tasks = 10

    def _update_last_call(self):
        self._last_call = time.time()

    def run(self):
        import gevent
        import gevent.monkey
        gevent.monkey.patch_socket()
        gevent.monkey.patch_ssl()

        self._update_last_call()
        self._buffer = []
        self._responds = []

        while True:
            if not self.loop_tick():
                gevent.sleep(0.1)
            if self._is_wait_limit_reached() and self._buffer:
                tasks = [
                    gevent.spawn(self._make_call, call)
                    for call in self._buffer
                ]
                gevent.joinall(tasks)
                self._buffer = []
                self._update_last_call()
                for respond in self._responds:
                    self.respond(*respond, force=True)

    def _make_call(self, args):
        """Attach actor to thread and call"""
        threading.current_thread().actor = self
        self._on_call(*args, force=True)

    def _is_wait_limit_reached(self):
        return (time.time() - self._last_call > self.max_wait)\
            or len(self._buffer) > self.max_tasks

    def _on_call(self, sender, seed, msg, force=False):
        """Save calls or force run"""
        if force:
            super(GreenActor, self)._on_call(sender, seed, msg)
        else:
            self._buffer.append([sender, seed, msg])

    def respond(self, seed, result, force=False):
        """Save response or force send"""
        if force:
            super(GreenActor, self).respond(seed, result)
        else:
            self._responds.append([seed, result])
