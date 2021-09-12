class ContentDictionary:
    def __init__(self, title_block, text_block):
        self.text_block = text_block
        title = ""
        for x in title_block:
            title = title + x['text']
        self.title = title


class TableSpilt:
    def __init__(self, lines, pdf):
        self.lines = lines
        self.pdf = pdf

    def get_this_name(self):
        filename = ''
        for i in self.pdf.pages[0].chars:
            if i['size'] == 11.000:
                filename = filename + i['text']
        filename = filename.replace('公告日', '')
        return filename.replace(' ', '')

    def same_page_handle(self, page, line, old_line):
        middleware = []
        for j in page.chars:
            if line['y0'] < j['y0'] < old_line['y0']:
                middleware.append(j)
        return middleware

    def different_page_handle(self, pdf, line, old_line):
        middleware = []
        for j in pdf.chars:
            if j['page_number'] < old_line['page_number']:
                continue
            elif j['page_number'] == old_line[
                'page_number'] and j['y0'] < old_line['y0']:
                middleware.append(j)
            elif line['page_number'] > j['page_number'] > old_line[
                'page_number']:
                middleware.append(j)
            elif line['page_number'] == j[
                'page_number'] and line['y0'] < j['y0']:
                middleware.append(j)
            elif j['page_number'] > line['page_number']:
                break
        return middleware

    def get_word(self, line, old_line):
        pdf = self.pdf
        if line['page_number'] == old_line['page_number']:
            middleware = self.same_page_handle(
                pdf.pages[old_line['page_number'] - 1], line, old_line)
        else:
            middleware = self.different_page_handle(pdf, line, old_line)
        return middleware

    def handle(self):
        table_list = []
        for l in range(1, len(self.lines)):
            table_list.append(self.get_word(self.lines[l], self.lines[l - 1]))
        return table_list

    def return_serialized_data(self):
        block = []
        page_serialization_dictionary = []
        title_block = []
        text_block = []
        table_list = self.handle()
        for table in table_list:
            for single in table:
                if single['size'] < 8.6 and (single[
                                                 'fontname'] != 'KDZGDU+SimHei' and single[
                                                 'fontname'] != 'AKIGOT+SimHei' and single[
                                                 'fontname'] != 'SPKMZY+SimHei'):
                    text_block.append(single)
                else:
                    title_block.append(single)
            page_serialization_dictionary.append(
                ContentDictionary(title_block, text_block))
            title_block = []
            text_block = []
        return page_serialization_dictionary
