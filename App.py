import os
import pprint
import shutil
from sql import DB

import pdfplumber

from differentiation_model import DifferentiationModel
from table_spilt import TableSpilt


class App:
    """
    测试类
    """
    def __init__(self, filename):
        self.filename = filename
        self.handle()
        self.db = DB()

    def handle(self):
        state = None
        this_table = []
        lines = []

        file_path = self.filename
        with pdfplumber.open(self.filename) as pdf:
            for x in pdf.lines:
                if x['linewidth'] > 1.4:
                    lines.append(x)

            bk_path = TableSpilt(lines, pdf).get_this_name() + '事务公告备份'
            end = os.path.join(os.path.expanduser("~"),
                               'Desktop') + '\\' + bk_path
            if not os.path.exists(end):
                os.mkdir(end)

            i = 0
            a = set()
            # for x in pdf.chars:
            #     if x['text']=='主':
            #         # pprint.pprint(x)
            #         a.add(x['fontname'])
            #         i=i+1
            # print(i)
            # pprint.pprint(a)
            # b=TableSpilt(lines, pdf).return_serialized_data()

            for t in TableSpilt(lines, pdf).return_serialized_data():
                DifferentiationModel().differentiation(t, bk_path, self.db)

            shutil.copyfile(file_path,
                            end + '//' + os.path.split(file_path)[1])
            shutil.copy(os.getcwd() + '//' + '使用前必读.md', end)

            self.db.Insert()


#conding=utf8
import json
import os
import sys
import shutil
import time
import zipfile


# 判断是不是pdf
def scan_zip(path):
    if path.endswith('.pdf'):
        return True
    return False


# 获取所有文件夹
def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)
    return Filelist


def main(path):
    list = get_filelist(path, [])

    for f in list:
        zip_file = scan_zip(f)
        if zip_file:
            print(f)
            App(f)


a = App('WGSW2621.pdf')
#main(r'C:\Users\ruson\Desktop\事务数据\2010')