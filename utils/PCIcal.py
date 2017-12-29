import scipy.io as sio
import xlrd
import numpy
#from jishu import jishu
import math
import numpy
from scipy import interpolate
import scipy.io as sio
A = u'upload/StandForPCI/DV.mat'
data = sio.loadmat(A)
DV = data['DV']
B = u'upload/StandForPCI/Calibrate.mat'
data2=sio.loadmat(B)
Calibrate=data2['Calibrate']

def jishu(mylist):
    myset=set(mylist)
    A=[]
    B=[]
    C=0
    D=[]
    E=[]
    for x in myset:
        for i in range(0,len(mylist)):
            if x==mylist[i]:
                C +=1
        D.append(C)
        B.append(x)
    E.append(D[0])
    for i in range(1,len(D)):
        E.append((D[i]-D[i-1]))
    return B,E



def CDV(DV_i,Calibrate):
    DVi=sorted(DV_i,reverse=True)
    L=[]
    for x in range(0,len(DVi)):
        if DVi[x]>5:
            L.append(x)
    l=len(L)
    if l<= 1:
        maxCDV=sum(DVi)
    else:
        new_DVi=[]
        m=1+(9/25)*(100-max(DVi))
        m_=math.floor(m)+1
        if m_>1:
            new_DVi=DVi
        else:
            for i in range(0,m_ ):
                new_DVi=DVi[i]
        Q=[]
        for x in range(0,len(new_DVi)):
            if new_DVi[x]>5:
                Q.append(x)
        q=min(len(Q),8)
        CDV=numpy.zeros([q])
        for j in range(1,q+1):
            A=[]
            CDV0=sum(new_DVi)
            a=[]
            for x in Calibrate[:,0]:
                if Calibrate[int(x-1),2]==(q-j+1):
                    if Calibrate[int(x-1),2]<143:
                        a.append(x)
            cvd0=[]
            cvd1=[]
            for i in a:
                cvd0.append(Calibrate[i-1][3])
                cvd1.append(Calibrate[i-1][4])
            gg=interpolate.interp1d(cvd0,cvd1,kind='slinear')
            CDV[j - 1]=gg(CDV0)
            new_DVi[q-j]=5
       # print('CDV=',CDV)
        maxCDV=max(CDV)
       # print('maxCDV=', maxCDV)
    return maxCDV

def yangzheng(SH1,SH2,N,NN):
    # File=xlrd.open_workbook('C:\\Users\\hasee\\Desktop\\pci\\Newfile.xls')
    # table=File.sheets()[0]
    #
    # SH1=table.col_values(0)
    # SH2=table.col_values(1)
    # print(SH1,SH2) ;# 向量
    SH=numpy.zeros([15,3],numpy.int32)
    for i in range(1,len(SH1)):
        for j in range(1,16):
            if SH1[i-1]==j and SH2[i-1]=='L':
                SH[j-1][0]=SH[j-1][0]+1
            if SH1[i-1]==j and SH2[i-1]=='M':
                SH[j-1][1]=SH[j-1][1]+1
            if SH1[i-1]==j and SH2[i-1]=='H':
                SH[j-1][2]=SH[j-1][2]+1
    PCI=numpy.zeros([1,100])
    #CDV([9., 9., 8, 0., 0., 2., 3.590206, 0., 0., 0, 0.8, 0., 0., 1., 0.], Calibrate)
    for k in range(0, 100):
        new_B = numpy.zeros([15, N])
        for l in range(0, 15):
            for m in range(0, 3):
                if SH[l, m] != 0:
                    map = []
                    app = numpy.random.randint(1, N + 1, (1, SH[l, m]))
                    map.append(app)
                    Alist = map[0][0]
                    C=jishu(Alist)
                    D=numpy.zeros([1,N])    #得到一个列表D表示N个单元中每个单元发生该病害的板块数
                    for n in range(0,N):
                        for x in range(0,len(C[0])):
                            if (n+1)==C[0][x]:
                                D[0][n]=C[1][x]
                    E = numpy.divide(NN, N)
                    F = numpy.divide(D,E)    #得到一个损坏密度的矩阵F
                    for i in range(0, len(F)):
                        for j in range(0, len(F)):
                            if F[i][j] > 1:
                                F[i][j] = 1
                    a = []
                    for r in DV[:, 0]:
                        if DV[int(r-1)][1] == (l * 3 + m + 1) :
                            a.append(r)
                    md=[]
                    dv=[]
                    for i in a: #interp1d的分母不能为0
                        md.append(DV[i-1][2])
                        dv.append(DV[i-1][3])
                    g = interpolate.interp1d(md, dv,kind='slinear')
                    new_B[l, :] = g(F) + new_B[l, :]
        maxCDV = numpy.zeros([1, N])
        #print ('maxCDV=',maxCDV)
        #print ('new_B[:,0]=',new_B[:,99])
        E=CDV(new_B[:,0],Calibrate)
        #print('E=',E)
        for q in range(0,N):
            maxCDV[0,q]=CDV(new_B[:,q],Calibrate)
        PCI[0,k]=numpy.mean(100-maxCDV)
    return numpy.mean(PCI),numpy.std(PCI)/numpy.mean(PCI)

# [y,yy]=yangzheng(5,100000)#其中100为单元数量
# print('PCI均值为',y,'变异系数为',yy)
def main():
    [y, yy] = yangzheng([],[],50,1000)

if __name__=="__main__":
    main()