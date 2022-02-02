# -*- coding: utf-8 -*-
from config import EE_RE_TEMPLATE
from special_mode.Validator import validator


class EE:
    name = '专利实施许可合同备案的生效'

    def __init__(self, queue):
        self.queue = queue
        if len(queue) != 10 or validator(queue, EE_RE_TEMPLATE):
            raise Exception("专利实施许可合同备案的生效解析错误")
        self.queue = queue

    def Insert(self, db):
        queue = self.queue
        db.cursor.execute('insert into ee values (%s,%s,%s,%s,%s,%s,%s,%s);',
                          (0, db.split_patent(queue[2]), queue[1], queue[4], queue[5], queue[6], queue[8], queue[9]))
        raw_data = '''专利实施许可合同备案的生效
专利号:{0}
合同备案号:{1}
让与人:{2}
受让人:{3}
使用外观设计的产品名称:{4}
许可种类:{5}
备案日期:{6}'''.format(queue[2], queue[1], queue[4], queue[5], queue[6], queue[8], queue[9])
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data,change_id, source)'
            'values (%s,%s,%s,%s,%s,%s,%s);',
            (0, 'EE01',
             queue[9],
             db.split_patent(queue[2]),
             raw_data,
             db.back()[0],
             db.filename
             ))
