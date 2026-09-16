import datetime
import os

class tools:

    def __init__(self, cursor, sql_table):
        self.tool_list = [self.read_directories, self.directory_permissions, self.request_directory_access]
        self.cursor = cursor
        self.sql_table = sql_table

    def get_all_tools(self):
        return self.tool_list

    def directory_permissions(self, directory_path: str):
        # first check if permission already granted (!!!!!CHANGE TO SQL QUERY)
        cursor = self.cursor

        query_result = self.sql_table.specific_query(cursor, 'filepath', directory_path, 'path_access_perms')

        if query_result == directory_path:
            return "Permission To Access Already Granted"

        else:
            if self.request_directory_access(directory_path) is True:
                #update sql table for permissions

                self.sql_table.create_table(cursor, 'path_access_perms', columns = {
                "id": "INT AUTO_INCREMENT PRIMARY KEY",
                "filepath": "VARCHAR(512) NOT NULL UNIQUE",
                #"permission_type": "ENUM('read', 'write', 'execute') DEFAULT 'read'",
                #"active": "BOOLEAN DEFAULT 1",
                "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                #"description": "VARCHAR(255)"
                })

                data = {
                   "filepath": directory_path,
                   #"permission_type": "read",
                   #"description": "Granted at runtime"
                }

                self.sql_table.create_entry('path_access_perms', data, cursor)

                return f"Permission Granted for {directory_path}"

            else:
                return f"Permission denied for {directory_path}"

    def request_directory_access(self, directory_path:str):
        answer = input(f"Do you allow this model to access {directory_path}? (y or n)")
        tmp = False
        while True:
            if answer == "y":
                tmp = True
                break
            elif answer == "n":
                tmp = False
                break
            else:
                print("Invalid response, please respond with y or n")
        return tmp

    def read_directories(self, directory_path:str):
        """Read the files from directory_path ONLY"""
        # first verify permissions
        perm_result = self.directory_permissions(directory_path)
        if perm_result not in ("Permission To Access Already Granted", f"Permission Granted for {directory_path}"):
            return perm_result

        list = []
        try:
            for root, dirs, files in os.walk(directory_path):
                for d in dirs:
                    list.append(f"Directory: {os.path.join(root, d)}")
                for f in files:
                    list.append(f"Files: {os.path.join(root, f)}")
            return list

        except:
            return f"There was an error with the tool call"

