import sys

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


def zeropad(arr): # np[E,CS2], np[E,CS2]
    # find longest length = max([(len(x),x) for x in ('a','b','aa')])
    maxlen,maxele = max([(len(l),l) for l in arr])
    print(maxlen,maxele)
#
#    arrS_zero = np.zeros(,dtype=float)
#    iS = 0
#    for iL in range(len(arrL)):
#        if  iS<len(arrS):
#            if arrL[iL][0] == arrS[iS][0]:
#                arrS_zero[iL] = arrS[iS]
#                iS+=1
#
#    return arrS_zero
#

plt.rcParams["font.size"] = 15
width = 0.100

if len(sys.argv) < 2:
    print("Useage: 1 for EM1.8/2.0, 2 for DNNLOgo, 3 for N3LO")
    exit(0)

inter = int(sys.argv[1])

indf = pd.DataFrame()
enbraOff = 0
enketOff = 0
title = ""
savename = ""
if inter==1:
    indf = pd.read_csv('./SF_Ca50_Ca49_fp-shell_EM1.8_2.0_magnus_Ca49_e14_E24_s500_hw16_A49.csv')
    enbraOff = 429.152647
    enketOff = 422.89922
    title = "EM1.8/2.0"
    savename = "c2s_em.pdf"
elif inter == 2:
    indf = pd.read_csv('./SF_Ca50_Ca49_fp-shell_DNNLOgo_magnus_Ca49_e14_E24_s500_hw16_A49.csv')
    enbraOff = 427.706549
    enketOff = 422.014998
    title = "DNNLOgo"
    savename = "c2s_dnnlogo.pdf"
elif inter == 3:
    indf = pd.read_csv('./SF_Ca50_Ca49_fp-shell_N3LO_LNL2_magnus_Ca49_e14_E24_s500_hw16_A49.csv')
    enbraOff = 426.26796
    enketOff = 420.360171
    title = "N3LO LNL2"
    savename = "c2s_n3lo.pdf"
else:
    print("no good interaction option")
    print("Useage: 1 for EM1.8/2.0, 2 for DNNLOgo, 3 for N3LO")
    exit(0)

# convert En bra to gs
indf['En bra'] = indf['En bra'].map(lambda x: x+enbraOff)
indf['En ket'] = indf['En ket'].map(lambda x: x+enketOff)

# combine n,l,j2 columns to be nlj2
indf['nlj2'] = indf['n'].astype(str)+indf['l'].astype(str)+indf['j2'].astype(str)
Nnlj2 = indf['nlj2'].nunique()
innp = []
nlj2lab = []
for i_nlj in indf['nlj2'].unique():
    tmpdf = indf[['En bra','CS^2']].loc[(indf['nlj2']==i_nlj)&(indf['En bra']>-0.1)&(indf['En bra']<5)&(indf['En ket']<1e-5)]
    tmpnp = tmpdf.to_numpy()
    nlj2lab.append(i_nlj)
    innp.append(tmpnp)

print(innp)
zeropad(innp)

# En ket<1e-5 for zero because getting to zero gives floating point thing
leq3 = indf.loc[(indf['j2']==3)&(indf['En bra']>-0.1)&(indf['En bra']<5)&(indf['En ket']<1e-5)]
leq1 = indf.loc[(indf['j2']==1)&(indf['En bra']>-0.1)&(indf['En bra']<5)&(indf['En ket']<1e-5)]
leq3np = leq3[['En bra','CS^2']].to_numpy()
leq1np = leq1[['En bra','CS^2']].to_numpy()

# for all, need n, l, j2
# need to find min and max of column
# initalise nparray to size of

#leq1np = zeropad(leq3np,leq1np)
#
#fix, ax = plt.subplots()
#opacity = 1
#
#ax.bar(leq3np[:,0],leq3np[:,1],width,label=r'$\nu1p_{3/2}$')
#ax.bar(leq1np[:,0],leq1np[:,1],width,bottom=leq3np[:,1],label=r'$\nu1p_{1/2}$')
#
indf.pivot_table(index='En bra',columns='nlj2',values='CS^2').plot.bar(rot=0, stacked=True,color = ['blue', 'green', 'red'])

plt.title(title)
plt.xlabel('Energy [MeV]')
plt.xlim([-0.1,5])
plt.ylabel('$C^2S$')

plt.legend()
plt.savefig(savename, bbox_inches="tight")
