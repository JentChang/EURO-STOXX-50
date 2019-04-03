#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import numpy as np


# In[4]:


class VSTOXXCalculator:
    
    def __init__(self):
        self.secs_per_day = float(60 * 60 * 24)
        self.secs_per_year = float(365 * self.secs_per_day)
        
    def calculate_sub_index(self, df, t_calc, t_settle, r):
        T = (t_settle - t_calc).total_seconds() / self.secs_per_year
        R = math.exp(r * T)
        
        df['dK'] = 0
        df['dK'][df.index[0]] = df.index[-1] - df.index[0]
        df['dK'][df.index[-1]] = df.index[-1] - df.index[-2]
        df['dK'][df.index[1:-1]] = (df.index.values[2:] - df.index.values[:-2]) / 2
        
        df['AbsDiffCP'] = abs(df['Call'] - df['Put'])
        min_val = min(df['AbsDiffCP'])
        f_df = df[df['SbsDiffCP'] == min_val]
        fwd_prices = f_df.index + R * (f_df['Call'] - f_df['Put'])
        F = np.mean(fwd_prices)
        
        K_i0 = df.index[df.index <= F][-1]
        
        df['MK'] = 0
        df['MK'][df.index < K_i0] = df['Put']
        df['MK'][K_i0] = (df['Call'][K_i0] + df['Put'][K_i0]) / 2
        df['MK'][df.index > K_i0] = df['Call']
        
        summation = sum(df['dK'] / (df.index.values ** 2)) * R * df['MK']
        variance = 2 / T * summation - 1 / T * (F / float(K_i0) - 1) ** 2
        subindex = 100 * math.sqrt(variance)
        
        return subindex

