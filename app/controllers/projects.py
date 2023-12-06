from http import HTTPStatus
import base_controller


class Controller(base_controller.BaseController):
    def GET_index(self):
        demandedId = self.parameterGetOr("rowid", [None])[0]
        
        filters = None

        if demandedId != None:
            filters = "rowid = {}".format(demandedId)
        
        projects = self.getStorage().selectJson(
            "Projects",
            ("rowid", "name", "description"),
            filters
        )
        
        for project in projects:
        
            # get tasks of this project
            associatedTasks = self.getStorage().selectJson(
                "Tasks",
                ("rowid", "projectid", "status", "content"),
                "projectid = {}".format(project["rowid"])
            )
            
            project["tasks"] = associatedTasks


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


    def GET_tasks(self):
        demandedId = self.parameterGetOr("rowid", [None])[0]
        
        filters = None

        if demandedId != None:
            filters = "rowid = {}".format(demandedId)
    
        tasks =  self.getStorage().selectJson(
            "Tasks",
            ("rowid", "projectid", "status", "content"),
            filters
        )

        return self.retJson(tasks)

    def POST_tasks(self):
        projectId   = self.bodyfieldGetOr("projectid", None)
        status      = self.bodyfieldGetOr("status", None)
        content     = self.bodyfieldGetOr("content", None)

        if None in (projectId, status, content):
            return self.retError(HTTPStatus.BAD_REQUEST)

        newObj = {
            "projectid":    projectId,
            "status":       status,
            "content":      content
        } 

        rowId = self.getStorage().insert("Tasks", newObj)

        newObj["rowid"] = rowId

        return self.retJson(newObj)
