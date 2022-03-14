import sys

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


def zeropad(arr):
    # Get list of unique energies
    e_list = []
    for i in arr:
        for j in i:
            e_list.append(j[0])

    e_list = sorted(set(e_list))
    arr_zero = np.zeros([len(arr),len(e_list),2],dtype=float)

    i_arr = 0
    for i in arr_zero:
        for e in range(len(e_list)):
            i[e][0] = e_list[e]
            tmparr = np.array(arr[i_arr])
            tmp = np.where(tmparr[:,] == e_list[e])
            tmplist = []
            if tmp[1]!=1:
                tmplist = list(tmparr[tmp[0]][tmp[1]])
            if len(tmplist)>0:
                i[e][1] = tmplist[0][1]
        i_arr = i_arr + 1

    return arr_zero

def label(inlab): # 3digit string [nlj2]
    # orbital angular momentum
    l = 'X'
    if inlab[1] == '0':
        l = 's'
    elif inlab[1] == '1':
        l = 'p'
    elif inlab[1] == '2':
        l = 'd'
    elif inlab[1] == '3':
        l = 'f'
    elif inlab[1] == '4':
        l = 'g'
    elif inlab[1] == '5':
        l = 'h'
    elif inlab[1] == '6':
        l = 'i'

    return '$\\nu'+inlab[0]+l+'_{'+inlab[2]+'/2}$'

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
indf.loc[indf['En ket']<1e-5,'En ket'] = 0 # because of floating point shenanigans
indf.loc[indf['En bra']<1e-5,'En bra'] = 0 # because of floating point shenanigans

# combine n,l,j2 columns to be nlj2
indf['nlj2'] = indf['n'].astype(str)+indf['l'].astype(str)+indf['j2'].astype(str)
Nnlj2 = indf['nlj2'].nunique()
innp = []
nlj2lab = []
for i_nlj in indf['nlj2'].unique():
    tmpdf = indf[['En bra','CS^2']].loc[(indf['nlj2']==i_nlj)&(indf['En bra']>-0.1)&(indf['En bra']<6)&(indf['En ket']==0)]
    tmpnp = tmpdf.to_numpy()
    nlj2lab.append(i_nlj)
    innp.append(tmpnp)

arr_zero = zeropad(innp)
fix, ax = plt.subplots()
opacity = 1

bottom_arr = np.zeros(arr_zero[0].shape,float)
i_lab = 0
for arr_plot in arr_zero:
    ax.bar(arr_plot[:,0],arr_plot[:,1],width,bottom=bottom_arr[:,1],label=label(nlj2lab[i_lab]))
    bottom_arr = bottom_arr+arr_plot
    i_lab = i_lab + 1

label(nlj2lab[2])
plt.title(title)
plt.xlabel('Energy [MeV]')
plt.xlim([-0.1,6])
plt.ylabel('$C^2S$')

plt.legend()
plt.savefig(savename, bbox_inches="tight")

print("Finished "+title)
