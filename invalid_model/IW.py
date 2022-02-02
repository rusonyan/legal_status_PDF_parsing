# -*- coding: utf-8 -*-
import re


class PatentInvalidation:
    name = '专利权全部无效表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"(\d\d-\d\d)", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        if state:
            self.Main_classification = queue[0]
            self.Patent_number = re.findall(r'ZL [0-9a-zA-Z.\d]{10,14}', queue[1])[0]
            self.Authorization_announcement_date = queue[2]
            self.Invalidation_decision_number = queue[3]
            self.Invalidation_decision_date = re.findall(r'\d\d\d\d\.\d\d\.\d\d', queue[4])[0]
        else:
            print("错误！创建专利权全部无效对象失败")

    def Insert(self, db):
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data, source)'
            'values (%s,%s,%s,%s,%s,%s);',
            (0, 'IW01', self.Invalidation_decision_date, db.split_patent(self.Patent_number),
             '专利权全部无效\n无效宣告决定日:' +
             self.Invalidation_decision_date +
             '\n无效宣告决定号:' + self.Invalidation_decision_number,
             db.filename
             ))
