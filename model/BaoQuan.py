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
            self.Invalidation_decision_date = queue[4]
        else:
            print("错误！创建专利保全对象失败")

    def Insert(self, db):
        db.cursor.execute('INSERT INTO [dbo].[PP] VALUES (?,?,?,?)',
                          self.Main_classification, self.Patent_number,
                          self.Invalidation_decision_date, db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'PP01', '专利权的保全', self.Invalidation_decision_date,
            self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date


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
            self.Invalidation_decision_date = queue[4]
        else:
            print("错误！创建专利保全解除对象失败")

    def Insert(self, db):
        db.cursor.execute('INSERT INTO [dbo].[PD] VALUES (?,?,?,?)',
                          self.Main_classification, self.Patent_number,
                          self.Invalidation_decision_date, db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'PD01', '专利权的保全的解除', self.Invalidation_decision_date,
            self.Patent_number,
            db.back()[0])

        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date