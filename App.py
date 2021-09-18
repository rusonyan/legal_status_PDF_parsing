import os
import pprint
import shutil
from DB import DB
import pyodbc
import pdfplumber
from datetime import datetime
from differentiation_model import DifferentiationModel
from table_spilt import TableSpilt


class App:
    """
    测试类
    """
    def __init__(self, filename):
        self.filename = filename
        (path, self.file) = os.path.split(filename)
        self.handle()

    def handle(self):
        lines = []
        file_path = self.filename

        with pdfplumber.open(self.filename) as pdf:
            for x in pdf.lines:
                if x['linewidth'] > 1.4:
                    lines.append(x)

            day = TableSpilt(lines, pdf).get_this_name()
            publishTime = time.strftime("%Y-%m-%d",
                                        time.strptime(day, u"%Y年%m月%d日"))
            bk_path = day + '事务公告备份'
            end = os.path.join(os.path.expanduser("~"),
                               'Desktop') + '\\' + bk_path
            if not os.path.exists(end):
                os.mkdir(end)

            db = DB(self.file, publishTime)
            try:
                for t in TableSpilt(lines, pdf).return_serialized_data():
                    DifferentiationModel().differentiation(t, bk_path, db)
            except pyodbc.DatabaseError as err:
                print(err)
                db.cn.rollback()
                print('写库失败！ 已回滚操作!')
            else:
                db.cn.commit()
            finally:
                db.cursor.execute('INSERT INTO [dbo].[DBlog] VALUES (?,?,?)',
                                  datetime.now(), db.publishTime, db.filename)
                db.cn.autocommit = True

            self.end(end)

    def end(self, end):
        shutil.copyfile(self.filename,
                        end + '//' + os.path.split(self.filename)[1])
        shutil.copy(os.getcwd() + '//' + '使用前必读.md', end)


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