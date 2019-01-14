# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 22:05:38 2019

@author: Nicolas
"""
import numpy as np

#takes 'xdy' as string
def xdy(s):
    try:
        dInd=s.find('d')
        x=int(s[:dInd])
        y=int(s[dInd+1:])
        w=np.random.randint(1,y+1, size=x)
        print(w, ' Summe=', sum(w))
    except ValueError:
        print(s,' konnte nicht als xdy interpretiert werden, h: Hilfe')
    return True

def maxErsch(E, W, taw):
    if taw<0:
        diff=[E[i]-W[i]+taw for i in range(len(E))]
        if min(diff)>=0: return min(diff)
        else: return np.inf #todo
    else:
        diff=[E[i]-W[i] for i in range(len(E))]
        if min(diff)>=0: return min(diff)+taw
        else:
            diff=[min(0,diff[i]) for i in range(len(diff))]
            return sum(diff)+taw

#einzelner Vergleich, return: bool
def vgl(e1, e2, e3, w1, w2, w3, taw):
    if(taw<=0):
        er1=e1-w1
        er2=e2-w2
        er3=e3-w3
        return (min(er1, er2, er3)+taw)>=0
    ag1=max(0,w1-e1)
    ag2=max(0,w2-e2)
    ag3=max(0,w3-e3)
    return (ag1+ag2+ag3)<=taw

#Eigenschaften 1 2 und 3, Taw+Erleichterung-Erschwernis
#Krit/Patzer werden nicht berücksichtigt
def Wkeit(l):
    [e1, e2, e3, TaW]=l
    count=0
    for x in range(1,21):
        for y in range(1,21):
            for z in range(1,21):
                count=count+vgl(e1,e2,e3,x, y, z,TaW)
    return count/(20**3)

#Talent W'keit ohne loop
def TW(_):
    print('E1 E2 E3 TaW+Mod')
    s=input()
    try:
        l=[int(x) for x in s.split()]
        print(Wkeit(l), '\n')
    except ValueError:
        return True
    return True

#Talent W'keit mit loop
def TWL(_):
    while True:
        print('E1 E2 E3 TaW+Mod')
        s=input()
        try:
            l=[int(x) for x in s.split()]
            print(Wkeit(l), '\n')
        except ValueError:
            break
    return True

# makes a throw for everyone in 
def useRead(index):
    if txtRead[index][0]:
        print('Erschwernis (keine: 0, >0 -> Erschwernis, <0 -> Erleichterung)')
        try:
            mod=int(input())
            print('Name geschafft? W1 W2 W3')
        except ValueError:
            print('Das war keine ganze Zahl')
        for line in txtRead[index][1]:
            throw(line, mod)
    else:
        print('update the .txt')

# can be used for any talent, given a split line from the txt files
def throw(line, mod=0):
    p=''
    k=''
    w=np.random.randint(1,21, size=3)
    if 1 in w: k='Krit?'
    if 20 in w: p='Patzer?'
    erg=vgl(int(line[1]), int(line[2]), int(line[3]), w[0], w[1], w[2], int(line[4])-mod)
    print(line[0], erg, w, p, k)

def Mk(_):
    useRead(0)
    return True

def Sn(_):
    useRead(1)
    return True

def end(_): return False

def he(_):
    print("Hilfe: \n t: Talentwurf \tl: ^ wiederholt \n tw: W'keit Talentwurf zu schaffen \n twl: ^ wiederholt \n Mk: Menschenk \n Sn: Sinnen \n c: Ende \n h: Hilfe \n sonst: xdy")
    return True

def default(s):
    xdy(s)
    return True

def init():
    funDict={
#        't':T,
#        'tl':TL,
        'tw':TW,
        'twl':TWL,
        'Mk':Mk,
        'Sn':Sn,
        'c':end,
        'h':he}
    
    try:
        mkData=open('MK.txt')
        mkData=mkData.readlines()
        print('sind diese Menschenk Werte (E1 E2 E3 TaW) richtig (j/n)')
        print(''.join(mkData))
        mkOK=input()
        if mkOK in 'jy': 
            mkOK = True
            mkData=[[y for y in x.split(' ')] for x in mkData[0:len(mkData)]]
        else: mkOK = False
    except FileNotFoundError:
        print('\n kein MK.txt')
        input()
        mkData=[]
        mkOK=False
    
    try:
        snData=open('SN.txt')
        snData=snData.readlines()
        print('sind diese Sinnensch Werte (E1 E2 E3 TaW) richtig (j/n)')
        print(''.join(snData))
        snOK=input()
        if snOK in 'jy': 
            snOK = True
            snData=[[y for y in x.split(' ')] for x in snData[0:len(snData)]]
        else: snOK = False
    except FileNotFoundError:
        print('\n kein SN.txt')
        input()
        snData=[]
        snOK=False
    return funDict, [(mkOK, mkData), (snOK, snData)]

(funDict, txtRead)=init()
sinnenData=None
var=True
while var:
    print('\n','Menü, h: Hilfe, c: Ende')
    s=input()
    var=funDict.get(s, default)(s)