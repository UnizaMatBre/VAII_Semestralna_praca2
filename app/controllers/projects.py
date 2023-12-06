from http import HTTPStatus
import base_controller


class Controller(base_controller.BaseController):
    def GET_index(self):
        projects = self.getStorage().selectJson(
            "Projects",
            ("name", "description")
        )

        return self.retJson(projects)


    def POST_index(self):
        name = self.bodyfieldGetOr("name", None)
        desc = self.bodyfieldGetOr("description", None)

        if name == None or desc == None:
            return self.retError(HTTPStatus.BAD_REQUEST)

        rowId = self.getStorage().insert("Projects", {
            "name":         name,
            "description":  desc
        })

        return self.retJson({
            "rowid": rowId,
            "name": name,
            "description": desc
        })