import re

"""
数据模型
"""


class BibliographiChanges:
    name = '著录事项变更表'

    def __init__(self, queue):
        state = False
        state = bool(re.findall(r"(\d\d-\d\d)", queue[0]))
        if state:
            self.Main_classification = queue[0]
            self.Patent_number = re.search(r'ZL [0-9a-zA-Z.\d]{10,14}', queue[1])[0]
            self.Authorization_announcement_date = queue[2]
            self.Invalidation_decision_number = queue[3]
            self.Invalidation_decision_date = queue[4]
        else:
            print("错误！创建著录事项变更对象失败")
