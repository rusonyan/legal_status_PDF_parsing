import re

from intermediary import PatentRightChangeIntermediary, PatentInvalidationIntermediary, PatentAbandonmentIntermediary, \
    PatentOwnerChangesIntermediary, PatentPreservationIntermediary, PatentPreservationCancellationIntermediary, \
    TerminationUnpaidAnnualFeeIntermediary, ExpiryOfThePatentRightIntermediary

"""
表识别分类
"""


def check_string(re_exp, str):
    res = re.search(re_exp, str)
    if res:
        return True
    else:
        return False


class DifferentiationModel:
    def differentiation(self, pgd, bk_path, db):
        state = ''
        check_tem = [
            "专利权的转移",
            "专利权全部无效",
            "未缴年费专利权终止",
            "专利权有效期届满",
            '专利权的主动放弃',
            '权利的恢复',
            '著录事项变更',
            '专利权人的姓名或者名称、地址的变更',
            '文件的公告送达',
            '专利实施的强制许可',
            '专利实施许可合同备案的生效',
            '专利实施许可合同备案的变更',
            '专利实施许可合同备案的注销',
            '专利权质押合同登记的生效',
            '专利权质押合同登记的变更',
            '专利权质押合同登记的注销',
            '专利权的保全',
            '专利权保全的解除',
        ]
        for c in check_tem:
            if check_string(c, pgd.title):
                state = c
        self.differentiation_handle(pgd, state, bk_path, db)

    def differentiation_handle(self, pgd, state, bk_path, db):
        title = state
        print(title + "表正在处理---<->\n")
        if check_string("专利权的转移$", title):  # 1
            PatentRightChangeIntermediary(pgd.text_block, bk_path, db)
        elif check_string("专利权全部无效$", title):  # 2
            PatentInvalidationIntermediary(pgd.text_block, bk_path, db)
        elif check_string("未缴年费专利权终止$", title):  # 3
            TerminationUnpaidAnnualFeeIntermediary(pgd.text_block, bk_path, db)
        elif check_string("专利权有效期届满$", title):  # 4
            ExpiryOfThePatentRightIntermediary(pgd.text_block, bk_path, db)
        elif check_string("专利权的主动放弃$", title):  # 5
            PatentAbandonmentIntermediary(pgd.text_block, bk_path, db)
        elif check_string("著录事项变更$", title):  # 6
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利权人的姓名或者名称、地址的变更$", title):  # 7
            PatentOwnerChangesIntermediary(pgd.text_block, bk_path, db)
        elif check_string("权利的恢复", title):  # 8
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("文件的公告送达$", title):  # 8
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利实施的强制许可$", title):  # 9
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利实施许可合同备案的生效$", title):  # 10
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利实施许可合同备案的变更$", title):  # 10
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利实施许可合同备案的注销$", title):  # 11
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利权质押合同登记的生效$", title):  # 12
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利权质押合同登记的变更$", title):  # 12
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利权质押合同登记的注销$", title):  # 12
            print("无需关注的警告：" + title + " 表暂无须解析！")
        elif check_string("专利权的保全$", title):  # 13
            PatentPreservationIntermediary(pgd.text_block, bk_path, db)
        elif check_string("专利权保全的解除$", title):  # 14
            PatentPreservationCancellationIntermediary(pgd.text_block, bk_path,
                                                       db)
        elif check_string("其他有关事项$", title):  # 15
            print("无需关注的警告：" + title + " 表暂无须解析！")
        else:
            print("致命错误,未曾定义的表头，已自动终止程序！ 新表头为：" + title)
        print("----------------------------------------------------")
