import urllib2

class Notify:
    def __init__(self, payload):
        self.payload = payload
        self.send()

    def send(self):
        urllib2.urlopen('http://localhost:3000/admin/faq/sites', self.payload)
