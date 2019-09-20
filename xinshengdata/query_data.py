from xinshengdata import connect_sql



# 创建连接mysql的实例化
create_query =  connect_sql.Create_Query()

def query_open_live(name=None):
    '''查询开播'''
    if name:
        sql = "SELECT a.`日期`, COUNT(a.`﻿原抖音号`) as anchor from livedata as a join enteranchor_list as b on a.`﻿原抖音号` = b.`原抖音号` where DATE(a.`日期`) >= '2019-9-1' AND DATE(a.`日期`) <= '2019-9-17'and a.`是否开播` = '开播' and b.`经纪人` = '%s' GROUP BY a.`日期` ORDER BY a.`日期`" % name
        data = create_query.my_qurey(sql)
        return data
    else:
        sql = "SELECT a.`日期`, COUNT(a.`﻿原抖音号`) as anchor from livedata as a join enteranchor_list as b on a.`﻿原抖音号` = b.`原抖音号` where DATE(a.`日期`) >= '2019-9-1' AND DATE(a.`日期`) <= '2019-9-17'and a.`是否开播` = '开播' GROUP BY a.`日期` ORDER BY a.`日期`"
        data = create_query.my_qurey(sql)
        return data

def query_new_anchor(name=None):
    '''查询新签约主播'''
    if name:
        sql = '''SELECT DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d') as '签约时间', COUNT(DISTINCT(b.`原抖音号`)) as '入驻主播' from livedata as a join enteranchor_list as b on a.`﻿原抖音号` = b.`原抖音号` where DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d') <= '2019-9-17' and b.`经纪人` = '%s' GROUP BY DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d') ORDER BY DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d')''' % name
        data = create_query.my_qurey(sql)
        return data
    else:
        sql = '''SELECT DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d') as '签约时间', COUNT(DISTINCT(b.`原抖音号`)) as '入驻主播' from livedata as a join enteranchor_list as b on a.`﻿原抖音号` = b.`原抖音号` where DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d') <= '2019-9-17' GROUP BY DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d') ORDER BY DATE_FORMAT(b.`签约时间`,'%%y-%%m-%%d')'''
        data = create_query.my_qurey(sql)
        return data

def query_sound_wave(name=None):
    '''查询音浪'''
    if name:
        sql = "SELECT a.`日期`, sum(a.`音浪 - 总计`) from livedata as a join enteranchor_list as b on a.`﻿原抖音号` = b.`原抖音号` where DATE(a.`日期`) >= '2019-9-1' and DATE(a.`日期`) <= '2019-9-17'and a.`是否开播` = '开播' and b.`经纪人` = '%s' GROUP BY a.`日期` ORDER BY a.`日期`" % name
        data = create_query.my_qurey(sql)
        return data
    else:
        sql = "SELECT a.`日期`, sum(a.`音浪 - 总计`) from livedata as a join enteranchor_list as b on a.`﻿原抖音号` = b.`原抖音号` WHERE DATE(a.`日期`) >= '2019-9-1' and DATE(a.`日期`) <= '2019-9-17'and a.`是否开播` = '开播' GROUP BY a.`日期` ORDER BY a.`日期`"
        data = create_query.my_qurey(sql)
        return data



if __name__ == '__main__':
    query_sound_wave('池珊')
