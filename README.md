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
