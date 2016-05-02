import urllib2
import json
import simplejson
import os
import pdb
from appflux.django.appflux_exception import AppfluxException

class Notify:
    def __init__(self, exception_object):
        if AppfluxException.before != []:
            for before_callback in AppfluxException.before:
                before_callback(exception_object, exception_object.global_attributes)

        json_response = exception_object.process_default_exception_data()
        json_response['bugflux']['app_id'] = 'fVKhia5dwDbQZLu5iiGtTwGi' #os.environ.get('AppfluxAppID', None)

        if AppfluxException.after != []:
            for after_callback in AppfluxException.after:
                after_callback(exception_object, exception_object.global_attributes)

        print simplejson.dumps(json_response)

        self.send(simplejson.dumps(json_response))

    def send(self, json_response):
        urllib2.urlopen('http://appflux.io/exceptions', json_response)
