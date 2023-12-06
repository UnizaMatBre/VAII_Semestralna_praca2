from http import HTTPStatus
import base_controller


class Controller(base_controller.BaseController):
    def GET_index(self):
        return self.retJson({ "a": 1, "b": 2 })

    
