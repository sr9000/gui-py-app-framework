from enum import Enum, auto
from threading import Lock
from typing import Tuple, Callable, Optional, Any

from kthread import KThread


class Task:
    class WorkCancelException(Exception):
        pass

    class State(Enum):
        Stop = auto()
        Work = auto()
        Done = auto()
        Wait = auto()

    class Status(Enum):
        Pausing = auto()
        Resuming = auto()
        Cancelling = auto()
        Killing = auto()

    _ping_callback: Tuple[Callable[[], None]] = ((lambda: None),)
    _force_ping_callback: Tuple[Callable[[], None]] = ((lambda: None),)
    _workload: Tuple[Callable[[Callable[[], None], Callable[[float], None]], Any]] = ((lambda p, u: (p(), u(1.0))),)
    _pause_lock: Lock
    _thread: Optional[KThread]

    status: Optional[Status]
    state: State
    progress: float

    def __init__(self) -> None:
        self._init()

    def _init(self):
        self.state = self.State.Stop
        self.status = None
        self._pause_lock = Lock()
        self._thread = None
        self.progress = 0.0

    def set_callback(self, ping: Callable[[], None], force_ping: Callable[[], None]) -> None:
        self._ping_callback = (ping,)
        self._force_ping_callback = (force_ping,)

    def set_workload(self, workload: Callable[[Callable[[], None], Callable[[float], None]], None]) -> None:
        """workload(ping: ()->Any, progress_update: (float)->None)
        If needed, catch exception WorkCancelException.
        Use ping() as often as u can.
        Dont forget progress_update with 0 .. 1.0"""
        self._workload = (workload,)

    def start(self):
        if self.state is self.State.Stop:
            self._thread = KThread(target=self._exec)
            self._thread.setDaemon(True)
            self._thread.start()

    def pause(self) -> None:
        if self.state is self.State.Work:
            if self.status is None:
                self.status = self.Status.Pausing
            self._force_ping_callback[0]()
            self._pause_lock.acquire()

    def resume(self) -> None:
        if self.state is self.State.Wait:
            if self.status is None:
                self.status = self.Status.Resuming
                self._force_ping_callback[0]()
            self._pause_lock.release()

    def cancel(self):
        if self.state in (self.State.Work, self.State.Wait):
            self.status = self.Status.Cancelling
            self._force_ping_callback[0]()
        self.resume()

    def finish(self):
        if self.state is self.State.Done:
            self.state = self.State.Stop
            self._init()

    def kill(self):
        if self.state not in (self.State.Stop, self.State.Done):
            self._thread.kill()
            self.status = self.Status.Killing
            self.resume()
            self._init()
            self._force_ping_callback[0]()

    def _exec(self):
        try:
            self.progress = 0.0
            self.state = self.State.Work
            self._workload[0](self._ping, self._update_progress)
            self.state = self.State.Done
        except self.WorkCancelException:
            self.state = self.State.Stop

        self._force_ping_callback[0]()

    def _ping(self) -> None:
        """Signalling, that task is alive an work still in progress.
        Used by workload implementation"""
        self._ping_callback[0]()
        self._check_pause()
        self._check_cancel()

    def _update_progress(self, progress: float):
        self.progress = progress

    def _check_pause(self) -> None:
        if self.status is self.Status.Cancelling:
            return

        if self._pause_lock.locked():
            assert self.status is self.Status.Pausing
            self.status = None
            self.state = self.State.Wait
            self._force_ping_callback[0]()

            self._pause_lock.acquire()
            self._pause_lock.release()

            self.state = self.State.Work
            if self.status is self.Status.Resuming:
                self.status = None
                self._force_ping_callback[0]()

    def _check_cancel(self) -> None:
        if self.status is self.Status.Cancelling:
            self.status = None
            raise self.WorkCancelException()
