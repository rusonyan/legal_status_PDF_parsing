import pyodbc


class DB:
    def __init__(self, filename, publishTime):
        # self.cn = pyodbc.connect(
        #     'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=PatentLog;UID=ruson;PWD=yanruisong'
        # )
        # print("此次操作数据库为：", "PatentLog")

        self.cn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Log;UID=ruson;PWD=yanruisong'
        )
        print("此次操作数据库为：", "LOG")

        self.cursor = self.cn.cursor()
        self.filename = filename
        self.publishTime = publishTime

    def back(self):
        self.cursor.execute('select @@identity')
        return self.cursor.fetchone()
