import json
from http import HTTPStatus


class HTTPResponse:
    __slots__ = ("status", "version", "headers", "body")

    def __init__(self):
        self.status     = HTTPStatus.OK
        self.version    = ""
        self.headers    = {}
        self.body       = {}


    def stringify(self):
        result = "{} {} {}\r\n".format(
            self.version,
            self.status.value,
            self.status.phrase
        )

        for field in self.headers.items():
            result += field[0] + ": " + str(field[1]) + "\r\n"

        if self.body != "":
            result += "\r\n"

            result += str(self.body)

        return result

            
"""
Basic HTTP handler containing basic methods requried to handle requests
"""
class BasicHTTPHandler:
    def __init__(self, server, request):
        self._server = server
        self._request = request


        # response part
        self._response = HTTPResponse()

        self._error = False


        try:
            self.handle()
        finally:
            self.finalize()


    """
    Methods for accessing request
    """
    def requestGetMethod(self):
        return self._request.method

    def requestGetPath(self):
        return self._request.path

    def requestParamsGetOr(self, name, alternative):
        return self._request.params.get(name, alternative)

    def requestHeaderGetOr(self, name, alternative = None):
        return self._request.headers.get(name, alterantive)

    def requestGetBody(self):
        return self._request.body


    """
    Methods for setting response
    """
    def responseHeaderPutAt(self, name, value):
        self._response.headers[name] = value


    def responseSetStatus(self, status):
        self._response.status = status


    def responseSetBody(self, text):
        self._response.body = text


    def responseBodyAdd(self, text):
        self._response.body += text


    """
    Signals that error was encountered and error page should be showed
    Override if custom response is warranted
    """
    def signalError(self, status, message = "", hideMessage = False):
        self.getServer().logError("{} {}: {}".format(
            status.value,
            status.phrase,
            status.description if message == "" else message
        ))

        
        self._error = True
        
        self.responseSetStatus(status)
        self.responseSetBody(status.description if hideMessage else message)


    """
    Method called to handle request itself
    """
    def handle(self):
        self.getServer().logInfo("{} {}".format(
            self.requestGetMethod().upper(),
            "/".join(self.requestGetPath())
        ))

        
        httpMethodName = "do{}".format( self.requestGetMethod() )

        httpMethodObj = None


        try:
            httpMethodObj = getattr(self, httpMethodName)

        except:
            self.signalError(HTTPStatus.NOT_IMPLEMENTED)

            return None

        httpMethodObj()


        
    """
    Method called after request is handled
    """
    def finalize(self):
        pass

    """
    Some handy getters
    """
    def getRequest(self):
        return self._request

    def getResponse(self):
        return self._response

    def getServer(self):
        return self._server

    def hasError(self):
        return self._error




