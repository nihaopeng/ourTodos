from abc import abstractmethod
from PySide6.QtWidgets import QWidget

class Page(QWidget):
    """页面基类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("Page 必须有一个父窗口")
    
    @abstractmethod
    def fresh(self):
        """刷新页面"""
        pass

from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject
from functools import wraps

class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)

class TaskRunner(QRunnable):
    def __init__(self, func, args, kwargs, signals):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = signals

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            # print(result)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))

def run_in_thread(on_success=None, on_error=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signals = WorkerSignals()
            if on_success:
                signals.finished.connect(on_success)
            if on_error:
                signals.error.connect(on_error)

            task = TaskRunner(func, args, kwargs, signals)
            QThreadPool.globalInstance().start(task)
        return wrapper
    return decorator