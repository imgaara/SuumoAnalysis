import pandas as pd
import numpy as np
import os

#导入特征数据
load_path = 'Data\\OneHotedData\\'
data_date = '2018-02-24' #数据日期
file_load_name = data_date + 'Kanagawa_Train_Data.csv'
dir_load = os.path.join(load_path, file_load_name)

df = pd.read_csv(dir_load, sep='\t', encoding = 'utf-16')
print('已载入数据包')
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df.fillna(0)

#内存用量
print(df.info(memory_usage='deep'))

# We're going to be calculating memory usage a lot,
# so we'll create a function to save us some time!

def mem_usage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)

df_int = df.select_dtypes(include=['int'])
converted_int = df_int.apply(pd.to_numeric,downcast='unsigned')

print(mem_usage(df_int))
print(mem_usage(converted_int))

compare_ints = pd.concat([df_int.dtypes,converted_int.dtypes],axis=1)
compare_ints.columns = ['before','after']
compare_ints.apply(pd.Series.value_counts)

#内存用量
print(df.info(memory_usage='deep'))

df_float = df.select_dtypes(include=['float'])
converted_float = df_float.apply(pd.to_numeric,downcast='float')

print(mem_usage(df_float))
print(mem_usage(converted_float))

compare_floats = pd.concat([df_float.dtypes,converted_float.dtypes],axis=1)
compare_floats.columns = ['before','after']
compare_floats.apply(pd.Series.value_counts)




optimized_df = df.copy()

optimized_df[converted_int.columns] = converted_int
optimized_df[converted_float.columns] = converted_float

print(mem_usage(df))
print(mem_usage(optimized_df))

#内存用量
print(df.info(memory_usage='deep'))
#内存用量
print(optimized_df.info(memory_usage='deep'))

