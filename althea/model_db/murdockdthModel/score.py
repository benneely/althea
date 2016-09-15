# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:48:01 2016

@author: nn31
"""

import pandas as pd
import numpy as np
import os
import pickle

module_path = os.path.dirname(__file__) 
#for qc: module_path = '/Users/nn31/Dropbox/40-githubRrepos/althea/althea'
model = pickle.load(open(os.path.join(module_path, 'model_db', 'murdockdthModel', 'model.p'),'rb'))

def linearSpline(x,cut):
    new_le = min(x,cut)
    new_g  = max(x,cut)-cut
    return new_le, new_g


def modelResults(time,age,female,weight,sbp,dbp,pulse,hx_smoking,dukeindx,chf_severity,ef,rdw,creatinine,
                 diabetes,charlson_indx,bun,hglbn,sodium,wbc,cpainfre_p2,afib,lbbb,lvh,qtcor):
                     age_le, age_g = linearSpline(age,60)
                     wt_le, wt_g = linearSpline(weight,80)
                     sysbp_le, sysbp_g = linearSpline(sbp,130)
                     diasbp2_le, diasbp2_g = linearSpline(dbp,90)
                     pulse_le, pulse_g = linearSpline(pulse,80)
                     
                     
