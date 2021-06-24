#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:47:30 2021

@author: zeynep
"""

import numpy as np

from importlib import reload 
import preferences

reload(preferences)


def get_rbsc(score1, score2):
    """
    This function computes the rank biresial correlation coefficient (RBSC) 
    as defined by Kerby in the following article:
    Kerby, Dave S. 
    "The simple difference formula: An approach to teaching nonparametric correlation."
    Comprehensive Psychology 3 (2014): 11-IT.
    
    Here we denote RBSC with rho. The hypothesis of this subroutine is that 
    score1 is higher than score2 on the average. So be careful in feeding the inputs.
    
    """
    
    favor, unfavor = 0,0
    for d1 in score1:
        for d2 in score2:
            if (d1) > (d2):
                favor += 1
            else:
                unfavor += 1
            
    rbsc = (favor - unfavor) / (favor + unfavor)
    return rbsc
    

def init():
    """
    This function splits the input set into 3 such that we get 2 lists of scores 
    (one higher than the other) and another list with the scores which are not 
    included to the first two lists.
    """
    score = np.random.rand(preferences.LEN_BIG_LIST)
    rank = np.argsort(score)
    
    temp_rank = np.random.randint(low=0, high=preferences.LEN_BIG_LIST, size=(2*preferences.LEN_SMALL_LIST,))
    rank1 = temp_rank[:preferences.LEN_SMALL_LIST]
    rank2 = temp_rank[preferences.LEN_SMALL_LIST:]
    
    #https://www.geeksforgeeks.org/python-difference-two-lists/
    rank_unused = list(set(rank) - set(rank1)) + list(set(rank1) - set(rank))
    rank_unused = list(set(rank_unused) - set(rank2)) + list(set(rank2) - set(rank_unused))
        
    score1 =  [score[r] for r in rank1] 
    score2 =  [score[r] for r in rank2] 
    scores_unused =  [score[r] for r in rank_unused] 
    
    if np.median(score1) > np.median(score2):
        scores_HI = score1
        scores_LO = score2
    else:
        scores_HI = score2
        scores_LO = score1
        
    return scores_HI, scores_LO, scores_unused

    


def move_from_source_to_dest(source,\
               dest, \
               HI_or_LO ):
    """
    This function picks a score from source and moves it to dest. 
    
    The chosen score can be high or low (HI_or_LO) depending on what the 
    intension is.
    """
        
    random_index = -1
    n_pick_iter = 0
    
    source_med = np.median(source)
            
    while n_pick_iter < preferences.NMAX_PICK_SCORE:
        
        n_pick_iter += 1
        random_index = np.random.randint( len(source) )

        """
        We want to pick a high score to source.
        
        In other words, the score picked from source should be higher than the 
        median score of dest.
        """
        if HI_or_LO == 'HI': 
            if source[random_index] > source_med:
                break
            
        elif HI_or_LO == 'LO': 
            if source[random_index] < source_med:
                break    
        else:
            print('The input is not recognized. Enter either HI or LO')
            

    moving = source[random_index]
    source.remove(moving)
    dest.append(moving)
        
    return source, dest, n_pick_iter

def update_HI(scores_HI, scores_unused, rho_prev):
 
    """
    Update **only** a single list (scores_HI)
    """
    
    if rho_prev <= preferences.RHO_STAR - preferences.EPS :   
        """
        If rho_prev is too low, increase it 
        """
        scores_unused, scores_HI, n_pick_iter = move_from_source_to_dest(source= scores_unused,\
                                                           dest = scores_HI, \
                                                           HI_or_LO = 'HI')
        
        scores_HI, scores_unused, n_pick_iter = move_from_source_to_dest(source= scores_HI,\
                                                           dest = scores_unused,\
                                                           HI_or_LO = 'LO')
    elif rho_prev >= preferences.RHO_STAR + preferences.EPS : 
        """
        If rho is too high, decrease it
        """
        scores_unused, scores_HI, n_pick_iter = move_from_source_to_dest(source= scores_unused,\
                                                           dest = scores_HI, \
                                                           HI_or_LO = 'LO')
        
        scores_HI, scores_unused, n_pick_iter = move_from_source_to_dest(source= scores_HI,\
                                                           dest = scores_unused,\
                                                           HI_or_LO = 'HI')     
        
    return scores_HI, n_pick_iter

def update_LO(scores_LO, scores_unused, rho_prev):
 
    """
    Update **only** a single list (scores_LO)
    """
    
    n_pick_iter = 0
    
    if rho_prev <= preferences.RHO_STAR - preferences.EPS :   
        """
        If rho_prev is too low, increase it 
        """
        scores_unused, scores_LO, n_pick_iter = move_from_source_to_dest(source= scores_unused,\
                                                           dest = scores_LO, \
                                                           HI_or_LO = 'LO')
        
        scores_LO, scores_unused, n_pick_iter = move_from_source_to_dest(source= scores_LO,\
                                                           dest = scores_unused,\
                                                           HI_or_LO = 'HI')
    elif rho_prev >= preferences.RHO_STAR + preferences.EPS : 
        """
        If rho is too high, decrease it
        """
        scores_unused, scores_LO, n_pick_iter = move_from_source_to_dest(source= scores_unused,\
                                                           dest = scores_LO, \
                                                           HI_or_LO = 'HI')
        
        scores_LO, scores_unused, n_pick_iter = move_from_source_to_dest(source= scores_LO,\
                                                           dest = scores_unused,\
                                                           HI_or_LO = 'LO')     
        
    return scores_LO, n_pick_iter
    
def update_HI_and_LO(scores_HI, scores_LO, scores_unused, rho):
    """
    Update **both** lists sequentially
    """
       
    n_update_iter = 0
    
    while (not ( (preferences.RHO_STAR - preferences.EPS <= rho)  and\
                (rho <= preferences.RHO_STAR +preferences.EPS) ) )\
           and n_update_iter < preferences.NMAX_UPDATE:
        
        n_update_iter += 1
        
        rho_prev = rho
        scores_HI, n_pick_iter = update_HI(scores_HI, scores_unused, rho_prev)
        rho = get_rbsc(scores_HI, scores_LO)
        
        print('HI n_update_iter: {0:2.0f} \t  rho: {1:2.2f} \t abs(rho_star- rho): {2:2.2f}'.format(\
              n_update_iter, rho, np.abs(preferences.RHO_STAR -rho)))
        
        rho_prev = rho
        scores_LO, n_pick_iter = update_LO(scores_LO, scores_unused, rho_prev)
        rho = get_rbsc(scores_HI, scores_LO)
        
        print('HI n_update_iter: {0:2.0f} \t  rho: {1:2.2f} \t abs(rho_star- rho): {2:2.2f}'.format(\
              n_update_iter, rho, np.abs(preferences.RHO_STAR -rho)))      
