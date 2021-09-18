import time

import cpca
import re
from dateutil.parser import parse
#
# a='2010年5月26日'
# array =
#
# publishTime = time.strftime("%Y-%m-%d", time.strptime(a, u"%Y年%m月%d日"))
# print (publishTime)


# def address(location):
#     df = cpca.transform([location], pos_sensitive=True)
#     print(df)
#     results = df.values[0]
#     state = True
#     for r in results:
#         if r == None:
#             state = False
#     if state and results[5] != -1:
#         return results
#     else:
#         return None
#
#
# location_str = "201201 上海市浦东新区金桥华东路5001号金桥出口加工区（南区）龙沪路143号"
#
# address(location_str)