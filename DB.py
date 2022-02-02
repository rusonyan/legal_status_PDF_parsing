import re
from datetime import datetime

import cpca
import mysql.connector
from loguru import logger


class DB:
    def __init__(self, filename, publish_time, pdf):
        # self.cn = mysql.connector.connect(
        #     host='localhost', port=3306, db='legalState', user='root', password='123456', charset='utf8'
        # )
        # print("此次操作数据库为：", "legalState")

        self.cn = mysql.connector.connect(
            host='localhost', port=3306, db='test', user='root', password='123456', charset='utf8'
        )
        logger.debug("此次操作数据库为：测试库")

        self.cursor = self.cn.cursor()
        self.filename = filename
        self.publishTime = publish_time
        self.pdf = pdf

    def back(self):
        self.cursor.execute('select @@identity')
        return self.cursor.fetchone()

    def split_patent(self, str):
        result = re.findall(r'ZL ([0-9a-zA-Z.\d]{10,14})', str)[0]
        if result is None:
            raise Exception('专利号错误')
        else:
            return result

    def spilt_address(self, location):
        return cpca.transform([location], ).values[0]

    def end(self):
        self.cursor.execute('insert into change_db_log (id, handle_time, open_day, source_name)'
                            'values (%s,%s,%s,%s);',
                            (0, datetime.now(), self.publishTime, self.filename))
