import traceback
import pdb
import json
from appflux.django.appflux_exception import AppfluxException

class AppfluxMiddleware:

    def __init__(self):
        self.request_hash = {}
        self.request_hash['bugflux'] = { }

    def process_exception(self, request, exception):
        if AppfluxException.before != []:
            for before_callback in AppfluxException.before:
                before_callback(self, request, exception)
        # _bugflux_request_hash = Appflux['api_key']

        json_response = self.process_default_exception_data(request, exception)

        if AppfluxException.after != []:
            for after_callback in AppfluxException.after:
                after_callback()
        print json_response

    def process_default_exception_data(self, request, exception):
        _bugflux_request_hash = self.request_hash['bugflux']
        _env_request_hash = _bugflux_request_hash['env'] = { }
        _env_request_hash['request'] = self.process_request_object(request)
        _env_request_hash['session'] = request.COOKIES
        _env_request_hash['params'] = self.process_params_object(request)
        _env_request_hash['headers'] = self.process_meta_data(request)
        _bugflux_request_hash['exception'] = traceback.format_exc()
        return json.dumps(self.request_hash)

    def add_tab(self, key, data):
        self.request_hash['bugflux'][key] = data

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
