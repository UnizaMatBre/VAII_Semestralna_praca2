import sqlite3


class StorageManager:
    def __init__(self, dbLocation):
        self._connection = sqlite3.Connection(dbLocation)

    def __del__(self):
        self._connection.close()


    def insert(self, modelName, dictionary):
        names   = dictionary.keys()
        values  = dictionary.values()
        
        cursor = None

        try:
            cursor = self._connection.cursor()

            try:
                cursor.execute("CREATE TABLE {}({}) ".format(
                    modelName,
                    ",".join(names)
                ))
            # ignore exception 
            except:
                pass


            typeCheck = lambda val: repr(val) if isinstance(val, str) else str(val)

            command = "INSERT INTO {} VALUES ({})".format(
                modelName,
                ",".join(typeCheck(i) for i in values)
            )
                
            cursor.execute(command)

            
                

            rowId = cursor.lastrowid

            self._connection.commit()

            return rowId
                        
        finally:
            if cursor != None:
                cursor.close()
            

        
    def select(self, modelName, filters = None):
        cursor = None

        try:
            cursor = self._connection.cursor()

            command = "SELECT rowid, * FROM {}".format(modelName)

            if filters != None:
                command += (" WHERE " + fitlers)
            
            result = cursor.execute(command)

            return result.fetchall()

            
        except:
            return ()
        
        finally:
            if cursor != None:
                cursor.close()
    
    def selectJson(self, modelName, fields, filters = None):
        result = self.select(modelName, filters)

        resultList = []

        for values in result:
            pairs = zip(fields, values)

            resultList.append({
                pair[0]: pair[1] for pair in pairs
            })
            
        return resultList
            
        
    def delete(self, modelName, filters):
        cursor = None

        try:
            cursor = self._connection.cursor()

            command = "DELETE FROM {} WHERE {}".format(modelName, filters)
            
            cursor.execute(command)

            self._connection.commit()

            
        except:
            return []
        
        finally:
            if cursor != None:
                cursor.close()


    def update(self, modelName, rowId, changesDict):
        items = changesDict.items()
        
        cursor = None

        try:
            cursor = self._connection.cursor()

            command = "UPDATE " + modelName + "\n"

            for item in items:
                value = item[1]

                if isinstance(value, str):
                    value = repr(item[1])

                
                setter = "SET {} = {}".format(item[0], value)

                command += setter + "\n"

            command += "WHERE rowid = " + str(rowId)

            cursor.execute(command)

            self._connection.commit()
                        
        finally:
            if cursor != None:
                cursor.close()
            
