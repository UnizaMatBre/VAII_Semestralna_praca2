from http import HTTPStatus
import base_controller


class Controller(base_controller.BaseController):
    def GET_index(self):
        return self.retView()
