# -*- coding: utf-8 -*-
from rule_out import EC_chart


class EC:
    name = '专利实施许可合同备案的注销'

    def __init__(self, queue):
        self.queue = queue
        if queue[2] in EC_chart:
            queue[3] = EC_chart[queue[2]][0]
            queue[4] = (EC_chart[queue[2]][1])
            if len(queue) > 5:
                queue[5] = EC_chart[queue[2]][2]
            else:
                queue.append(EC_chart[queue[2]][2])
        if len(queue) < 6:
            raise Exception("专利实施许可合同备案的注销错误")

    def Insert(self, db):
        queue = self.queue
        db.cursor.execute('insert into ec (id, patent_id, contract, giver, assignee, pub_date)'
                          ' values (%s,%s,%s,%s,%s,%s);',
                          (0, db.split_patent(queue[1]), queue[2], queue[3], queue[4], queue[5]))
        raw_data = '''专利实施许可合同备案的注销
专利号:{0}
合同备案号:{1}
让与人:{2}
受让人:{3}
解除日:{4}'''.format(queue[1], queue[2], queue[3], queue[4], queue[5])
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data,change_id, source)'
            'values (%s,%s,%s,%s,%s,%s,%s);',
            (0, 'EC01',
             queue[5],
             db.split_patent(queue[1]),
             raw_data,
             db.back()[0],
             db.filename
             ))
