#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from threading import Thread
from dateutil.relativedelta import  relativedelta
from OptionUtility import *
from EurexWebPage import*
from VSTOXXCalculator import *
import time


# In[ ]:


class VSTOXXSubIndex:
    
    def __init__(self, path_to_subindexes):
        self.sub_index_store_path = path_to_subindexes
        self.utility = OptionUtility()
        self.webpage = EurexWebPage()
        self.calculator = VSTOXXCalculator()
        self.csv_date_format = '%m/%d/%Y'
    
    def start(self, months=2, r=0.015):
        for selectse_date in self.webpage.get_available_dates():
            print("正在从 - %s - 收集数据......" % selectse_date)
            self.calculate_and_save_sub_indexes(selectse_date, months, r)
            time.sleep(0.5)
        print('完成')
        
    def calculate_and_save_sub_indexes(self, selectse_date, months_fwd, r):
        current_dt = self.webpage.get_date_from_web_date(selectse_date)
        
        for i in range(1, months_fwd+1):
            expiry_dt = self.utility.fwd_expiry_date(current_dt, i)
            dataset, update_dt = self.get_data(current_dt, expiry_dt)
            
            if not dataset.empty:
                sub_index = self.calculator.calculator_sub_index(dataset, update_dt, expiry_dt)
                self.save_vstoxx_sub_index_to_csv(current_dt, sub_index, i)
                
    def save_vstoxx_sub_index_to_csv(self, current_dt, sub_index, month):
        subindex_df = None
        try:
            subindex_df = pd.read_csv(self.sub_index_store_path, index_col=[0])
        except:
            subindex_df = pd.DataFrame()
        
        display_date = current_dt.strftime(self.csv_date_format)
        subindex_df.set_value(display_date, 'I' + str(month), sub_index)
        subindex_df.to_csv(self.sub_index_store_path)
        
    def get_data(self, current_dt, expiry_dt):
        calls, dt1 = self.webpage.get_option_series_data(True, current_dt, expiry_dt)
        puts, dt2 = self.webpage.get_option_series_data(False, current_dt, expiry_dt)
        option_series = calls.join(puts, how='inner')
        
        if dt1 != dt2:
            print('ERROR: 两个不同的标的价格')
        
        return option_series, dt1

vstoxx_subindex = VSTOXXSubIndex("data/vstoxx_sub_indexes.csv")
vstoxx_subindex.start(2)