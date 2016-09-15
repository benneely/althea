# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 15:38:33 2016

@author: nn31
"""
import numpy as np
import pandas as pd

def modelResults(male,nonHispAA,age,sbp,trtbp,tcl,hdl,diab,smoke):
    if male==1 and nonHispAA==0:
        betas={'log_age':12.344,
               'log_age_sqr':0,
               'log_tcl':11.853,
               'log_age_log_tcl':-2.664,
               'log_hdl':-7.99,
               'log_age_log_hdl':1.769,
               'trtsbp':1.797,
               'trtsbp_log_age':0,
               'untrtsbp':1.764,
               'untrtsbp_log_age':0,
               'smoke':7.837,
               'smoke_log_age':-1.795,
               'diabetes':0.658,
               }
        derivation_lp_mean=61.18
        baselineSurvival=0.9144
    elif male==1 and nonHispAA==1:
        betas={'log_age':2.469,
               'log_age_sqr':0,
               'log_tcl':0.302,
               'log_age_log_tcl':0,
               'log_hdl':-0.307,
               'log_age_log_hdl':0,
               'trtsbp':1.916,
               'trtsbp_log_age':0,
               'untrtsbp':1.809,
               'untrtsbp_log_age':0,
               'smoke':0.549,
               'smoke_log_age':0,
               'diabetes':0.645,
               }
        derivation_lp_mean=19.54
        baselineSurvival=0.8954
    elif male==0 and nonHispAA==0:
        betas={'log_age':-29.799,
               'log_age_sqr':4.884,
               'log_tcl':13.54,
               'log_age_log_tcl':-3.114,
               'log_hdl':-13.578,
               'log_age_log_hdl':3.149,
               'trtsbp':2.019,
               'trtsbp_log_age':0,
               'untrtsbp':1.957,
               'untrtsbp_log_age':0,
               'smoke':7.574,
               'smoke_log_age':-1.665,
               'diabetes':0.661,
               }
        derivation_lp_mean=-29.18
        baselineSurvival=0.9665
    elif male==0 and nonHispAA==1:
        betas={'log_age':17.114,
               'log_age_sqr':0,
               'log_tcl':0.94,
               'log_age_log_tcl':0,
               'log_hdl':-18.92,
               'log_age_log_hdl':4.475,
               'trtsbp':29.291,
               'trtsbp_log_age':-6.432,
               'untrtsbp':27.82,
               'untrtsbp_log_age':-6.087,
               'smoke':0.691,
               'smoke_log_age':0,
               'diabetes':0.874,
               }
        derivation_lp_mean=86.61
        baselineSurvival=0.9533
    #start logic
    lage = np.log(age)
    lsbp = np.log(sbp)
    ltcl = np.log(tcl)
    lhdl = np.log(hdl)
    untrtbp = int((trtbp==0))
    #create the linear predictors
    if male==0 and nonHispAA==0:
        lp = ((betas['log_age']*lage) + (betas['log_age_sqr']*(lage)**2) + (betas['log_tcl']*ltcl) + 
        (betas['log_age_log_tcl']*(lage*ltcl)) + (betas['log_hdl']*lhdl) + 
        (betas['log_age_log_hdl']*(lage*lhdl)) + (betas['trtsbp']*(trtbp*lsbp)) + 
        (betas['untrtsbp']*(untrtbp*lsbp)) + (betas['smoke']*smoke) + 
        (betas['smoke_log_age']*(smoke*lage)) + (betas['diabetes']*diab))
    elif male==0 and nonHispAA==1: 
        lp = ((betas['log_age']*lage) + (betas['log_tcl']*ltcl) + (betas['log_hdl']*lhdl) + 
        (betas['log_age_log_hdl']*(lage*lhdl)) + (betas['trtsbp']*(trtbp*lsbp)) + 
        (betas['trtsbp_log_age']*(trtbp*lsbp*lage)) + (betas['untrtsbp']*(untrtbp*lsbp)) + 
        (betas['untrtsbp_log_age']*(untrtbp*lsbp*lage)) + (betas['smoke']*smoke) + 
        (betas['smoke_log_age']*(smoke*lage)) + (betas['diabetes']*diab))
    elif male==1 and nonHispAA==0:
        lp = ((betas['log_age']*lage) + (betas['log_tcl']*ltcl) + (betas['log_age_log_tcl']*(lage*ltcl)) + 
        (betas['log_hdl']*lhdl) + (betas['log_age_log_hdl']*(lage*lhdl)) + 
        (betas['trtsbp']*(trtbp*lsbp)) + (betas['untrtsbp']*(untrtbp*lsbp)) + 
        (betas['smoke']*smoke) + (betas['smoke_log_age']*(smoke*lage)) +
        (betas['diabetes']*diab))
    elif male==1 and nonHispAA==1:  
        lp = ((betas['log_age']*lage) + (betas['log_tcl']*ltcl) + (betas['log_hdl']*lhdl) + 
        (betas['trtsbp']*(trtbp*lsbp)) + (betas['untrtsbp']*(untrtbp*lsbp)) + 
        (betas['smoke']*smoke) + (betas['diabetes']*diab))
    #Now get things on the probscale
    if (age<40 or age>79):
        pred = np.nan
    else:
        pred = (1 - baselineSurvival**(np.exp(lp-derivation_lp_mean)))
    results = {"time":3652.5,
               "risk":pred}
    return results
    
#practice calls
#def test():
#    print(modelResults(0,0,55,120,0,213,50,0,0)        )
#    print(modelResults(0, 1, 55, 120, 0, 213, 50, 0, 0))
#    print(modelResults(1, 0, 55, 120, 0, 213, 50, 0, 0))
#    print(modelResults(1, 1, 55, 120, 0, 213, 50, 0, 0))    
#test()

def score(x):
    zz = pd.DataFrame(x)
    results = zz.apply(lambda x: modelResults(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8]),axis=1)
    return(results.to_dict())

#see what calls to make
#q = np.zeros([1,9])
#q[0,:] = [0,0,55,120,0,213,50,0,0]
#q2 = np.zeros([2,9])
#q2[0,:] = [0, 1, 55, 120, 0, 213, 50, 0, 0]
#q2[1,:] = [1, 0, 55, 120, 0, 213, 50, 0, 0]
#score(q)
#score(q2)













    
        
        