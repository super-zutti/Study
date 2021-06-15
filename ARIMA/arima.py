# 基本のライブラリを読み込む
import numpy as np
import pandas as pd
from scipy import stats

# グラフ描画
from matplotlib import pylab as plt
import seaborn as sns
sns.set()

# グラフを横長にする
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

# 統計モデル
import statsmodels.api as sm

# 普通にデータを読み込む
# https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/AirPassengers.html
dataNormal = pd.read_csv('AirPassengers.csv')
dataNormal.head()

# 以下のコードの方が読み込みは簡単
data = pd.read_csv('AirPassengers.csv', 
                   index_col='Month', 
                   parse_dates=True, 
                   dtype='float')
data.head()