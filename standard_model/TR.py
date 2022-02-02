import re

from rule_out import TR_chart


def filter(str):
    return not bool(bool(re.search(r'.*主分类号.*', str)) or bool(re.search(r'.*专利号.*', str) or str is '·'))


class PatentTransfer:
    name = "专利权变更表"

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"(\d\d-\d\d)", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        state = bool(queue[2] == "专利权人")
        if state:
            self.Main_classification = queue[0]
            self.Patent_number = queue[1]
            self.Change_items = queue[2]
            self.Right_holder_before_change = queue[3]
            self.Right_holder_after_change = queue[4]
            self.Registration_effective_date = queue[5][0:-2]
            self.Right_holder_before_address = queue[6]
            self.before_co_patent_holder = None
            self.after_co_patent_holder = None
            if self.Patent_number in TR_chart:
                self.Right_holder_before_change = TR_chart[self.Patent_number][0]
                self.Right_holder_after_change = TR_chart[self.Patent_number][1]
                self.Right_holder_before_address = TR_chart[self.Patent_number][2]
                self.Right_holder_after_address = TR_chart[self.Patent_number][3]
                self.Registration_effective_date = TR_chart[self.Patent_number][4]
            else:
                self.Right_holder_after_address = queue[6].strip('专利权人').strip('共同专利权人')
            if len(queue) > 8 and filter(queue[8]):
                self.before_co_patent_holder = queue[8]
                if len(queue) > 9 and filter(queue[9]):
                    self.after_co_patent_holder = queue[9]

        else:
            print("错误！，创建专利转移对象失败")

    def Insert(self, db):
        address = db.spilt_address(self.Right_holder_after_address)
        if address[4] is not None:
            abcode = int(address[4])
        else:
            abcode = None
        db.cursor.execute(
            'insert into tr '
            'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',
            (0, db.split_patent(self.Patent_number),
             self.Right_holder_before_change,
             self.before_co_patent_holder,
             self.Right_holder_after_change,
             self.after_co_patent_holder,
             self.Right_holder_before_address,
             self.Right_holder_after_address,
             self.Registration_effective_date,
             db.filename,
             abcode,
             address[0],
             address[1],
             address[2],
             address[3],
             ))
        if self.before_co_patent_holder is not None:
            self.Right_holder_before_change = self.Right_holder_before_change + ';' + self.before_co_patent_holder
        if self.after_co_patent_holder is not None:
            self.Right_holder_after_change = self.Right_holder_after_change + ';' + self.after_co_patent_holder
        raw_data = '''专利权的转移
登记生效日:{4}
变更事项:专利权人
变更前权利人:{0}
变更后权利人:{1}
变更事项:地址
变更前权利人:{2}
变更后权利人:{3}'''.format(self.Right_holder_before_change,
                     self.Right_holder_after_change,
                     self.Right_holder_before_address,
                     self.Right_holder_after_address,
                     db.publishTime)
        db.cursor.execute(
            'insert into patent_change_log (id, code, before_change, '
            'after_change, pub_date, patent_num, raw_data,change_id, source)'
            'values (%s,%s,%s,%s,%s,%s,%s,%s,%s);',
            (0, 'TR01',
             self.Right_holder_before_change + '\n' + self.Right_holder_before_address,
             self.Right_holder_after_change + '\n' + self.Right_holder_after_address,
             self.Registration_effective_date,
             db.split_patent(self.Patent_number),
             raw_data,
             db.back()[0],
             db.filename
             ))
