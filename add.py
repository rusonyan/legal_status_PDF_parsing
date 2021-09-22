import cpca

from win10toast import ToastNotifier

toaster = ToastNotifier()


#
# a='2010年5月26日'
# array =
#
# publishTime = time.strftime("%Y-%m-%d", time.strptime(a, u"%Y年%m月%d日"))
# print (publishTime)

# truncate table AV
# truncate table CF
# truncate table CX
# truncate table CP
# truncate table DBlog
# truncate table IW
# truncate table PD
# truncate table PP
# truncate table StateChange
# truncate table TR
def address(location):
    df = cpca.transform([location], pos_sensitive=True)
    results = df.values[0]
    state = True
    for r in results:
        if r == None:
            state = False
    if state and results[5] != -1:
        print(1)
        for x in results:
            print(x)
    else:
        print(2)
        for x in results:
            print(x)


location_str = "102100 北京市延庆县延庆镇莲花池村南"

address(location_str)

toaster.show_toast('XML法律状态解析器',
                   "已自动更新！",
                   icon_path=None,
                   duration=10, )
