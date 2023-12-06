import socket
import json
import datetime
from email.utils import formatdate
from urllib.parse import urlparse, parse_qs



"""
Class representing request
It allows simple access to parts of response.
It contains parser for text form of request 
"""
class HTTPRequest:
    __slots__ = ("method", "path", "params", "version", "headers", "body")


    @classmethod
    def fromText(cls, text):
        ## instance
        instance = cls()

        ## steal starter from request
        starterText, rest = text.split("\r\n",  1)

        ## steal body and turn it into JSON
        ## NOTE: only json is currently supported 
        headerText, bodyText = rest.split("\r\n\r\n")
                

        ## parse starter
        instance.method, pathText, instance.version = starterText.split(" ")


        ## path needs extra care
        parsedPath = urlparse(pathText)
        
        instance.path = parsedPath.path.split("/")

        instance.params = parse_qs(parsedPath.query)
        
        ##upper method just in case
        instance.method = instance.method.upper()

        
        ## parse headers
        for line in headerText.split("/r/n"):
            name, value = line.split(":", 1)

            # handle arrayed values
            if "," in value:
                value = value.split(",")

            instance.headers[name] = value

        
        ## parse body
        if bodyText.strip() != "":
            instance.body = json.loads(bodyText)


        return instance
    
    def __init__(self):
        self.method     = None
        self.path       = None
        self.params     = {}
        self.version    = None

        self.headers    = {}
        self.body       = {}



    
"""
Class representing server handling HTTP requests
It listens on specific port, parses requests and pass them to handler.
"""
class HTTPServer:
    def __init__(self, host, storage, logger, handlerClass):
        self._host      = host
        self._storage   = storage
        self._logger    = logger

        self._handlerClass = handlerClass

        self._halted = False

        print(storage)

    def getStorage(self):
        return self._storage

    def getFullAddress(self):
        return "http://{}:{}".format(self._host[0], self._host[1])

    """
    Runs loop that listen to port, parsing requests and returning responses
    Loop can be broken by setting _halted to true
    """
    def start(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind(self._host)
        serverSocket.listen(1)

        try:
            while not self._halted:
                clientConnection, clientAddress = serverSocket.accept()

                requestText = clientConnection.recv(1024).decode()

                request = HTTPRequest.fromText(requestText)
                
                # pass controll to handler
                handler = self._handlerClass(self, request)

                

                ## get response
                response = handler.getResponse()


                ## fill headers with server informations
                response.version            = request.version
                response.headers["Server"]  = "MyPythonServer 1.0.0"
                response.headers["Date"]    = formatdate(timeval=None, localtime=False, usegmt=True)

                responseText = response.stringify().encode()
                
                clientConnection.sendall(responseText)
                clientConnection.close()
                
        finally:
            serverSocket.close()



    def logError(self, text):
        now = datetime.datetime.now()
        
        message = "({})[ERRO]: {}".format(
            now,
            text
        )

        self._logger(message)


    def logInfo(self, text):
        now = datetime.datetime.now()
        
        message = "({})[INFO]: {}".format(
            now,
            text
        )

        self._logger(message)

    
