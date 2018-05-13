import pandas as pd
import time
import os

#计时开始
start = time.clock()

load_path = 'Data\\CleanData\\'
save_path = 'Data\\OneHotedData\\'
data_date = '2018-02-24' #数据日期
file_save_name = data_date + 'Kanagawa_Train_Data.csv'
dir_save = os.path.join(save_path, file_save_name)

wardlist = ['Kanagawa'] #区域列表
#wardlist = ['Test','Tokyo']

df = pd.DataFrame()
for w in wardlist:
    file_load_name = data_date + w + '_clean.csv'
    dir_load = os.path.join(load_path, file_load_name)
    df_load = pd.read_csv(dir_load, sep='\t', encoding = 'utf-16')
    df =pd.concat([df,df_load], axis=0, ignore_index=True)
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df.reset_index(drop=True)
print('[数据载入完成]')

print('[开始Data特征编码]')

one_hot_building_type = pd.get_dummies(df['building_type'])
df = df.drop('building_type', axis=1)
df =pd.concat([df,one_hot_building_type], axis=1)

one_hot_station0 = pd.get_dummies(df['station0'])
df = df.drop('station0', axis=1)
df =pd.concat([df,one_hot_station0], axis=1)

one_hot_station1 = pd.get_dummies(df['station1'])
df = df.drop('station1', axis=1)
df =pd.concat([df,one_hot_station1], axis=1)

one_hot_station2 = pd.get_dummies(df['station2'])
df = df.drop('station2', axis=1)
df =pd.concat([df,one_hot_station2], axis=1)
print('[编码完成]')
predictors = []
predictors.append('name')
predictors.append('city_ward')
predictors.append('addr')
predictors.append('route0')
predictors.append('route1')
predictors.append('route2')
predictors.append('rent')
predictors.append('admin')
predictors.append('deposit')
predictors.append('gratuity')
predictors.append('security')
predictors.append('non_refund')
predictors.append('depreciation')
predictors.append('rent_adm')
predictors.append('initial_cost')
predictors.append('itemurl')
df = df.drop(predictors, axis=1)

print('保存文件：' + dir_save)
df.to_csv(dir_save, sep = '\t',encoding='utf-16')
#结束计时
elapsed = (time.clock() - start)
print('总耗时：',elapsed,'秒')
#结束提示音
print("\007")
