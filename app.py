from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
# noinspection PyUnresolvedReferences
import threading
from flask import Flask
from flask import request
import json, os
from flask import make_response
app = Flask(__name__)

clients = []
address1 = '127.0.0.1'
class SimpleChat(WebSocket):

    def handleMessage(self):
        address1 = self.address
        for client in clients:
          if client != self:
             client.sendMessage(self.address[0] + u' - ' + self.data)

    def handleConnected(self):
       print(self.address, 'connected')
       #address1 = self.address
       for client in clients:
          client.sendMessage(self.address[0] + u' - connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    #mkrsp= makeWebhookResult(req)
    #r = make_response(json.dumps(mkrsp, indent=4))
    #r.headers['Content-Type'] = 'application/json'
    clients[0].sendMessage(address1[0] + u' - ' + str(req))
    return "test"

def flaskServer(address1):
    #port = int(os.getenv('PORT', 80))
    #print("Starting app on port %d" % port)
    app.run(debug=False, port=80, host='', threaded=True)

def webSocketServer():
    #port = int(os.getenv('PORT', 5000))
    #print("Starting webSocketServer on port %d" % port )
    server = SimpleWebSocketServer('', 8000, SimpleChat)
    server.serveforever()

if __name__ == '__main__':
    t1 = threading.Thread(target=flaskServer, args=(address1,))
    t2 = threading.Thread(target=webSocketServer)
    t1.start()
    t2.start()

