# -*- coding: utf-8 -*-
import re

'''
专利实施许可合同备案的生效 
专利权质押合同登记的生效 
专利权质押合同登记的注销 
专用表的切段
'''


def delete(dg):
    for i in dg:
        if re.search(i, dg):
            return True
    return False


def same_page_handle(node_group, page_hi, page_end_num_hi):
    return list(filter(lambda x: page_end_num_hi <= x['y0'] <= page_hi, node_group))


def different_page_handle(node_group, page_hi, page_end_num_hi, page_num, page_end_num):
    middleware = []
    for x in node_group:
        for y in x.chars:
            if page_num < y['page_number'] < page_end_num:
                middleware.append(y)
            elif y['page_number'] == page_num and y['y0'] <= page_hi:
                middleware.append(y)
            elif y['page_number'] == page_end_num and y['y0'] >= page_end_num_hi:
                middleware.append(y)
            else:
                pass
    return middleware


def block_spilt(temp, i=1):
    text_group = []
    short_text = temp[0]['text']
    while i < len(temp):
        if temp[i]['fontname'] == temp[i - 1]['fontname']:
            short_text = short_text + temp[i]['text']
        else:
            text_group.append(short_text)
            short_text = ''
            short_text = short_text + temp[i]['text']
        i = i + 1
    text_group.append(short_text)
    return text_group


class Spilt:
    def __init__(self, text_block, db):
        self.pdf = db.pdf
        page_num = None
        page_hi = None
        for tb in text_block:
            if tb['text'] == '主' and 7.9 < tb['size'] < 8.1:
                page_num = tb['page_number']
                page_hi = tb['y0']
                break
        page_end_num_hi = 100000.0
        for tt in text_block:
            if tt['page_number'] == text_block[-1]['page_number'] and tt['y0'] < page_end_num_hi:
                page_end_num_hi = tt['y0']
        page_end_num_hi = page_end_num_hi - 16
        self.text_group = self.handle(page_num, page_hi, text_block[-1]['page_number'], page_end_num_hi)

    def handle(self, page_num, page_hi, page_end_num, page_end_num_hi):
        if page_num == page_end_num:
            node = same_page_handle(self.pdf.pages[page_num - 1].chars, page_hi, page_end_num_hi)
        else:
            node = different_page_handle(self.pdf.pages[page_num - 1:page_end_num], page_hi, page_end_num_hi,
                                         page_num,
                                         page_end_num)
        text_group = block_spilt(
            list(filter(lambda x: x['size'] <= 9.1 and (x['text'] == '-' or x['size'] != 8.5), node)))
        return text_group

    def return_serialized_data(self, template, i=0, j=0, text_temp=''):
        group = []
        text_block = []
        while i < len(self.text_group):
            if re.search('----', self.text_group[i]):
                text_block.append(text_temp.strip())
                text_temp = ''
                group.append(text_block)
                text_block = []
                j = 0
            elif re.search(template[j], self.text_group[i]):
                if j != 0:
                    text_block.append(text_temp.strip())
                    text_temp = ''
                j = j + 1
            else:
                text_temp = text_temp + self.text_group[i]
            i = i + 1
        return group
