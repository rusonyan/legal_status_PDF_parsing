import re


class PatentPreservation:
    name = '专利保全表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"(\d\d-\d\d)", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        if state:
            self.Main_classification = queue[0]
            self.Patent_number = queue[1]
            self.Authorization_announcement_date = queue[2]
            self.Invalidation_decision_number = queue[3]
            self.Invalidation_decision_date = re.findall(r'\d\d\d\d\.\d\d\.\d\d', queue[4])[0]
        else:
            print("错误！创建专利保全对象失败")

    def Insert(self, db):
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data, source)'
            'values (%s,%s,%s,%s,%s,%s);',
            (0, 'PP01',
             self.Invalidation_decision_date,
             db.split_patent(self.Patent_number),
             '专利权的保全\n登记生效日:' + self.Invalidation_decision_date,
             db.filename)
        )


class PatentPreservationCancellation:
    name = '专利保全解除表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"(\d\d-\d\d)", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        if state:
            self.Main_classification = queue[0]
            self.Patent_number = queue[1]
            self.Authorization_announcement_date = queue[2]
            self.Invalidation_decision_number = queue[3]
            self.Invalidation_decision_date = re.findall(r'\d\d\d\d\.\d\d\.\d\d', queue[4])[0]
        else:
            print("错误！创建专利保全解除对象失败")

    def Insert(self, db):
        db.cursor.execute(
            'insert into patent_change_log (id, code, pub_date, patent_num, raw_data, source)'
            'values (%s,%s,%s,%s,%s,%s);',
            (0, 'PD01',
             self.Invalidation_decision_date,
             db.split_patent(self.Patent_number),
             '专利权的保全\n解除日:' + self.Invalidation_decision_date,
             db.filename))
