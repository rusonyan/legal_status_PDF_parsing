# -*- coding: utf-8 -*-
from config import PE_RE_TEMPLATE
from special_mode.Validator import validator


class PE:
    name = '专利权质押合同登记的生效'

    def __init__(self, queue):
        self.queue = queue
        if len(queue) != 9 or validator(queue, PE_RE_TEMPLATE):
            raise Exception("专利权质押合同登记的生效解析错误")
        self.queue = queue

    def Insert(self, db):
        queue = self.queue
        db.cursor.execute('insert into pe (id, patent_id, license_num, pub_date, pledger, pledgee, product_name) '
                          'values (%s,%s,%s,%s,%s,%s,%s);',
                          (0, db.split_patent(queue[1]), queue[4], queue[5], queue[6], queue[7], queue[8]))
        raw_data = '''专利权质押合同登记的生效
专利号:{0}
登记号:{1}
登记生效日:{2}
出质人:{3}
质权人:{4}
使用外观设计的产品名称:{5}'''.format(queue[1], queue[4], queue[5], queue[6], queue[7], queue[8])
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data,change_id, source)'
            'values (%s,%s,%s,%s,%s,%s,%s);',
            (0, 'PE01',
             queue[5],
             db.split_patent(queue[1]),
             raw_data,
             db.back()[0],
             db.filename
             ))
