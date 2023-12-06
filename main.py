import framework.server
import framework.handler
import framework.storage




server = framework.server.HTTPServer(
    host            = ("0.0.0.0", 8000),
    logger          = print,
    storage         = framework.storage.StorageManager("app\\database.db"),
    handlerClass    = framework.handler.FrameworkHTTPHandler,
)

server.start()
