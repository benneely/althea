# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:08:30 2016

@author: nn31
"""

import imp

def dynamic_score(path):
    utils = imp.load_source("scores",path)
    return utils.score

