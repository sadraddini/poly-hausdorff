#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 15:35:45 2018

@author: sadra
"""
import numpy as np

def valuation(x):
    """
    Description: given a set of Gurobi variables, output a similar object with values
    Input:
        x: dictionary or a vector, each val an numpy array, each entry a Gurobi variable
        output: x_n: dictionary with the same key as, each val an numpy array, each entry a float 
    """
    if type(x)==type(dict()):
        x_n={}
        for key,val in x.items():
            x_n[key]=np.ones(val.shape)
            (n_r,n_c)=val.shape
            for row in range(n_r):
                for column in range(n_c):
                    x_n[key][row,column]=x[key][row,column].X   
        return x_n
    elif type(x)==type(np.array([])):
        x_n=np.empty(x.shape)
        for row in range(x.shape[0]):
            for column in range(x.shape[1]):
                x_n[row,column]=x[row,column].X
        return x_n
    else:
        raise("x is neither a dictionary or a numpy array")
def vertices_cube(T):
    """
    Description: 2**n * n array of vectors of vertices in unit cube in R^n
    """
    from itertools import product 
    v=list(product(*zip([-1]*T,[1]*T)))
    return np.array(v)

def sample(l,u):
    """
    Description: sample from box of l:lower corner, u: upper corner, with uniform distribution
    """
    return l+(u-l)*np.random.random_sample(l.shape)

def PI(n):
    return np.vstack((np.eye(n),-np.eye(n)))