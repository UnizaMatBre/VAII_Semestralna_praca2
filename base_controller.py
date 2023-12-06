from collections import namedtuple

ActionResult = namedtuple(
    "ActionResult",
    ("order", "data")
)


class BaseController:
    def __init__(self, storage, sharedData, parameters, body):
        self._storage       = storage
        self._sharedData    = sharedData
        self._params        = parameters
        self._body          = body

    def attributeGetOr(self, name, alternative):
        return self._sharedData.get(name, alternative)

    def parameterGetOr(self, name, alternative):
        return self._params.get(name, alternative)

    def bodyfieldGetOr(self, name, alternative):
        return self._body.get(name, alternative)


    def getStorage(self):
        return self._storage
    
    """
    Orders handler to load and show view
    """
    def retView(self, data = {}):
        return ActionResult("retView", data)


    """
    Orders handler to return json in body of response
    """
    def retJson(self, data = {}):
        return ActionResult("retJson", data)


    """
    Orders handler to signal error
    """
    def retError(self, status, message = ""):
        return ActionResult(
            "retError", { "status": status, "message": message }
        )
