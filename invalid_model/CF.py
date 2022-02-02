# -*- coding: utf-8 -*-
import re


class TerminationUnpaidAnnualFee:
    name = '未缴年费终止表'

    def __init__(self, queue):
        self.Patent_number = re.findall(r'ZL [0-9a-zA-Z.\d]{10,14}', queue[1])[0]

    def Insert(self, db):
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data, source)'
            'values (%s,%s,%s,%s,%s,%s);',
            (0, 'CF01', db.publishTime, db.split_patent(self.Patent_number), '未缴年费专利权终止', db.filename))
