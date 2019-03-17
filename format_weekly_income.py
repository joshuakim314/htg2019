import sys
import random
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

import pandas as pd
from matrix import *
from statistics_tools import *
import xlrd
import xlsxwriter

csv_name = "/Users/joshuakim/PycharmProjects/HTG2019/average-weekly-earnings-by-industry-annual.csv"
tp = pd.read_csv(csv_name, iterator=True, chunksize=1000) # gives TextFileReader, which is iterable with chunks of 1000 rows
df = pd.concat(tp, ignore_index=True)  # df is DataFrame; if errors, do `list(tp)` instead of `tp`

df = df[(df.geo == "Prince Edward Island") & (df.type_of_employees == "All employees") & (df.overtime == "Including overtime") & (df.status != "F") & (df.status != "x") & (df.status != "..")]
# dropping passed columns
# df.drop(["dguid", "uom", "uom_id", "scalar_factor", "scalar_id", "status", "symbol", "terminated", "decimals"], axis=1, inplace=True)
df = df.sort_values("north_american_industry_classification_system_naics")

count_row = df.shape[0]  # gives number of row count
count_col = df.shape[1]  # gives number of col count

prev_row = 0
df_list = []
for row in range(count_row-1):
    if df.iloc[row][5] != df.iloc[row+1][5]:
        df_temp = df.iloc[prev_row:row+1, :]
        df_list.append(df_temp)
        prev_row = row+1
    else:
        continue
df_list.append(df.iloc[prev_row:, :])

# for df_temp in df_list:
#     print(df_temp.shape[0])

linear_fit_income = dict()
for df_temp in df_list:
    terminated = False
    if df_temp.iloc[0][13] == "t":
        terminated = True
    df_temp = df_temp.sort_values("ref_date")
    ref_date_list = df_temp["ref_date"].tolist()
    weekly_earning_list = df_temp["value"].tolist()
    empty_indices = []
    for i in range(len(weekly_earning_list)):
        if weekly_earning_list[i] == "nan":
            empty_indices.append(i)
    for index in sorted(empty_indices, reverse=True):
        del ref_date_list[index]
        del weekly_earning_list[index]
    if len(weekly_earning_list) < 2:
        linear_fit_income[df_temp.iloc[0][5]] = [False, False, False, True]
        continue
    coeff = linear_least_square_fit(ref_date_list, response=weekly_earning_list)
    correl = pearson_correlation_sample(ref_date_list, weekly_earning_list)
    linear_fit_income[df_temp.iloc[0][5]] = [coeff[0], coeff[1], correl, terminated]

for key, value in linear_fit_income.items():
    print(key, value)

workbook = xlsxwriter.Workbook("weekly_earning_prince_edward_island.xlsx")
worksheet = workbook.add_worksheet()
row_excel = 0

worksheet.write(row_excel, 0, "Industry")
worksheet.write(row_excel, 1, "Constant Coefficient")
worksheet.write(row_excel, 2, "Variable Coefficient")
worksheet.write(row_excel, 3, "Pearson Correlation")
worksheet.write(row_excel, 4, "Terminated")
row_excel += 1

for key in linear_fit_income.keys():
    worksheet.write(row_excel, 0, key)
    worksheet.write(row_excel, 1, linear_fit_income[key][0])
    worksheet.write(row_excel, 2, linear_fit_income[key][1])
    worksheet.write(row_excel, 3, linear_fit_income[key][2])
    worksheet.write(row_excel, 4, linear_fit_income[key][3])
    row_excel += 1
workbook.close()
