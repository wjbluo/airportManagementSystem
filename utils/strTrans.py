
def transforDiseaseType(num):
    str = '默认'
    if int(num) == 1:
        str = '纵向、横向和斜向裂缝'
    if int(num) == 2:
        str = '角隅断裂'
    if int(num) == 3:
        str = '破碎板或交叉裂缝'
    if int(num) == 4:
        str = '沉陷或错台'
    if int(num) == 5:
        str = '胀裂'
    if int(num) == 6:
        str = '嵌缝料损坏'
    if int(num) == 7:
        str = '接缝破碎'
    if int(num) == 8:
        str = '唧泥和板底脱空'
    if int(num) == 9:
        str = '耐久性裂缝'
    if int(num) == 10:
        str = '收缩裂缝'
    if int(num) == 11:
        str = '坑洞'
    if int(num) == 12:
        str = '起皮、龟裂和细微裂纹'
    if int(num) == 13:
        str = '板角剥落'
    if int(num) == 14:
        str = '小补丁'
    if int(num) == 15:
        str = '大补丁和开挖补块'
    return str