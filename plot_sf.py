import sys

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
import pandas as pd


def zeropad(arr1, arr2): # np[E,CS2], np[E,CS2]
    # start with assumption arr1 is shortest
    arrS = arr2
    arrL = arr1
    # if not, swap them
    if len(arr1)<len(arr2):
        arrL = arr2
        arrS = arr1

    arrS_zero = np.zeros(arrL.shape,dtype=float)
    iS = 0
    for iL in range(len(arrL)):
        if  iS<len(arrS):
            if arrL[iL][0] == arrS[iS][0]:
                arrS_zero[iL] = arrS[iS]
                iS+=1

    return arrS_zero


plt.rcParams["font.size"] = 15
width = 0.100

if len(sys.argv) < 2:
    print("Useage: 1 for EM1.8/2.0, 2 for DNNLOgo, 3 for N3LO")
    exit(0)

inter = int(sys.argv[1])

indat = pd.DataFrame()
enbraOff = 0
enketOff = 0
title = ""
savename = ""
if inter==1:
    indat = pd.read_csv('./SF_Ca50_Ca49_fp-shell_EM1.8_2.0_magnus_Ca49_e14_E24_s500_hw16_A49.csv')
    enbraOff = 429.152647
    enketOff = 422.89922
    title = "EM1.8/2.0"
    savename = "c2s_em.pdf"
elif inter == 2:
    indat = pd.read_csv('./SF_Ca50_Ca49_fp-shell_DNNLOgo_magnus_Ca49_e14_E24_s500_hw16_A49.csv')
    enbraOff = 427.706549
    enketOff = 422.014998
    title = "DNNLOgo"
    savename = "c2s_dnnlogo.pdf"
elif inter == 3:
    indat = pd.read_csv('./SF_Ca50_Ca49_fp-shell_N3LO_LNL2_magnus_Ca49_e14_E24_s500_hw16_A49.csv')
    enbraOff = 426.26796
    enketOff = 420.360171
    title = "N3LO LNL2"
    savename = "c2s_n3lo.pdf"
else:
    print("no good interaction option")
    print("Useage: 1 for EM1.8/2.0, 2 for DNNLOgo, 3 for N3LO")
    exit(0)

# convert En bra to gs
indat['En bra'] = indat['En bra'].map(lambda x: x+enbraOff)
indat['En ket'] = indat['En ket'].map(lambda x: x+enketOff)

# En ket<1e-5 for zero because getting to zero gives floating point thing
leq3 = indat.loc[(indat['j2']==3)&(indat['En bra']>-0.1)&(indat['En bra']<5)&(indat['En ket']<1e-5)]
leq1 = indat.loc[(indat['j2']==1)&(indat['En bra']>-0.1)&(indat['En bra']<5)&(indat['En ket']<1e-5)]

leq3np = leq3[['En bra','CS^2']].to_numpy()
leq1np = leq1[['En bra','CS^2']].to_numpy()

leq1np = zeropad(leq3np,leq1np)

fix, ax = plt.subplots()
opacity = 1

ax.bar(leq3np[:,0],leq3np[:,1],width,label=r'$\nu1p_{3/2}$')
ax.bar(leq1np[:,0],leq1np[:,1],width,bottom=leq3np[:,1],label=r'$\nu1p_{1/2}$')

plt.text(0.1,1.75,'$0^+_1$')
plt.text(1.3,1.75,'$2^+_1$')
plt.text(2.5,0.90,'$1^+_1$')
plt.text(3.2,1.00,'$2^+_2$')
plt.text(4.0,0.05,'$2^+_3$')
plt.text(4.7,0.05,'$3^+_1$')

plt.title(title)
plt.xlabel('Energy [MeV]')
plt.ylabel('$C^2S$')

plt.legend()
plt.savefig(savename, bbox_inches="tight")
