# -*- coding: utf-8 -*-
class EM:
    name = '专利实施许可合同备案的变更'

    def __init__(self, queue):
        self.queue = queue

    def Insert(self, db):
        queue = self.queue
        db.cursor.execute('insert into em (id, patent_id,contract, pub_date, matter, before_change, after_change)'
                          ' values (%s,%s,%s,%s,%s,%s,%s);',
                          (0, db.split_patent(queue[1]), queue[2], queue[3], queue[4], queue[5], queue[6]))
        raw_data = '''专利实施许可合同备案的变更
专利号:{0}
登记号:{1}
变更日:{2}
变更事项:{3}
变更前:{4}
变更后:{5}'''.format(queue[1], queue[2], queue[3], queue[4], queue[5], queue[6])
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data,change_id, source)'
            'values (%s,%s,%s,%s,%s,%s,%s);',
            (0, 'EM01',
             queue[3],
             db.split_patent(queue[1]),
             raw_data,
             db.back()[0],
             db.filename
             ))
