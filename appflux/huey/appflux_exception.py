import redis
import ast
import threading
from appflux.notify import Notify

class AppfluxException(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        if(item['type'] == 'message'):
            result = str(item['data']).replace('true', 'True').replace('false', 'False').replace('null', 'None')
            self.json_response = ast.literal_eval(result)
            if(self.json_response['status'] == 'error-task'):
                Notify(self)

    def process_default_exception_data(self):
        self.json_response

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item)
