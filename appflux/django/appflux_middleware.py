import traceback
import pdb

class AppfluxMiddleware:
    def process_exception(self, request, exception):
        _request_hash = {}
        _request_hash['request'] = self.process_request_object(request)
        _request_hash['cookies'] = request.COOKIES
        _request_hash['params'] = self.process_params_object(request)
        _request_hash['header'] = request.META
        _request_hash['exception_payload'] = traceback.format_exc()
        pdb.set_trace()
        print _request_hash

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
