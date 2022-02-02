from StringMiddleware import StringMiddleware
from ToNode import Spilt
from config import EE_TEMPLATE, PE_TEMPLATE, PC_TEMPLATE
from invalid_model.AV import PatentAbandonment
from invalid_model.CF import TerminationUnpaidAnnualFee
from invalid_model.CX import ExpiryOfThePatentRight
from invalid_model.IP import PatentInvalidationPart
from invalid_model.IW import PatentInvalidation
from rule_out import PRCI
from special_mode.EC import EC
from special_mode.EE import EE
from special_mode.EM import EM
from special_mode.PC import PC
from special_mode.PE import PE
from standard_model.BaoQuan import PatentPreservation, PatentPreservationCancellation
from standard_model.CB import BibliographiChanges
from standard_model.CP import PatentOwnerChanges
from standard_model.TR import PatentTransfer

"""
表处理规则
"""


class PatentRightChangeIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            if single_ling[1] in PRCI or single_ling[5] == '佛山市华龙铝业有限公司':
                continue
            else:
                PatentTransfer(single_ling).Insert(db)


class PatentAbandonmentIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            PatentAbandonment(single_ling).Insert(db)


class PatentInvalidationIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            PatentInvalidation(single_ling).Insert(db)


class PatentInvalidationPartIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            PatentInvalidationPart(single_ling).Insert(db)


class BibliographyChangesIntermediary:
    def __init__(self, text_block):
        b = StringMiddleware(text_block).branch()
        for single_ling in StringMiddleware(text_block).branch():
            BibliographiChanges(single_ling)


class PatentOwnerChangesIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            PatentOwnerChanges(single_ling).Insert(db)


class PatentPreservationIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            PatentPreservation(single_ling).Insert(db)


class PatentPreservationCancellationIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            PatentPreservationCancellation(single_ling).Insert(db)


class TerminationUnpaidAnnualFeeIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branches():
            TerminationUnpaidAnnualFee(single_ling).Insert(db)


class ExpiryOfThePatentRightIntermediary:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branches():
            ExpiryOfThePatentRight(single_ling).Insert(db)


class PILConsent:
    def __init__(self, text_block, db):
        for single_ling in Spilt(text_block, db).return_serialized_data(EE_TEMPLATE):
            EE(single_ling).Insert(db)


class PPCConsent:
    def __init__(self, text_block, db):
        for single_ling in Spilt(text_block, db).return_serialized_data(PE_TEMPLATE):
            PE(single_ling).Insert(db)


class PPCRemove:
    def __init__(self, text_block, db):
        for single_ling in Spilt(text_block, db).return_serialized_data(PC_TEMPLATE):
            PC(single_ling).Insert(db)


class PILChange:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            EM(single_ling).Insert(db)


class PILRemove:
    def __init__(self, text_block, db):
        for single_ling in StringMiddleware(text_block).branch():
            EC(single_ling).Insert(db)
