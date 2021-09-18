import re


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
            self.Right_holder_after_address = queue[7]
            if len(queue) > 8 and queue[8] != '主分类号' and queue[8] != '专利号':
                self.Right_holder_before_change = self.Right_holder_before_change + ";" + queue[
                    8]
                if len(queue) > 9 and queue[9] != '主分类号' and queue[9] != '专利号':
                    self.Right_holder_after_change = self.Right_holder_after_change + ";" + queue[
                        9]
        else:
            print("错误！，创建专利转移对象失败")

    def Insert(self, db):
        pass

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
            self.Right_holder_after_address = queue[6]
            if len(queue) > 7 and queue[7] != '主分类号' and queue[7] != '专利号':
                self.Right_holder_before_change = self.Right_holder_before_change + ";" + queue[
                    7]
                if len(queue) > 8 and queue[8] != '主分类号' and queue[8] != '专利号':
                    self.Right_holder_after_change = self.Right_holder_after_change + ";" + queue[
                        8]
        else:
            print("错误！，创建专利更名对象失败")

    def Insert(self, db):
        db.cursor.execute(
            'INSERT INTO [dbo].[CP] VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
            self.Main_classification, self.Patent_number,
            self.Right_holder_before_change, self.Right_holder_after_change,
            self.Right_holder_before_address, self.Right_holder_after_address,
            db.publishTime, db.filename)
        db.cursor.execute(
            'INSERT INTO [dbo].[StateChange]([code],[after_change],[announcement_date],[patent_num],[change_id]) VALUES (?,?,?,?,?)',
            'IW01', '专利权的全部无效', self.Invalidation_decision_date,
            self.Patent_number,
            db.back()[0])
        return self

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Change_items + "," + self.Right_holder_before_change + "," + self.Right_holder_after_change + "," + self.Right_holder_before_address + "," + self.Right_holder_after_address