import re

"""
数据模型
"""


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

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Change_items + "," + self.Right_holder_before_change + "," + self.Right_holder_after_change + "," + self.Right_holder_before_address + "," + self.Right_holder_after_address


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

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date


class TerminationUnpaidAnnualFee:
    name = '未缴年费终止表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"\d\d-\d\d", queue[0]))
        if state and bool(re.search(r'ZL .*', queue[1])) and bool(re.search('ZL \w{12}\.\w', queue[1])):
            data = queue[1].split(' ')
            self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
            self.Patent_number = data[0] + ' ' + data[1]
            self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}',
                                                data[2]))[0]
            self.Authorization_announcement_date = (re.findall(
                r'\d{4}\.\d{1,2}\.\d{1,2}', data[3]))[0]

        elif state and bool(re.search(r'ZL .*', queue[1])) and not bool(re.search('ZL \w{12}\.\w', queue[1])):
            data = queue[2].split(' ')
            self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
            self.Patent_number = queue[1]
            self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}',
                                                data[0]))[0]
            self.Authorization_announcement_date = (re.findall(
                r'\d{4}\.\d{1,2}\.\d{1,2}', data[1]))[0]
        else:
            print("错误！创建未缴年费终止对象失败")

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Application_date + "," + self.Authorization_announcement_date


class ExpiryOfThePatentRight:
    name = '专利有效期满注销表'

    def __init__(self, queue):
        state = False
        state = bool(re.search(r"\d\d-\d\d", queue[0]))
        state = bool(re.search(r'ZL .*', queue[1]))
        data = queue[2].split(' ')
        if state:
            self.Main_classification = (re.findall(r'\d\d-\d\d', queue[0]))[0]
            self.Patent_number = queue[1]
            self.Application_date = (re.findall(r'\d{4}\.\d{1,2}\.\d{1,2}',
                                                data[0]))[0]
            self.Authorization_announcement_date = (re.findall(
                r'\d{4}\.\d{1,2}\.\d{1,2}', data[1]))[0]
        else:
            print("错误！创建专利有效期满对象失败")

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

    def __str__(self):
        return self.Main_classification + "," + self.Patent_number + "," + self.Authorization_announcement_date + "," + self.Invalidation_decision_number + "," + self.Invalidation_decision_date
