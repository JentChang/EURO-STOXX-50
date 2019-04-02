# EURO-STOXX-50
EURO STOXX 50指数波动率分析
## 获取数据

STOXX网站公布每日历史收盘价格的指数 http://www.stoxx.com/data/historical/hiastorical_benchmark.html

EURO STOXX50指数 >> STOXX Europe600指数 http://www.stoxx.com/download/historical_values/hbrbcpe.txt Historical Data >>Benchmark 

EURO STOXX50波动率 >> VSTOXX每日波动率 http://www.stoxx.com/download/historical_values/h_vstoxx.txt Historical Data >>Strate Indices

```python
from urllib.request import urlretrieve
url_path = 'http://www.stoxx.com/download/historical_values/'
stoxxru600_url = url_path + 'hbrbcpe.txt'
vstoxx_url = url_path + 'h_vstoxx.txt'

data_folder = 'C:\\IWORK\MPF\\EURO STOXX 50\\data\\'
stoxxeu600_filepath = data_folder + 'stoxxeu600.txt'
vstoxx_filepath = data_folder + 'vstoxx.txt'
urlretrieve(stoxxru600_url, stoxxeu600_filepath)
urlretrieve(vstoxx_url, vstoxx_filepath)
```

```python
import pandas as pd
columns = ['Date', 'SX5P', 'SX5E', 'SXXP', 'SXXE', 'SXXF', 'SXXA', 'DK5F', 'DKXF', 'EMPTY']
stoxxeu600 = pd.read_csv(stoxxeu600_filepath, index_col=0, parse_dates=True, dayfirst=True, header=None, skiprows=4, names=columns, sep=';')
del stoxxeu600['EMPTY']
stoxxeu600.head()
vstoxx = pd.read_csv(vstoxx_filepath, index_col=0, parse_dates=True, dayfirst=True, header=2)
vstoxx.head()
```

## 数据合并

```python
import datetime as dt
cutoff_date = dt.datetime(1999, 1, 4)
data = pd.DataFrame({'EUROSTOXX': stoxxeu600['SX5E'][stoxxeu600.index >= cutoff_date],
                    'VSTOXX': vstoxx['V2TX'][vstoxx.index >= cutoff_date]})
data.head()
```

## 财务分析

```python
from pylab import  *
data.plot(subplots=True, figsize=(15, 10), color='b', grid='True')
```
[!图片](/images/history.png)

```python
data[data.EUROSTOXX == 0]
```
### diff：差分  查看收益分布

```python
data.diff().hist(figsize= (15, 5), color='b', bins=100)
```
[!图片](/images/diff.png)

### 绘制对数收益率图表

```python
import numpy as np
log_return = np.log(data / data.shift(1)).dropna()
log_return.plot(subplots=True, figsize=(15, 10), color='b', grid=True)
```
[!图片](/images/rol.png)

## 相关性

```python
log_return.corr()
```
### 回归
```python
import statsmodels.api as sm
ols_fit = sm.OLS(log_return['VSTOXX'].values, log_return['EUROSTOXX'].values).fit()

log_return.plot(figsize=(15, 10), x='EUROSTOXX', y='VSTOXX', kind='scatter')
plot(log_return['EUROSTOXX'], ols_fit.fittedvalues, 'r')
```
[!图片](/images/ols.png)

### 在时间序列上的相关性

>python3的库调用更改了，可以查看3的使用方法

```python
log_return['EUROSTOXX'].rolling(252).corr(log_return['VSTOXX']).plot(figsize=(15, 10))
```
[!图片](/images/rol_ols.png)

