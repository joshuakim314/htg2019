import sys
import random
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

import pandas as pd
from matrix import *
from statistics_tools import *
import xlrd
import xlsxwriter

csv_name = "/Users/joshuakim/PycharmProjects/HTG2019/consumer-price-index-by-geography-all-items-monthly-percentage-change-not-seasonally-adjusted-canada-provinces-whitehorse-yellowknife-and-iqaluit.csv"
tp = pd.read_csv(csv_name, iterator=True, chunksize=1000) # gives TextFileReader, which is iterable with chunks of 1000 rows
df = pd.concat(tp, ignore_index=True)  # df is DataFrame; if errors, do `list(tp)` instead of `tp`

df = df[(df.ref_date == "2019-01") & (df.products_and_product_groups == "All-items")]
# dropping passed columns
# df.drop(["dguid", "uom", "uom_id", "scalar_factor", "scalar_id", "status", "symbol", "terminated", "decimals"], axis=1, inplace=True)
df = df.sort_values("geo")

count_row = df.shape[0]  # gives number of row count
count_col = df.shape[1]  # gives number of col count

writer = pd.ExcelWriter('cpi_2019.xlsx')
df.to_excel(writer)
writer.save()


if __name__ == "__main__":
    print(df.geo.tolist())
