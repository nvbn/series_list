from Queue import Empty
from ..loaders import library


def _fetch_one(episode, tick):
    """Fetch one episode"""
    import gevent
    jobs = [
        gevent.spawn(episode.load_poster),
        gevent.spawn(episode.load_subtitle),
    ]
    gevent.joinall(jobs)
    return episode, tick


def fetcher_proc(in_queue, out_queue, current_tick):
    """Fetcher process"""
    import gevent
    from gevent.monkey import patch_socket
    patch_socket()

    library.import_all()

    while True:
        pull = []
        while len(pull) < 10:
            try:
                episode, tick = in_queue.get_nowait()
            except Empty:
                break
            if tick == current_tick.value:
                pull.append((episode, tick))
        jobs = [gevent.spawn(_fetch_one, *data) for data in pull]
        gevent.joinall(jobs)
        for job in jobs:
            out_queue.put(job.value)
