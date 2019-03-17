import sys
import random
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

import pandas as pd
from matrix import *
from statistics_tools import *
import xlrd
import xlsxwriter

csv_name = "/Users/joshuakim/PycharmProjects/HTG2019/14100087-eng/14100087.csv"
tp = pd.read_csv(csv_name, iterator=True, chunksize=1000)  # gives TextFileReader, which is iterable with chunks of 1000 rows
df = pd.concat(tp, ignore_index=True)  # df is DataFrame; if errors, do `list(tp)` instead of `tp`

df = df[(df.REF_DATE == 2018) & (df.Immigrant_status == "Landed immigrants") & (df.Sex == "Both sexes") & (df.Age_group == "25 to 54 years")]
# dropping passed columns
# df.drop(["dguid", "uom", "uom_id", "scalar_factor", "scalar_id", "status", "symbol", "terminated", "decimals"], axis=1, inplace=True)
# df = df.sort_values("geo")

count_row = df.shape[0]  # gives number of row count
count_col = df.shape[1]  # gives number of col count

# writer = pd.ExcelWriter('cpi_2019.xlsx')
# df.to_excel(writer)
# writer.save()

print(df.head())