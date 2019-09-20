from pyecharts import Line, Grid
from xinshengdata import query_data
import json, decimal
from pyecharts.echarts import option as opts


all_data = query_data.query_open_live()
cs_data = query_data.query_open_live('池珊')
xw_data = query_data.query_open_live('希文')
bb_data = query_data.query_open_live('北北')
zsq_data = query_data.query_open_live('张思强')
lch_data = query_data.query_open_live('李春煌')

'''开播主播可视化'''
# all
times = []
peoples = []
for i in all_data:
    times.append(i[0])
    peoples.append(i[1])

line1 = Line("开播主播趋势图")
line1.add("开播主播", times, peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='30%')


# 池珊组
cs_times = []
cs_peoples = []
for i in cs_data:
    cs_times.append(i[0])
    cs_peoples.append(i[1])

# 希文组
xw_times = []
xw_peoples = []
for i in xw_data:
    xw_times.append(i[0])
    xw_peoples.append(i[1])

# 北北组
bb_times = []
bb_peoples = []
for i in bb_data:
    bb_times.append(i[0])
    bb_peoples.append(i[1])

# 张思强组
zsq_times = []
zsq_peoples = []
for i in zsq_data:
    zsq_times.append(i[0])
    zsq_peoples.append(i[1])

line_open = Line("各部门开播主播趋势图", title_pos='50%')
line_open.add("池珊组", cs_times, cs_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')
line_open.add("希文组", xw_times, xw_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')
line_open.add("北北组", bb_times, bb_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')
line_open.add("张思强组", zsq_times, zsq_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')


all_data = query_data.query_sound_wave()
cs_data = query_data.query_sound_wave('池珊')
xw_data = query_data.query_sound_wave('希文')
bb_data = query_data.query_sound_wave('北北')
zsq_data = query_data.query_sound_wave('张思强')
# lch_data = query_data.query_sound_wave('李春煌')

'''主播音浪可视化'''


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)



# all
times = []
peoples = []
for i in all_data:
    times.append(i[0])
    j = json.dumps(i[1], cls=DecimalEncoder)
    peoples.append(j)
print(peoples)
line2 = Line("音浪趋势图")
line2.add("音浪", times, peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='30%')


# 池珊组
cs_times = []
cs_peoples = []
for i in cs_data:
    cs_times.append(i[0])
    j = json.dumps(i[1], cls=DecimalEncoder)
    cs_peoples.append(j)

# 希文组
xw_times = []
xw_peoples = []
for i in xw_data:
    xw_times.append(i[0])
    j = json.dumps(i[1], cls=DecimalEncoder)
    xw_peoples.append(j)

# 北北组
bb_times = []
bb_peoples = []
for i in bb_data:
    bb_times.append(i[0])
    j = json.dumps(i[1], cls=DecimalEncoder)
    bb_peoples.append(j)

# 张思强组
zsq_times = []
zsq_peoples = []
for i in zsq_data:
    zsq_times.append(i[0])
    j = json.dumps(i[1], cls=DecimalEncoder)
    zsq_peoples.append(j)

line_sound = Line("各部门开播主播趋势图", title_pos='50%')
line_sound.add("池珊组", cs_times, cs_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')
line_sound.add("希文组", xw_times, xw_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')
line_sound.add("北北组", bb_times, bb_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')
line_sound.add("张思强组", zsq_times, zsq_peoples, mark_point=["max, min"], mark_line=['average'], legend_pos='70%')




grid = Grid(height=720, width=1500)
grid.add(line1, grid_top='60%', grid_right='60%')
grid.add(line_open, grid_top='60%', grid_left='60%')
grid.add(line2, grid_bottom='60%', grid_right='60%')
grid.add(line_sound, grid_bottom='60%', grid_left='60%')


grid.render('line01.html')