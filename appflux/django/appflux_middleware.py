import traceback
import pdb
import sys
from appflux.django.appflux_exception import AppfluxException
from appflux.notify import Notify

class AppfluxMiddleware:

    def __init__(self):
        self.request_hash = {}

    def process_exception(self, request, exception):
        self.request = request
        self.exception = exception
        self.global_attributes = {}
        self.global_attributes['request'] = request
        self.global_attributes['exception'] = exception
        Notify(self)

    def process_default_exception_data(self):
        _bugflux_request_hash = self.request_hash
        _env_request_hash = _bugflux_request_hash['env'] = { }
        _env_request_hash['request'] = self.process_request_object(self.request)
        _env_request_hash['session'] = self.request.COOKIES
        _env_request_hash['params'] = self.process_params_object(self.request)
        _env_request_hash['headers'] = self.process_meta_data(self.request)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # print '************************************************************************************************************************************************************************************************************************************************'
        # print sys.exc_info()[1]
        # print '************************************************************************************************************************************************************************************************************************************************'
        # print traceback.print_tb(exc_traceback)
        # print '************************************************************************************************************************************************************************************************************************************************'
        # print traceback.print_exception(exc_type, exc_value, exc_traceback)
        # print '************************************************************************************************************************************************************************************************************************************************'
        # print traceback.extract_stack()
        # print '************************************************************************************************************************************************************************************************************************************************'
        # print traceback.format_tb(exc_traceback)
        # print '************************************************************************************************************************************************************************************************************************************************'
        _exception_message = _bugflux_request_hash['exception'] = {}
        _exception_message['backtrace'] = traceback.format_tb(exc_traceback)
        _exception_message['class'] = sys.exc_info()[0].__name__
        _exception_message['message'] = str(sys.exc_info()[1])

        return self.request_hash

    def add_tab(self, key, data):
        self.request_hash['custom_tabs'] = {
            key: data
        }

    def process_params_object(self, request):
        _request_hash = {}
        _request_hash['GET'] = request.GET
        _request_hash['POST'] = request.POST
        return _request_hash

    def process_request_object(self, request):
        _request_hash = {}
        _request_hash['scheme'] = request.scheme
        _request_hash['body'] = request.body
        _request_hash['path'] = request.path
        _request_hash['path_info'] = request.path_info
        _request_hash['method'] = request.method
        _request_hash['encoding'] = request.encoding
        return _request_hash

    def process_meta_data(self, request):
        meta_data = request.META
        meta_data.pop('wsgi.errors', None)
        meta_data.pop('wsgi.input', None)
        meta_data.pop('wsgi.file_wrapper', None)
        return meta_data
