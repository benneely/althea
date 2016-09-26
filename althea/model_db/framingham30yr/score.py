# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 14:05:39 2016

@author: nn31
"""

import pandas as pd
import numpy as np
import os
import pickle
import pandas as pd

module_path = os.path.dirname(__file__) 
#for qc:
#module_path = '/Users/nn31/Dropbox/40-githubRrepos/althea/althea/model_db/framingham30yr/'
print(module_path)
model = pickle.load(open(os.path.join(module_path,'model.p'),'rb'))



def modelResults(male,age,sbp,tc,hdlc,smoke,trtbp,diab,time=30):
    model_time = model.get('cvd').get('time')
    indx = [i for i,x in enumerate(model_time) if model_time[i] < time]
    newtime = max(indx)+1
    cvd_srv_fnc = model.get('cvd').get('survival_fnc')[:newtime]
    dth_srv_fnc = model.get('dth').get('survival_fnc')[:newtime]
    lcvd = model.get('lcvd')[:newtime]
    bcvd_male  = model.get('cvd').get('betas').get('male')*male
    if ((age>=20) and (age<=60)):
        bcvd_age = model.get('cvd').get('betas').get('age')*np.log(age)
    else:
        bcvd_age = np.nan
    if ((sbp>=78) and (sbp<=240)):
        bcvd_sbp = model.get('cvd').get('betas').get('sbp')*np.log(sbp)
    else:
        bcvd_sbp = np.nan
    if ((tc>=100) and (tc<=405)):
        bcvd_tc = model.get('cvd').get('betas').get('tc')*np.log(tc)
    else:
        bcvd_tc = np.nan 
    bcvd_hdlc = model.get('cvd').get('betas').get('hdlc')*np.log(hdlc)
    bcvd_smoke = model.get('cvd').get('betas').get('smoke')*smoke
    bcvd_trtbp = model.get('cvd').get('betas').get('trtbp')*trtbp
    bcvd_diab  = model.get('cvd').get('betas').get('diab')*diab
    
    bdth_male  = model.get('dth').get('betas').get('male')*male
    bdth_age   = model.get('dth').get('betas').get('age')*np.log(age)
    bdth_sbp   = model.get('dth').get('betas').get('sbp')*np.log(sbp)
    bdth_tc    = model.get('dth').get('betas').get('tc')*np.log(tc)
    bdth_hdlc  = model.get('dth').get('betas').get('hdlc')*np.log(hdlc)
    bdth_smoke = model.get('dth').get('betas').get('smoke')*smoke
    bdth_trtbp = model.get('dth').get('betas').get('trtbp')*trtbp
    bdth_diab  = model.get('dth').get('betas').get('diab')*diab
    bcvdsum    = np.sum([bcvd_male,bcvd_age,bcvd_sbp,bcvd_tc,bcvd_hdlc,
                         bcvd_smoke,bcvd_trtbp,bcvd_diab])
    bcvddth    = np.sum([bdth_male,bdth_age,bdth_sbp,bdth_tc,bdth_hdlc,
                         bdth_smoke,bdth_trtbp,bdth_diab])
    scvd = np.zeros([newtime])
    sdth = np.zeros([newtime])
    Lcvd_S = np.zeros([newtime])
    for i in range(newtime):
        scvd[i] = cvd_srv_fnc[i]**np.exp(bcvdsum-model.get('cvd').get('mean_lp'))
        sdth[i] = dth_srv_fnc[i]**np.exp(bcvddth-model.get('dth').get('mean_lp'))
        if i==0:
            Lcvd_S[i] = np.exp(bcvdsum-model.get('cvd').get('mean_lp'))*(-np.log(cvd_srv_fnc[i]))
        else:
            Lcvd_S[i] = scvd[i-1]*sdth[i-1]*np.exp(bcvdsum-model.get('cvd').get('mean_lp'))*lcvd[i]
    return(np.sum(Lcvd_S) )
     
def score_matrix(x):
    zz = pd.DataFrame(x)
    results = zz.apply(lambda x: modelResults(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8]),axis=1)
    return(results.to_dict())
    
def score(male='Female',
          age=25,
          sbp=110,
          tc=150,
          hdlc=60,
          trtbp='No',
          smoke='No',
          diab='No',
          time=30):
    if male=='Male':
        maley=1
    else:
        maley=0
    if trtbp=='Yes':
        trtbpy=1
    else:
        trtbpy=0
    if smoke=='Yes':
        smokey=1
    else:
        smokey=0
    if diab=='Yes':
        diaby=1
    else:
        diaby=0
    matrix = np.array([[maley,age,sbp,tc,hdlc,smokey,trtbpy,diaby,time]])
    return(score_matrix(matrix))
    
    
#from the paper a couple of test cases to run through 
#figure 3
#~1%
#modelResults(age=25, male=0, tc=150, hdlc=60, trtbp=0, sbp=110, smoke=0, diab=0)
#~3.5%
#age=25; male=0; tc=260; hdlc=35; trtbp=0; sbp=110; smoke=0; diab=0;   
#modelResults(age=25, male=0, tc=260, hdlc=35, trtbp=0, sbp=110, smoke=0, diab=0)
#~6%
#age=25; male=0; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=0; diab=0;
#modelResults(age=25, male=1, tc=260, hdlc=35, trtbp=0, sbp=160, smoke=1, diab=1)
#~12% 
#age=25; male=0; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=1; diab=0;
#~26%
#age=25; male=0; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=1; diab=1;
#modelResults(age=25, male=0, tc=260, hdlc=35, trtbp=0, sbp=160, smoke=1, diab=1)
#missing
#age=3; male=0; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=1; diab=1;
#figure 4
#~1%
#age=25; male=1; tc=150; hdlc=60; trtbp=0; sbp=110; smoke=0; diab=0;
#~5%
#age=25; male=1; tc=260; hdlc=35; trtbp=0; sbp=110; smoke=0; diab=0;
#~10%
#age=25; male=1; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=0; diab=0; 
#~20%
#age=25; male=1; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=1; diab=0;
#~40%
#age=25; male=1; tc=260; hdlc=35; trtbp=0; sbp=160; smoke=1; diab=1;

