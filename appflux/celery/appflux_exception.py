from __future__ import absolute_import

from celery.signals import task_failure
from appflux.notify import Notify
import traceback

class AppfluxException:
    def __init__(self):
        task_failure.connect(self.exception_handler, weak=False)

    def exception_handler(self, exception, args, sender, task_id, kwargs, signal, traceback, einfo):
        self.exception = exception
        self.args = args
        self.kwargs = kwargs
        self.traceback_line = traceback
        Notify(self)

    def process_default_exception_data(self):
        _exception_response_hash = {}
        _exception_response_hash['exception'] = str(self.exception)
        _exception_response_hash['args'] = self.args
        _exception_response_hash['kwargs'] = self.kwargs
        _exception_response_hash['traceback'] = traceback.format_exc(self.traceback_line)
        return _exception_response_hash
