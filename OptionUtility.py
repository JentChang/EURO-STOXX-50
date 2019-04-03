#!/usr/bin/env python
# coding: utf-8

# In[2]:


import calendar as cal
import datetime as dt
from dateutil.relativedelta import relativedelta


# In[3]:


class OptionUtility:
    
    def get_settlement_date(self, date):
        day = 21 - (cal.weekday(date.year, date.month, 1) + 2) % 7
        return dt.datetime(date.year, date.month, day, 12, 0, 0)
    
    def get_date(self, web_date_string, date_format):
        return dt.datetime.strptime(web_date_string, date_format)
    
    def fwd_expiry_date(self, current_dt, month_fws):
        return self.get_settlement_date(current_dt + relativedelta(month = +month_fws))


# In[ ]:




