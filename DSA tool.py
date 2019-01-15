# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 22:05:38 2019

@author: Nicolas
"""
import numpy as np
doPlot=True
try:
    import matplotlib.pyplot as plt
except:
    doPlot=False


helpString={
        'menu':'\n Menü, h: Hilfe, c: Ende',
        'help':"Hilfe: \n t: Talentwurf \n tl: ^ loop \n tw: W'keit Talentwurf zu schaffen \n twl: ^ loop \n twp: Plottet TW/TaW \n mk: Menschenk \n sn: Sinnen \n c: Ende \n h: Hilfe \n sonst: xdy",
        'initMK':'sind diese Menschenk Werte (E1 E2 E3 TaW) richtig (j/n)',
        'initSN':'sind diese Sinnensch Werte (E1 E2 E3 TaW) richtig (j/n)',
        'xdy':'konnte nicht als xdy interpretiert werden, h: Hilfe'
        }

needsInput={
        't':'E1 E2 E3 TaW+Mod opt:wdh',
        'tw':'E1 E2 E3 TaW+Mod',
        'twp':'E1 E2 E3 startTaW',
        'mk':'Erschwernis (keine: 0, >0 -> Erschwernis, <0 -> Erleichterung)',
        'sn':'Erschwernis (keine: 0, >0 -> Erschwernis, <0 -> Erleichterung)'
        }

#takes 'xdy' as string
def xdy(args):
    s=args[0]
    if 'd' not in s or len(args)>1: 
        print(args,helpString['xdy'])
        return True 
    try:
        dInd=s.find('d')
        x=int(s[:dInd])
        y=int(s[dInd+1:])
        w=np.random.randint(1,y+1, size=x)
        print(w, ' Summe=', sum(w))
    except ValueError:
        print(s,helpString['xdy'])
    return True

def T(args):
    args=[int(x) for x in args[1:]]
    wdh=1
    if len(args)==5:wdh=args[4]
    for _ in range(wdh): throw(['', args[0], args[1], args[2], args[3]], 0)
    return True

def TL(_):
    while True:
        print('E1 E2 E3 TaW+Mod opt:wdh')
        s=input()
        try:
            args=[int(x) for x in s.split()]
            wdh=1
            if len(args)==5:wdh=args[4]
            for _ in range(wdh): throw(['', args[0], args[1], args[2], args[3]], 0)
        except ValueError:
            break
    return True

#einzelner Vergleich, return: bool
def vgl(e1, e2, e3, w1, w2, w3, taw):
    if(taw<=0):
        er1=e1-w1+taw
        er2=e2-w2+taw
        er3=e3-w3+taw
        return min(er1, er2, er3)>=0
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
def TW(args):
    try:
        l=[int(x) for x in args[1:]]
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

#plottet tw gegen TaW, funktioniert nicht im normalen cmd
def TWP(args):
    E=[int(x) for x in args[1:5]]
    x=[]
    y=[]
    while True:
        x.append(E[3])
        y.append(Wkeit(E))
        if y[len(y)-1] > 0.99 : break
        E[3]=E[3]+1
    if doPlot:
        plt.scatter(x,y)
        plt.show()
    else : print([(x[i],y[i]) for i in range(len(x))])
    return True

# makes a throw for everyone in 
def useRead(index, modS):
    if txtRead[index][0]:
        try:
            mod=int(modS)
            print('Erg  Name  W1 W2 W3')
        except ValueError:
            print('Das war keine ganze Zahl, -> mod=0')
            print('Erg  Name  W1 W2 W3')
            mod=0
        for line in txtRead[index][1]:
            throw(line, mod)
    else:
        print('update the .txt')

# can be used for any talent, given a split line from the txt files
def throw(line, mod):
    p=''
    k=''
    w=np.random.randint(1,21, size=3)
    if 1 in w: k='Krit?'
    if 20 in w: p='Patzer?'
    erg=vgl(int(line[1]), int(line[2]), int(line[3]), w[0], w[1], w[2], int(line[4])-mod)
    print(f'{erg:4} {line[0]:10}',w , p, k)

def Mk(args):
    useRead(0, args[1])
    return True

def Sn(args):
    useRead(1, args[1])
    return True

def end(_): return False

def he(_):
    print(helpString['help'])
    return True

#gets a string, tries to get args from the user
def getMissingArgs(s):
    print(needsInput[s])
    args=input()
    args=args.split()
    ret=[s]
    for i in range(len(args)):
        ret.append(args[i])
    return ret
    
    
def init():
    funDict={
        't':T,
        'tl':TL,
        'tw':TW,
        'twl':TWL,
        'twp':TWP,
        'mk':Mk,
        'sn':Sn,
        'c':end,
        'h':he}
    try:
        mkData=open('MK.txt')
        mkData=mkData.readlines()
        print(helpString['initMK'])
        print(''.join(mkData))
        mkOK=input()
        if mkOK in 'jy': 
            mkOK = True
            mkData=[[y for y in x.split()] for x in mkData[0:len(mkData)]]
        else: mkOK = False
    except FileNotFoundError:
        print('\n kein MK.txt')
        input()
        mkData=[]
        mkOK=False
    
    try:
        snData=open('SN.txt')
        snData=snData.readlines()
        print(helpString['initSN'])
        print(''.join(snData))
        snOK=input()
        if snOK in 'jy': 
            snOK = True
            snData=[[y for y in x.split()] for x in snData[0:len(snData)]]
        else: snOK = False
    except FileNotFoundError:
        print('\n kein SN.txt')
        input()
        snData=[]
        snOK=False
    return funDict, [(mkOK, mkData), (snOK, snData)]

funDict, txtRead=init()
var=True
while var:
    print(helpString['menu'])
    s=input()
    args=s.split()
    if (len(args)==1 and s in needsInput):
        args=getMissingArgs(args[0])
    var=funDict.get(args[0], xdy)(args)
