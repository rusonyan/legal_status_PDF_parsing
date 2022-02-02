import re

"""
表拆成单行数据:
    StringMiddleware.branch()  ->针对每行单数据分割
    StringMiddleware.branches()->针对每行双数据分割
"""


def is_ZL(text):
    return bool(re.search(r'ZL .*', text))


class StringMiddleware:
    def __init__(self, queue):
        string = []
        string_queue = ''
        self.queue = queue
        self.string = string

    def branch(self):
        queue = self.queue
        string = self.string
        string_queue = ''
        for x in range(len(queue)):
            if x == len(queue) - 1:
                string.append(string_queue + queue[x]['text'])
                break
            if (queue[x + 1]['x0'] - queue[x]['x0']) > 17 or (
                    queue[x + 1]['x0'] <= 44
                    and queue[x + 1]['x0'] != queue[x]['x0']):
                string_queue = string_queue + queue[x]['text']
                string.append(string_queue)
                string_queue = ""
            else:
                string_queue = string_queue + queue[x]['text']
        results = string
        patent_transfer_queue = []
        for i in range(len(results)):
            if is_ZL(results[i]):
                state = True
                for j in range(i + 1, len(results)):
                    if is_ZL(results[j]):
                        patent_transfer_queue.append(results[i - 1:j - 1])
                        state = False
                        break
                if state:
                    patent_transfer_queue.append(results[i - 1:])
        return patent_transfer_queue

    def branches(self):
        queue = self.queue
        string = self.string
        string_queue = ''
        for x in range(len(queue)):
            if x == len(queue) - 1:
                string.append(string_queue + queue[x]['text'])
                break
            if (queue[x + 1]['x0'] - queue[x]['x0']) > 17 or (
                    (queue[x + 1]['x0'] <= 44 or 280 <= queue[x + 1]['x0'] <= 307)
                    and queue[x + 1]['x0'] != queue[x]['x0']):
                string_queue = string_queue + queue[x]['text']
                string.append(string_queue)
                string_queue = ""
            else:
                string_queue = string_queue + queue[x]['text']
        results = string
        patent_transfer_queue = []
        for i in range(len(results)):
            if is_ZL(results[i]):
                state = True
                for j in range(i + 1, len(results)):
                    if is_ZL(results[j]):
                        patent_transfer_queue.append(results[i - 1:j])
                        state = False
                        break
                if state:
                    patent_transfer_queue.append(results[i - 1:])
        return patent_transfer_queue
