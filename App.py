# -*- coding: utf-8 -*-
import os
import sys
import time

import pdfplumber
from loguru import logger

from DB import DB
from DifferentiationModel import DifferentiationModel
from TableSpilt import TableSpilt
from Toast import send_errow


class App:
    """
    单个PDF源启动类
    """

    def __init__(self, filename):
        self.filename = filename
        (path, self.file) = os.path.split(filename)
        self.handle()

    def handle(self):
        with pdfplumber.open(self.filename) as pdf:
            try:
                tableSpilt = TableSpilt(pdf, self.file)
                publish_time = time.strftime("%Y-%m-%d",
                                             time.strptime(tableSpilt.get_this_name(), u"%Y年%m月%d日"))
                db = DB(self.file, publish_time, pdf)
                for t in tableSpilt.return_serialized_data():
                    DifferentiationModel().differentiation(t, db)
            except Exception as err:
                db.cn.rollback()
                send_errow('pdf', str(err))
                logger.error(str(err) + '写库失败,已回滚操作!')
                sys.exit()
            else:
                db.end()
                db.cn.commit()


if __name__ == '__main__':
    App('WGSW364802.pdf')
