#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:14:02 2021

@author: zeynep
"""
import numpy as np
import time

from importlib import reload 
import preferences 
reload(preferences)

import tools as tools

if __name__ == '__main__':
    
    start_time = time.time()
    
    scores_HI, scores_LO, scores_unused = tools.init()
    
    rho = tools.get_rbsc(scores_HI, scores_LO)
     
    if preferences.RHO_STAR - preferences.EPS < rho and\
    rho < preferences.RHO_STAR + preferences.EPS:
        print('rho {} is in range RHO_STAR \pm EPS.'.format(rho))
    else:
        print('rho {} is NOT in range RHO_STAR \pm EPS'.format(rho))
        tools.update_HI_and_LO(scores_HI, scores_LO, scores_unused, rho)

        
        
    # Time elapsed 9.67 sec
    elapsed_time = time.time() - start_time
    print('Time elapsed %2.2f sec' %elapsed_time)          

