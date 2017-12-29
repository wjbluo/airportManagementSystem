import math

def GetYeMa(page,limit,count):
    page = int(page)
    limit = int(limit)
    maxPage = math.ceil(count/limit)
    if int(page)<=1:
        return 1,maxPage,1,limit
    if int(page)>maxPage:
        return maxPage,maxPage,(maxPage-1)*limit+1,maxPage*limit
    return int(page),maxPage,(int(page)-1)*limit+1, int(page)*limit