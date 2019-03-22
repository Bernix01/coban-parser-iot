import logging
import sys
import socketserver
from parser.parser import generarDatosPeticion, generar_respuesta
from .gprs_socket_client import send_data, create_client, send_login
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


class EchoRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request,
                                                 client_address,
                                                 server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Echo the back to the client
        data = self.request.recv(1024)
        self.logger.debug('recv()->"%s"', data)
        datagram = str(data, 'utf-8')
        if not(datagram.startswith('@@')):
            self.request.send('bye'.encode('utf-8'))
            return
        data_dict = generarDatosPeticion(datagram)
        self.server.client.close()
        try:
            if (send_login(self.server.client, data_dict["Dispositivo"])):
                send_data(data_dict, self.server.client)
        except:
            self.logger.debug('coban -> reconnecting')
            self.server.client.close()
            self.server.client = create_client(self.server.coban_address,self.server.coban_port)
            if (send_login(self.server.client, data_dict["Dispositivo"])):
                send_data(data_dict, self.server.client)
        self.request.send(generar_respuesta(data_dict).encode('utf-8'))
        return

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)


class GPSSocketServer(socketserver.TCPServer):
    client = None
    coban_address = ''
    coban_port = 0

    def __init__(self, server_address,
                 handler_class=EchoRequestHandler, coban_address='', coban_port=0
                 ):
        self.logger = logging.getLogger('GPSTranslator')
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_address,
                                        handler_class)
        self.coban_address = coban_address
        self.coban_port = coban_port
        self.client = create_client(coban_address, coban_port)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug('waiting for request')
        self.logger.info(
            'Handling requests, press <Ctrl-C> to quit'
        )
        socketserver.TCPServer.serve_forever(self, poll_interval)
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.verify_request(
            self, request, client_address,
        )

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.process_request(
            self, request, client_address,
        )

    def server_close(self):
        self.logger.debug('server_close')
        if self.client:
            self.client.close()
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.finish_request(
            self, request, client_address,
        )

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(
            self, request_address,
        )

    def shutdown(self):
        self.logger.debug('shutdown()')
        return socketserver.TCPServer.shutdown(self)
