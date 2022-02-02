# -*- coding: utf-8 -*-
import re


class ExpiryOfThePatentRight:
    name = '专利有效期满注销表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"\d\d-\d\d", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        if len(queue) >= 3:
            if state:
                self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
                self.Patent_number = re.findall(r'ZL [0-9a-zA-Z.\d]{10,14}', queue[1])[0]
            else:
                print("错误！创建专利有效期满对象失败")
        else:
            self.Patent_number = re.findall(r'ZL [0-9a-zA-Z.\d]{10,14}', queue[1])[0]

    def Insert(self, db):
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data, source)'
            'values (%s,%s,%s,%s,%s,%s);',
            (0, 'CX01', db.publishTime, db.split_patent(self.Patent_number), '专利权有效期届满', db.filename))
