# -*- coding: utf-8 -*-
from config import PC_TEMPLATE
from special_mode.Validator import validator


class PC:
    name = '专利权质押合同登记的注销'

    def __init__(self, queue):
        self.queue = queue
        if len(queue) != 8 or validator(queue, PC_TEMPLATE):
            raise Exception("专利权质押合同登记的生效解析错误")

    def Insert(self, db):
        queue = self.queue
        db.cursor.execute('insert into pc (id, patent_id, license_num,pub_date, pledger, pledgee ) '
                          'values (%s,%s,%s,%s,%s,%s);',
                          (0, db.split_patent(queue[1]), queue[4], queue[5], queue[6], queue[7]))
        raw_data = '''专利权质押合同登记的注销
专利号:{0}
登记号:{1}
解除日:{2}
出质人:{3}
质权人:{4}'''.format(queue[1], queue[4], queue[5], queue[6], queue[7])
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data,change_id, source)'
            'values (%s,%s,%s,%s,%s,%s,%s);',
            (0, 'PC01',
             queue[5],
             db.split_patent(queue[1]),
             raw_data,
             db.back()[0],
             db.filename
             ))
