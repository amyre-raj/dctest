import requests
import time
 
class pdi:

    def __init__(self, in_ip):
        self.url = in_ip + "/restapi/relay/outlets/"
        self.headers = {'X-CSRF': 'x'}
        self.payload = {'value':'false'}
        self.auth = requests.auth.HTTPBasicAuth('admin','1234')

    def send(self,payload, outlet):
        r = requests.put(self.url + str(outlet-1) + "/state/", auth=self.auth ,data=self.payload,headers=self.headers)

    def on(self, outlet):
        self.payload = {'value':'true'}
        self.send(self.payload, outlet)

    def off(self, outlet):
        self.payload = {'value':'false'}
        self.send(self.payload, outlet)

    def setup(self):
        for i in range(1,8):
            self.off(i)

if __name__ == "__main__": 

    pdu = pdi("http://172.23.5.188")

    # turn off all outlets
    pdu.setup()

    # turn on outlet 3
    pdu.on(1)
    pdu.on(2)
    
    #time.sleep(3)
    #pdu.off(3)