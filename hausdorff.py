#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 10:55:56 2018

@author: sadra

Hausdorff distance routines
"""
import numpy as np
from gurobipy import Model, GRB, LinExpr

from polytope import ball_polytope


def hausdorff_distance_polytope_to_polytope(p1,p2,norm="uniform",ball_approximation=2):
    d12=directed_distance_polytope_to_polytope(p1,p2,norm,ball_approximation)
    d21=directed_distance_polytope_to_polytope(p2,p1,norm,ball_approximation)
    return max(d12,d21)
    
def directed_distance_polytope_to_polytope(p1,p2,norm,ball_approximation):
    # Distance between two polytopes
    # Inputs: polytope 1, polytope 2
    # Output: distance from polytope 2 to polytope 1: 
        # minimum epsilon such that polytope 2 \subset in polytope 1+ epsilon
    n1=p1.H.shape[1]
    n2=p2.H.shape[1]
    if n1==n2:
        n=n1
    else:
        raise("ERROR: Two polytopes are in different dimensions: %d and %d"%(n1,n2))
    model=Model("Distance between two polytopes")
    p_ball=ball_polytope(n,norm)
    Lambda_main=np.empty((p1.H.shape[0],p2.H.shape[0]),dtype='object')
    Lambda_ball=np.empty((p_ball.H.shape[0],p2.H.shape[0]),dtype='object')
    T_main=np.empty((n,n),dtype='object')
    T_ball=np.empty((n,n),dtype='object')
    epsilon=model.addVar(lb=-10,obj=1,ub=10)
    for row in range(p1.H.shape[0]):
        for column in range(p2.H.shape[0]):
            Lambda_main[row,column]=model.addVar(lb=0,ub=GRB.INFINITY)
    for row in range(p_ball.H.shape[0]):
        for column in range(p2.H.shape[0]):
            Lambda_ball[row,column]=model.addVar(lb=0,ub=GRB.INFINITY)  
    for row in range(n):
        for column in range(n):
            T_main[row,column]=model.addVar(lb=-GRB.INFINITY,ub=GRB.INFINITY)
            T_ball[row,column]=model.addVar(lb=-GRB.INFINITY,ub=GRB.INFINITY)        
    model.update()
    constraints_AB_eq_CD(model,Lambda_main,p2.H,p1.H,T_main)
    constraints_AB_eq_CD(model,Lambda_ball,p2.H,p_ball.H,T_ball)
    constraints_AB_smaller_c(model,Lambda_main,p2.h,p1.h,1)
    constraints_AB_smaller_c(model,Lambda_ball,p2.h,p_ball.h,epsilon)
    for row in range(n):
        for column in range(n):
            model.addConstr(T_main[row,column]+T_ball[row,column]==int(row==column))
    model.optimize()  
    return epsilon.X

def constraints_AB_eq_CD(model,A,B,C,D):
    for row in range(A.shape[0]):
        for column in range(B.shape[1]):
            lhs=LinExpr()
            rhs=LinExpr()
            for k in range(A.shape[1]):
                lhs.add(A[row,k]*B[k,column])
            for k in range(C.shape[1]):
                rhs.add(C[row,k]*D[k,column])
            model.addConstr(rhs==lhs)
            
def constraints_AB_smaller_c(model,A,b,c,epsilon):
    for row in range(A.shape[0]):
        lhs=LinExpr()
        for k in range(A.shape[1]):
            lhs.add(A[row,k]*b[k,0])
            model.addConstr(lhs<=c[row,0]*epsilon)  