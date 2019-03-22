from socketter.gps_socket_server import GPSSocketServer, EchoRequestHandler
import logging

if __name__ == '__main__':
    import socket
    import threading

    address = ('0.0.0.0', 8080)  # let the kernel assign a port
    server = GPSSocketServer(
        address, EchoRequestHandler, '217.23.132.215', 47750)
    ip, port = server.server_address  # what port was assigned?

    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)
    server.serve_forever()
    # Start the server in a thread
    # t = threading.Thread(target=server.serve_forever)
    # t.setDaemon(True)  # don't hang on exit
    # t.start()
