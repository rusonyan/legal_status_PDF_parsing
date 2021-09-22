import CsvWrite
from StringMiddleware import StringMiddleware
from model.BaoQuan import PatentPreservation, PatentPreservationCancellation
from model.Invalid import PatentAbandonment, PatentInvalidation, TerminationUnpaidAnnualFee, ExpiryOfThePatentRight
from model.owner import PatentTransfer, PatentOwnerChanges

"""
表处理
"""


class PatentRightChangeIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        b = StringMiddleware(text_block).branch()
        for single_ling in StringMiddleware(text_block).branch():
            rows.append(PatentTransfer(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


class PatentAbandonmentIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        b = StringMiddleware(text_block).branch()
        for single_ling in StringMiddleware(text_block).branch():
            rows.append(PatentAbandonment(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


class PatentInvalidationIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        for single_ling in StringMiddleware(text_block).branch():
            rows.append(PatentInvalidation(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


# class BibliographiChangesIntermediary:
#     def __init__(self, text_block, bk_path, db):
#         rows = []
#         b = StringMiddleware(text_block).branch()
#         for single_ling in StringMiddleware(text_block).branch():
#             rows.append(BibliographiChanges(single_ling).Insert(db))
#         CsvWrite.write(rows, bk_path)


class PatentOwnerChangesIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        for single_ling in StringMiddleware(text_block).branch():
            rows.append(PatentOwnerChanges(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


class PatentPreservationIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        b = StringMiddleware(text_block).branch()

        for single_ling in StringMiddleware(text_block).branch():
            rows.append(PatentPreservation(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


class PatentPreservationCancellationIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        for single_ling in StringMiddleware(text_block).branch():
            rows.append(PatentPreservationCancellation(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


class TerminationUnpaidAnnualFeeIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        b = StringMiddleware(text_block).branchs()
        for single_ling in StringMiddleware(text_block).branchs():
            rows.append(TerminationUnpaidAnnualFee(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)


class ExpiryOfThePatentRightIntermediary:
    def __init__(self, text_block, bk_path, db):
        rows = []
        for single_ling in StringMiddleware(text_block).branchs():
            rows.append(ExpiryOfThePatentRight(single_ling).Insert(db))
        CsvWrite.write(rows, bk_path)
