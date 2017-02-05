from __future__ import absolute_import

from celery.signals import task_failure
from appflux.notify import Notify
import traceback
import sys

class AppfluxException:
    def __init__(self, app_id):
        self.app_id = app_id
        task_failure.connect(self.exception_handler, weak=False)

    def exception_handler(self, exception, args, sender, task_id, kwargs, signal, traceback, einfo):
        self.exception = exception
        self.args = args
        self.kwargs = kwargs
        self.traceback_line = traceback
        Notify(self)

    def process_default_exception_data(self):
        _exception_response_hash = {}
        _exception_message = _exception_response_hash['exception'] = {}
        exc_type, exc_value, exc_traceback = sys.exc_info()
        _exception_message['backtrace'] = traceback.format_tb(exc_traceback)
        _exception_message['class'] = sys.exc_info()[0].__name__
        _exception_message['message'] = str(sys.exc_info()[1])
        # _exception_response_hash['exception'] = str(self.exception)
        _exception_response_hash['args'] = self.args
        _exception_response_hash['kwargs'] = self.kwargs
        # _exception_response_hash['traceback'] = traceback.format_exc(self.traceback_line)
        return _exception_response_hash
