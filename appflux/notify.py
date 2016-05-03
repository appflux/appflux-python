import urllib2
import requests
# import json
from json import JSONEncoder
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
        json_response['app_id'] = 'm1LGnkC1zELcSTjb12vWRQni' #os.environ.get('AppfluxAppID', None)

        if AppfluxException.after != []:
            for after_callback in AppfluxException.after:
                after_callback(exception_object, exception_object.global_attributes)

        self.send(JSONEncoder().encode(json_response))

    def send(self, json_response):
        requests.post('http://localhost:3000/exceptions', json={ 'bugflux': json_response })
