#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib
from lxml import html
from OptionUtility import *
import pandas as pd


# In[2]:


class EurexWebPage:
    
    def __init__(self):
#         self.url = '%s%s%s%s%s' % (
#             "http://www.eurexchange.com/",
#             'exchange-en/market-data/statistics/',
#             'market-statistics-online/100!',
#             'onlineStats?productGroupId=13370&productId=69660',
#             '&viewType=3'
#         )
        self.url = "http://www.eurexchange.com/exchange-en/market-data/statistics/market-statistics-online/100!onlineStats?productGroupId=13370&productId=69660&viewType=3"
        self.param_url = '&cp=%s&month=%s&year=%s&busDate=%s'
        self.lastupdated_dateformat = '%b %d, %Y %H: %M: %S'
        self.web_date_format = '%Y%m%d'
        self.__strike_price_header__ = 'Strike price'
        self.__price_header__ = 'Daily settlem price'
        self.utility = OptionUtility()
        
    def get_available_dates(self):
        html_data = urllib.request.urlopen(self.url).read()
        webpage = html.fromstring(html_data)
        
        dates_listed = webpage.xpath("//select[@name='busDate']" + "/option")
        
        return [date_element.get('value') for date_element in reversed(dates_listed)]
    
    def get_date_from_web_date(self, web_date):
        return self.utility.get_date(web_date, self.web_date_format)
    
    def get_option_series_data(self, is_call, current_dt, option_dt):
        selected_date = current_dt.strftime(self.web_date_format)
        option_type = 'Call' if is_call else 'Put'
        target_url = (self.url + self.param_url) % (option_type, option_dt.month, option_dt.year, selected_date)
        
        html_data = urllib.request.urlopen(target_url).read()
        print(html_data)
        webpage = html.fromstring(html_data)
        print(webpage)
        update_date = self.get_last_update_date(webpage)
        indexes = self.get_date_headers_indexes(webpage)
        data = self.__get_data_rows__(webpage, indexesm, option_type)
        
        return data, update_date
    
    def __get_data_rows__(self, webpage, indexes, header):
        data = pd.DataFrame()
        for row in webpage.xpath("//table[@class='dataTable']/" + "tbody/tr"):
            columns = row.xpath("./td")
            if len(columns) > max(indexes):
                try:
                    [K, price] = [float(columns[i].text.replace(",","")) for i in indexes]
                    data.set_value(K, header, price)
                except:
                    continue
        
        return data
    
    def get_date_headers_indexes(self, webpage):
        table_headers = webpage.xpath("//table[@class='dataTable']" + "/thead/th/text()")
        indexes_of_interest = [table_headers.index(self.__strike_price_header__), table_headers.index(self.__price_header__)]
        
        return indexes_of_interest
    
    def get_last_update_date(self, webpage):
        print(webpage.xpath("//p[@class='date']/b")[-1].text)
        return dt.datetime.strptime(webpage.xpath("//p[@class='date']/b")[-1].text, self.lastupdated_dateformat)


# In[ ]:




