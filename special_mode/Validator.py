# -*- coding: utf-8 -*-
import re


def validator(queue, RETEMPLETE, i=0):
    try:
        while i < len(queue) or i < len(RETEMPLETE):
            if re.search(RETEMPLETE[i], queue[i]):
                return False
            i = i + 1
        return True
    except Exception:
        return False
