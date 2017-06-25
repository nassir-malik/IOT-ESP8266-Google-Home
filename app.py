import websockets
import asyncio
import json
import time
# import logging
import threading
<<<<<<< HEAD
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# ws_logger = logging.getLogger('websockets.server')
# ws_logger.setLevel(logging.INFO)
=======
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
        print(self.data)
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
    port = int(os.getenv('PORT', 80))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='', threaded=True)

def webSocketServer():
    port = int(os.getenv('PORT', 5000))
    print("Starting webSocketServer on port %d" % port )
    server = SimpleWebSocketServer('', port, SimpleChat)
    server.serveforever()

if __name__ == '__main__':
    t1 = threading.Thread(target=flaskServer, args=(address1,))
    t2 = threading.Thread(target=webSocketServer)
    t1.start()
    t2.start()
>>>>>>> origin/master

# logger = logging.getLogger(__name__)

class HttpWSSProtocol(websockets.WebSocketServerProtocol):
    rwebsocket = None
    rddata = None
    async def handler(self):
        try:
            request_line, headers = await websockets.http.read_message(self.reader)
            method, path, version = request_line[:-2].decode().split(None, 2)

        except Exception as e:
            print(e.args)
            self.writer.close()
            self.ws_server.unregister(self)

            raise

        # TODO: Check headers etc. to see if we are to upgrade to WS.
        if path == '/ws':
            # HACK: Put the read data back, to continue with normal WS handling.
            self.reader.feed_data(bytes(request_line))
            self.reader.feed_data(headers.as_bytes().replace(b'\n', b'\r\n'))

            return await super(HttpWSSProtocol, self).handler()
        else:
            try:
                return await self.http_handler(method, path, version)
            except Exception as e:
                print(e)
            finally:

                self.writer.close()
                self.ws_server.unregister(self)


    async def http_handler(self, method, path, version):

        try:
            await self.rwebsocket.send(json.dumps(self.reader._buffer.decode('utf-8')))
            print('In http function:')
            self.rddata = await self.rwebsocket.recv()
            print('Out HTTP function:')
            print("HTTP function")

            response = '\r\n'.join([
                'HTTP/1.1 200 OK',
                'Content-Type: text/html',
                '',
                '<html><body><h1>'+self.rddata+'</h1></body></html>',
            ])
        except Exception as e:
            print(e)
        self.writer.write(response.encode())

def updateData(data):
    HttpWSSProtocol.rddata = data

async def ws_handler(websocket, path):
    #logger.info('Client connecting: %s, %s', websocket, path)
    game_name = 'g1'

    try:
        #g, player_name = join_game(game_name, websocket)
        HttpWSSProtocol.rwebsocket = websocket
        await websocket.send(
            json.dumps({'event': 'init', 'player_name': "test", 'score': ['score']})
        )
        data ='{"empty":"empty"}'
        while True:
        #     #data = await websocket.recv()
            print('In ws function:')
            data = await websocket.recv()
            print('Out ws function:')
        #
        #logger.info('data: %s', data)
        #     data = json.loads(data)
            updateData(data)
        print('From sock func:' + str(data))

            #handle_event(g, player_name, data, websocket)

    finally:
        #logger.info(u'Disconnecting client and leaving game')
        #leave_game(websocket)
        print("")


start_server = websockets.serve(ws_handler, '0.0.0.0', 80, klass=HttpWSSProtocol)
# logger.info('Listening on port %d', port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
