#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 18:15:00 2018

@author: sadra
"""

import numpy as np
from gurobipy import Model, GRB, LinExpr

from auxilary_methods import PI
from polytope import polytope

from hausdorff import hausdorff_distance_polytope_to_polytope


p1=polytope(PI(2),1*np.array([1,1,1,1]).reshape(4,1))
p2=polytope(PI(2),1*np.array([1,1.4,0.8,1]).reshape(4,1))
print(hausdorff_distance_polytope_to_polytope(p1,p2))