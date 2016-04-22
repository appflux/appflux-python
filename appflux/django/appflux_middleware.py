import traceback
import pdb
import json

class AppfluxMiddleware:
    def process_exception(self, request, exception):
        _request_hash = { }
        _bugflux_request_hash = _request_hash['bugflux'] = { }
        _env_request_hash = _bugflux_request_hash['env'] = { }
        _bugflux_request_hash = Appflux['api_key']
        _env_request_hash['request'] = self.process_request_object(request)
        _env_request_hash['session'] = request.COOKIES
        _env_request_hash['params'] = self.process_params_object(request)
        _env_request_hash['headers'] = self.process_meta_data(request)
        _bugflux_request_hash['exception'] = traceback.format_exc()
        json_response = json.dumps(_request_hash)
        # pdb.set_trace()
        print json_response

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
