import re

"""
数据模型
"""


class PatentInvalidation:
    name = '专利权全部无效表'

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
            print("错误！创建专利权全部无效对象失败")

    def Insert(self, db):
        db.cursor.execute('INSERT INTO [dbo].[IW] VALUES (?,?,?,?,?)',
                          self.Main_classification, self.Patent_number,
                          self.Invalidation_decision_number,
                          self.Invalidation_decision_date, db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'IW01', '专利权的全部无效', self.Invalidation_decision_date,
            self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date


class TerminationUnpaidAnnualFee:
    name = '未缴年费终止表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"\d\d-\d\d", queue[0]))
        if state and bool(re.search(r'ZL .*', queue[1])) and bool(
                re.search('ZL \w{12}\.\w', queue[1])):
            data = queue[1].split(' ')
            self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
            self.Patent_number = data[0] + ' ' + data[1]
            self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}',
                                                data[2]))[0]
            self.Authorization_announcement_date = (re.findall(
                r'\d{4}\.\d{1,2}\.\d{1,2}', data[3]))[0]

        elif state and bool(re.search(r'ZL .*', queue[1])) and not bool(
                re.search('ZL \w{12}\.\w', queue[1])):
            data = queue[2].split(' ')
            self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
            self.Patent_number = queue[1]
            self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}',
                                                data[0]))[0]
            self.Authorization_announcement_date = (re.findall(
                r'\d{4}\.\d{1,2}\.\d{1,2}', data[1]))[0]
        else:
            print("错误！创建未缴年费终止对象失败")

    def Insert(self, db):
        db.cursor.execute('INSERT INTO [dbo].[CF] VALUES (?,?,?,?)',
                          self.Main_classification, self.Patent_number,
                          db.publishTime, db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'CF01', '未缴年费专利权终止', db.publishTime, self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Application_date + "," + self.Authorization_announcement_date


class ExpiryOfThePatentRight:
    name = '专利有效期满注销表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"\d\d-\d\d", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        if len(queue) >= 3:
            data = queue[2].split(' ')
            if state:
                self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
                self.Patent_number = queue[1]
                if len(re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}', data[0])) == 0:
                    data = queue[1].split(' ')
                    self.Patent_number = data[0] + ' ' + data[1]
                    data = data[2:]
                    self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}', data[0]))[0]
                    self.Authorization_announcement_date = (re.findall(
                        r'\d{4}\.\d{1,2}\.\d{1,2}', data[1]))[0]
                else:
                    self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}', data[0]))[0]
                    self.Authorization_announcement_date = (re.findall(
                        r'\d{4}\.\d{1,2}\.\d{1,2}', data[1]))[0]
            else:
                print("错误！创建专利有效期满对象失败")
        else:
            self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
            self.Patent_number = queue[1]
            data = queue[1].split(' ')
            self.Patent_number = data[0] + ' ' + data[1]
            data = data[2:]
            self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}', data[0]))[0]
            self.Authorization_announcement_date = (re.findall(
                r'\d{4}\.\d{1,2}\.\d{1,2}', data[1]))[0]

    def Insert(self, db):
        db.cursor.execute('INSERT INTO [dbo].[CX] VALUES (?,?,?,?,?)',
                          self.Main_classification, self.Patent_number,
                          db.publishTime, self.Authorization_announcement_date,
                          db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'CX01', '专利有效期满', db.publishTime, self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Application_date + "," + self.Authorization_announcement_date


class PatentAbandonment:
    name = '专利放弃表'

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
            print("错误！创建专利放弃对象失败")

    def Insert(self, db):
        db.cursor.execute('INSERT INTO [dbo].[AV] VALUES (?,?,?,?)',
                          self.Main_classification, self.Patent_number,
                          self.Invalidation_decision_date, db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'AV01', '专利权主动放弃', db.publishTime, self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date


class BibliographiChanges:
    name = '著录事项变更表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"(\d\d-\d\d)", queue[0]))
        if state:
            self.Main_classification = queue[0]
            self.Patent_number = queue[1]
            self.Authorization_announcement_date = queue[2]
            self.Invalidation_decision_number = queue[3]
            self.Invalidation_decision_date = queue[4]
        else:
            print("错误！创建著录事项变更对象失败")

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date
