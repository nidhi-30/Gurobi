#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gurobipy as gp
from gurobipy import GRB
import numpy as np


# In[5]:


print("Model 1: Solution of Problem 1")

try:
    # Create a new model
    m1 = gp.Model("doctor-patient-model1")
    
    # Create variables
    d4p1 = m1.addVar(name="d4p1")
    d4p2 = m1.addVar(name="d4p2")
    d5p1 = m1.addVar(name="d5p1")
    d5p2 = m1.addVar(name="d5p2")
    
    # Set objective
    m1.setObjective(130*d4p1 + 95* d4p2 + 118* d5p1 + 83* d5p2, GRB.MINIMIZE)
    
    # Add constraints
    m1.addConstr(d4p1 + d4p2 == 1, "c0")
    m1.addConstr(d5p1 + d5p2 == 1, "c1")
    m1.addConstr(d4p1 + d5p1 == 1, "c2")
    m1.addConstr(d4p2 + d5p2 == 1, "c3")
    
    # Optimize model
    m1.optimize()
    
    for v in m1.getVars():
        print('%s %g' % (v.varName, v.x))
        
    print('Obj: %g' % m1.objVal)
    
except gp.GurobiError as e:
    print('Error code' + str(e.errno) + ': ' + str(e))
    
except AttributeError:
    print('Encountered an attribute error')


# In[3]:


print("Model 2: Solution of Problem 2")

# Randomly add values to the table
np.random.seed(2004)
time = np.random.randint(50, 150 ,size = (36))

# Assign values that were alrady given
time[18] = 130
time[19] = 95
time[24] = 118
time[25] = 83

# Define keys for each doctor and patient
keys = [('d1','p1'),('d1','p2'),('d1','p3'),('d1','p4'),('d1','p5'),('d1','p6'),
       ('d2','p1'),('d2','p2'),('d2','p3'),('d2','p4'),('d2','p5'),('d2','p6'),
       ('d3','p1'),('d3','p2'),('d3','p3'),('d3','p4'),('d3','p5'),('d3','p6'),
       ('d4','p1'),('d4','p2'),('d4','p3'),('d4','p4'),('d4','p5'),('d4','p6'),
       ('d5','p1'),('d5','p2'),('d5','p3'),('d5','p4'),('d5','p5'),('d5','p6'),
       ('d6','p1'),('d6','p2'),('d6','p3'),('d6','p4'),('d6','p5'),('d6','p6')]

try:
    # Convert to dictionary
    dic = gp.multidict(zip(keys, time))
    dict_keys, dict_time = dic
    
    # Define list for doctors and patients
    docs = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6']
    pats = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']
    
    # Create a new model
    m2 = gp.Model("doctor-patient-model2")
    
    # Create variables
    x = m2.addVars(dict_keys, name='value')
                    
    # Set objective    
    m2.setObjective(x.prod(dict_time), GRB.MINIMIZE)
        
    # Add constraints
    for i in docs:
        m2.addConstr(sum(x[i,j] for j in pats) == 1, "c0")
    for p in pats:
        m2.addConstr(sum(x[q,p] for q in docs) == 1, "c1")
    
    # Optimize model
    m2.optimize()
    
    for v in m2.getVars():
        print('%s %g' % (v.varName, v.x))
        
    print('Obj: %g' % m2.objVal)
    
except gp.GurobiError as e:
    print('Error code' + str(e.errno) + ': ' + str(e))
    
except AttributeError:
    print('Encountered an attribute error')