class FrameworkHTTPHandler(BasicHTTPHandler):
        
    
    """
    Imports requested module and pulls object from it
    Whem error happends, reports it and returns None
    TODO: Implement caching
    """
    def importFrom(self, modulePath, objectName):
        theModule = None

        try:
            theModule = __import__(modulePath, None, None, [objectName], 0)

        except ModuleNotFoundError as e:
            self.signalError(HTTPStatus.NOT_FOUND, "{} {} not found".format(objectName, modulePath))

        except BaseException as e:
            self.signalError(HTTPStatus.INTERNAL_SERVER_ERROR, "{} import/execution failure".format(modulePath))


        return theModule



        
    """
    Evaluates standard interaction for accessing endpoint

    """
    def evaluateEndpoint(self):
        ## create path to endpoint. If endpoint is empty, defualt to "root"
        ## NOTE: currently we don't suport sub-directories - all controllers must be in same dir
        endpointName = "root"

        if self.requestGetPath()[-1] != "":
            endpointName = self.requestGetPath()[-1]
        

        endpointPath = "app.controllers.{}".format(endpointName)   


        ## create name of the action - if action is missing, default to "index"
        ## we also append http method

        actionName      = self.requestParamsGetOr("action", ["index"])[0]
        fullActionName  = self.requestGetMethod() + "_" + actionName


        ## steal controller
        controllerModule = self.importFrom(endpointPath, "Controller")

        if self.hasError():
            return None

        controller = controllerModule.Controller(
            self.getServer().getStorage(),  # storage manager - access to db
            None,                           # shared data - currently not implemented
            self.getRequest().params,       # parameters from url
            self.getRequest().body          # data from request body
        )


        ## try to get correct action
        actionResult = None

        try:
            actionMethod = getattr(controller, fullActionName)
            actionResult = actionMethod()
        
        except AttributeError as e:
            self.signalError(
                HTTPStatus.METHOD_NOT_ALLOWED,
                "{} not supported by {}".format(
                    self.requestGetMethod(),
                    actionName
                )
            )

            return None

        except Exception as e:
            self.signalError(HTTPStatus.INTERNAL_SERVER_ERROR, e, True)

            return None
        

        ## get action result and do specific stuff based on it
         

        try:
            orderMethod = getattr(self, actionResult.order)

            return orderMethod(actionResult.data)

        except AttributeError:
            self.signalError(
                HTTPStatus.ITNERNAL_SERVER_ERROR,
                "Unknown action's order"
            )

            return None

        except e:
            self.signalError(HTTPStatus.INTERNAL_SERVER_ERROR, e, True)

            return None

    """
    Handlers of ActionResult orders
    """
    def retView(self, data):
        # TODO: some parts shared with endpoint eval, possible refactor?
        actionName      = self.requestParamsGetOr("action", ["index"])[0]
        fullActionName  = self.requestGetMethod() + "_" + actionName

        
        endpointName = "root"

        if self.requestGetPath()[-1] != "":
            endpointName = self.requestGetPath()[-1]


        # construct path and impir t
        viewPath = "app.views.{}.{}".format(
            endpointName,
            fullActionName
        )

        ## import view module, call it and return result
        viewModule = self.importFrom(viewPath, "View")

        if self.hasError():
            return None

        try:
            return viewModule.View(data)
        except e:
            self.signalError(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                str(e)
            )
        
            return None

        
    def retJson(self, data):
        return json.dumps(data)

    def retError(self, data):
        self.signalError(data["status"], data["message"])

        return None



    """
    Finds and reads public resource (javascript, css, images, videos)
    """
    def evaluateResource(self):
        resourcePath = "app\\resources" + "\\".join(self.requestGetPath())
        print(resourcePath)

        content = None

        try:
            with open(resourcePath) as fileObj:
                allContent = fileObj.read()

                return allContent

            

        except OSError:
            self.signalError(HTTPStatus.NOT_FOUND, "Resource {} not found".format(
                self.requestGetPath()[-1]
            ))

        return None


    """
    Shared code between GET and HEAD
    This is done because HEAD is supposed to be GET without body
    """
    def sharedHeadGet(self):
        # no "." in name? Must be endpoint
        if not "." in self.requestGetPath()[-1]:
            return self.evaluateEndpoint()


        # otherwise it is resource
        return self.evaluateResource()
        

    """
    Handles GET request
    It accepts both endpoints and resources
    """
    def doGET(self):
        result = self.sharedHeadGet()
        
        if result:
            self.responseSetBody(result)    
        
    
    """
    Handles HEAD requests
    It works same way as GET, but body is thrown away instead
    """
    def doHEAD(self):
        # mehod must be changed to GET
        self._request.method = "GET"
        
        # result is ignored in 
        self.sharedHeadGet()

    """
    Handles POST requests.
    Resource files are not allowed and are handled by status error
    """
    def doPOST(self):
    
        # resource files are not allowed in post requests
        if "." in self.requestGetPath()[-1]:
            self.signalError(HTTPStatus.METHOD_NOT_ALLOWED)

            # also note that only GET/HEAD can be used
            self.responseHeaderPutAt("Allow", "GET, HEAD")

            return None

        # evaluate endpoint and return it
        result = self.evaluateEndpoint()

        if result:
            self.responseSetBody(result)    
