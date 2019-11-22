from itertools import groupby

lst = [1, 2, 3, 5, 6, 7, 8, 11, 12, 13, 19]  # 连续数字

fun = lambda x: x[1] - x[0]
for k, g in groupby(enumerate(lst), fun):
    l1 = [j for i, j in g]  # 连续数字的列表
    print(l1)
    if len(l1) > 1:
        scop = str(min(l1)) + '-' + str(max(l1))  # 将连续数字范围用"-"连接
    else:
        scop = l1[0]
    print("连续数字范围：{}".format(scop))