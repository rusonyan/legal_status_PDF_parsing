import csv
import os

"""
数据写表
"""


def instance_tranfer_list(type):
    spilt = []
    for x in type:
        spilt.append(x.__str__().split(','))
    # pprint.pprint(spilt)
    return spilt


def write(rows, bk_path):
    if len(rows) > 0:
        csv_name = os.path.join(os.path.expanduser("~"),
                                'Desktop') + '\\' + bk_path + "\\" + type(
            rows[0]).name + ".csv"

        with open(csv_name, 'a', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            b = instance_tranfer_list(rows)
            f_csv.writerows(b)

        print("此表内容已经成功输出至-->" + csv_name + ' 共计' + str(len(rows)) + '条数据')
    else:
        print("此表为空")
