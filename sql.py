import pyodbc


class DB:
    def __init__(self):
        self.cn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Patentlog;UID=ruson;PWD=yanruisong'
        )
        self.cursor = self.cn.cursor()
        self.queue = []

    def add(self, sql_str):
        self.queue.append(sql_str)

    def Insert(self):  #事务处理写库操作
        try:
            for single in self.queue:
                self.cursor.execute(single)
                print(single)
        except pyodbc.DatabaseError as err:
            self.cn.rollback()
        else:
            self.cn.commit()
        finally:
            self.cn.autocommit = True