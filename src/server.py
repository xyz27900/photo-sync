import socket
import sys
from urllib.parse import urlparse, parse_qs

from logger import logger


class Request:
    def __init__(self, query):
        self.query = self.transform_query(query)

    @staticmethod
    def transform_query(query: dict):
        new_query = {}

        for key in query:
            value = query[key]
            if type(value) == list and len(value) == 1:
                new_query[key] = value[0]
            else:
                new_query[key] = value

        return new_query


class Response:
    def __init__(self, connection):
        self.connection = connection

    def send(self, body: str, status='200 OK'):
        response = f"HTTP/1.0 {status}\n\n{body}"
        self.connection.sendall(response.encode())


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeners = {}
        self.started = False

    def listen(self):
        self.started = True

        logger.log("Server started", scope="Server")

        while self.started:
            connection, address = self.socket.accept()
            request = connection.recv(1024).decode()
            header = request.split('\n')[0].split()
            method = header[0]
            url = header[1]
            parse_result = urlparse(url)
            path = parse_result.path
            query = parse_qs(parse_result.query)

            req = Request(query)
            res = Response(connection)

            listener = self.listeners.get(path, {}).get(method)

            if listener:
                listener(req, res)
            else:
                res.send(f"Cannot {method} {path}", '404 Not Found')

            connection.close()

    def run(self, port: int):
        try:
            self.socket.bind(('', port))
            self.socket.listen(1)
            self.listen()
        except socket.error as error:
            logger.log(f"Bind failed: {error}", scope="Server")
            sys.exit(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.started = False
        self.socket.close()
        logger.log("Server stopped", scope="Server")

    def get(self, path):
        def wrapper(listener):
            if path in self.listeners:
                self.listeners[path]['GET'] = listener
            else:
                self.listeners[path] = {'GET': listener}
            return listener

        return wrapper


server = Server()
