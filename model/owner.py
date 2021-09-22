import re

import cpca


def spilt_address(location):
    results = cpca.transform([location], pos_sensitive=True).values[0]
    state = True
    for r in results:
        if r == None:
            state = False
    if state and results[5] != -1:
        return results
    else:
        return []


def filter(str):
    return bool(bool(re.search(r'.*主分类号.*', str)) and bool(re.search(r'.*专利号.*', str)))


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
            if self.Right_holder_before_change == '深圳市鸣鑫实业有限公司':
                self.Right_holder_before_address = '518040 广东省深圳市福田区侨香路鸿新花园三期B座1104'
                self.Right_holder_after_address = '518052 广东省深圳市南山区北环大道9116号富华科技大厦A座8楼'
            else:
                self.Right_holder_after_address = queue[6].strip('专利权人').strip('共同专利权人')
            if len(queue) > 8 and filter(queue[8]):
                self.Right_holder_before_change = self.Right_holder_before_change + ";" + queue[
                    8]
                if len(queue) > 9 and filter(queue[9]):
                    self.Right_holder_after_change = self.Right_holder_after_change + ";" + queue[
                        9]
        else:
            print("错误！，创建专利转移对象失败")

    def Insert(self, db):
        address = spilt_address(self.Right_holder_after_address)
        if len(address) == 8:
            db.cursor.execute(
                'INSERT INTO [dbo].[TR] VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                self.Main_classification, self.Patent_number,
                self.Right_holder_before_change,
                self.Right_holder_after_change,
                self.Right_holder_before_address,
                self.Right_holder_after_address, self.Registration_effective_date,
                db.filename, address[0], address[1],
                address[2], address[3], )
        else:
            db.cursor.execute(
                'INSERT INTO [dbo].[TR] VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                self.Main_classification, self.Patent_number,
                self.Right_holder_before_change,
                self.Right_holder_after_change,
                self.Right_holder_before_address,
                self.Right_holder_after_address, self.Registration_effective_date, db.filename, 'null', 'null', 'null',
                'null')
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[before_change],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?,?)',
            'TR01', self.Right_holder_before_change + '\n' +
                    self.Right_holder_before_address, self.Right_holder_after_change +
                    '\n' + self.Right_holder_after_address,
            self.Registration_effective_date, self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Change_items + "," + self.Right_holder_before_change + "," + self.Right_holder_after_change + "," + self.Registration_effective_date + "," + self.Right_holder_before_address + "," + self.Right_holder_after_address


class PatentOwnerChanges:
    name = '专利人姓名或地址变更表'

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
            self.Right_holder_after_change = queue[4][0:-2]
            self.Right_holder_before_address = queue[5]
            if self.Right_holder_before_change == '彭建峰':
                self.Right_holder_before_address = '222003 江苏省连云港市新浦区盐河北路168号中房新天地A1楼2单元601'
                self.Right_holder_after_address = '713305 陕西省咸阳市乾县漠西乡四里坊村一组'
            else:
                self.Right_holder_after_address = queue[6].strip('专利权人').strip('共同专利权人')
            if len(queue) > 7 and filter(queue[7]):
                self.Right_holder_before_change = self.Right_holder_before_change + ";" + queue[
                    7]
                if len(queue) > 8 and filter(queue[8]):
                    self.Right_holder_after_change = self.Right_holder_after_change + ";" + queue[
                        8]
        else:
            print("错误！，创建专利更名对象失败")

    def Insert(self, db):
        address = spilt_address(self.Right_holder_after_address)
        if len(address) == 8:
            db.cursor.execute(
                'INSERT INTO [dbo].[CP] VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                self.Main_classification, self.Patent_number,
                self.Right_holder_before_change,
                self.Right_holder_after_change,
                self.Right_holder_before_address,
                self.Right_holder_after_address, db.publishTime, db.filename, address[0], address[1],
                address[2], address[3], )
        else:
            db.cursor.execute(
                'INSERT INTO [dbo].[CP] VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                self.Main_classification, self.Patent_number,
                self.Right_holder_before_change,
                self.Right_holder_after_change,
                self.Right_holder_before_address,
                self.Right_holder_after_address, db.publishTime, db.filename, 'null', 'null', 'null',
                'null')
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[before_change],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?,?)',
            'CP01', self.Right_holder_before_change + '\n' +
                    self.Right_holder_before_address, self.Right_holder_after_change +
                    '\n' + self.Right_holder_after_address, db.publishTime,
            self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Change_items + "," + self.Right_holder_before_change + "," + self.Right_holder_after_change + "," + self.Right_holder_before_address + "," + self.Right_holder_after_address