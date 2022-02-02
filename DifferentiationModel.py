import re

from loguru import logger

from Intermediary import PatentRightChangeIntermediary, PatentInvalidationIntermediary, PatentAbandonmentIntermediary, \
    PatentOwnerChangesIntermediary, PatentPreservationIntermediary, PatentPreservationCancellationIntermediary, \
    TerminationUnpaidAnnualFeeIntermediary, ExpiryOfThePatentRightIntermediary, PILConsent, PPCConsent, PPCRemove, \
    PILChange, PILRemove, PatentInvalidationPartIntermediary

"""
表识别分类
"""


def check_string(re_exp, str):
    res = re.search(re_exp, str)
    if res:
        return True
    else:
        return False


def differentiation_handle(pgd, state, db):
    title = state
    logger.info(title + "表即将处理---<->\n")
    if check_string("专利权的转移$", title):  # 1
        PatentRightChangeIntermediary(pgd.text_block, db)
    elif check_string("专利权全部无效$", title):  # 2
        PatentInvalidationIntermediary(pgd.text_block, db)
    elif check_string("专利权部分无效$", title):  # 2
        PatentInvalidationPartIntermediary(pgd.text_block, db)
    elif check_string("未缴年费专利权终止$", title):  # 3
        TerminationUnpaidAnnualFeeIntermediary(pgd.text_block, db)
    elif check_string("专利权有效期届满$", title):  # 4
        ExpiryOfThePatentRightIntermediary(pgd.text_block, db)
    elif check_string("专利权的主动放弃$", title):  # 5
        PatentAbandonmentIntermediary(pgd.text_block, db)
    elif check_string("著录事项变更$", title):  # 6
        logger.debug(title + " 暂不解析")
    elif check_string("专利权人的姓名或者名称、地址的变更$", title):  # 7
        PatentOwnerChangesIntermediary(pgd.text_block, db)
    elif check_string("权利的恢复", title):  # 8
        logger.debug(title + " 暂不解析")
    elif check_string("文件的公告送达$", title):  # 8
        logger.debug(title + " 暂不解析")
    elif check_string("专利实施的强制许可$", title):  # 9
        logger.debug(title + " 暂不解析")
    elif check_string("专利实施许可合同备案的生效$", title):  # 10
        PILConsent(pgd.text_block, db)
    elif check_string("专利实施许可合同备案的变更$", title):  # 10
        PILChange(pgd.text_block, db)
    elif check_string("专利实施许可合同备案的注销$", title):  # 11
        PILRemove(pgd.text_block, db)
    elif check_string("专利权质押合同登记的生效$", title):  # 12
        PPCConsent(pgd.text_block, db)
    elif check_string("专利权质押合同登记的变更$", title):  # 12
        logger.debug(title + " 暂不解析")
    elif check_string("专利权质押合同登记的注销$", title):  # 12
        PPCRemove(pgd.text_block, db)
    elif check_string("专利权的保全$", title):  # 13
        PatentPreservationIntermediary(pgd.text_block, db)
    elif check_string("专利权保全的解除$", title):  # 14
        PatentPreservationCancellationIntermediary(pgd.text_block,
                                                   db)
    elif check_string("其他有关事项$", title):  # 15
        logger.debug(title + " 暂不解析")
    else:
        logger.error("致命错误,未曾定义的表头，已自动终止程序！ 新表头为：" + title)


class DifferentiationModel:
    def differentiation(self, pgd, db):
        state = ''
        check_tem = [
            "专利权的转移",
            "专利权全部无效",
            "专利权部分无效",
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
        differentiation_handle(pgd, state, db)
