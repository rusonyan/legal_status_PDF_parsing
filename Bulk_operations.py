# -*- coding: utf-8 -*-
import os

from loguru import logger

from App import App

'''
批量处理PDF
'''


def scan_pdf(path):
    if path.endswith('.pdf'):
        return True
    return False


def get_files(old_dir, Files):
    if os.path.isfile(old_dir):
        Files.append(old_dir)
    elif os.path.isdir(old_dir):
        for s in os.listdir(old_dir):
            newDir = os.path.join(old_dir, s)
            get_files(newDir, Files)
    return Files


def bulk_operations(path):
    for f in get_files(path, []):
        if scan_pdf(f):
            logger.info(f)
            App(f)


if __name__ == '__main__':
    bulk_operations(r'C:\Users\ruson\Desktop\事务数据\TEST')
