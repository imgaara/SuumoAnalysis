import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#修正matplotlib中文字符显示错误
plt.rcParams['font.sans-serif'] = ['SimHei'] #正确显示中文标签
plt.rcParams['axes.unicode_minus'] = False #正确显示负号

#Pandas显示设置
pd.set_option('max_rows',200)
pd.set_option('max_columns',200)
pd.set_option("display.max_colwidth", 80)

#路径设置
load_path = 'Data\\PredictedData\\'
save_path = 'Results\\'
data_date = '2018-02-28' #数据日期
file_load_name = data_date + 'Kanagawa_Predicted.csv'
dir_load = os.path.join(load_path, file_load_name)
#读取数据
df = pd.read_csv(dir_load, sep='\t', encoding = 'utf-16')
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df.reset_index(drop=True)
print('[载入数据完成]')

#查询某条数据
'''
df1 = df.loc[df['name'] == 'アイレット']
df2 = df.loc[(df['area'] == 57.75) & (df['rent_adm'] == 109500)][['name','floor_max','cha']]
df3 = df.loc[df['name'] == 'ピアエスポワール']
print(df1)
print(df2)
print(df3)
'''
'''
df_1_s1 = df.loc[(df["station0"] == "武蔵小杉駅") & (df["distance0"] < 10)]
df_1_s2 = df.loc[(df["station1"] == "武蔵小杉駅") & (df["distance1"] < 10)]
df_1_s3 = df.loc[(df["station2"] == "武蔵小杉駅") & (df["distance2"] < 10)]
#
#df_2_s1 = df.loc[(df["station0"] == "日吉駅") & (df["distance0"] < 15)]
#df_2_s2 = df.loc[(df["station1"] == "日吉駅") & (df["distance1"] < 15)]
#df_2_s3 = df.loc[(df["station2"] == "日吉駅") & (df["distance2"] < 15)]
#
#df_3_s1 = df.loc[(df["station0"] == "元住吉駅") & (df["distance0"] < 15)]
#df_3_s2 = df.loc[(df["station1"] == "元住吉駅") & (df["distance1"] < 15)]
#df_3_s3 = df.loc[(df["station2"] == "元住吉駅") & (df["distance2"] < 15)]

df_4_s1 = df.loc[(df["station0"] == "新丸子駅") & (df["distance0"] < 11)]
df_4_s2 = df.loc[(df["station1"] == "新丸子駅") & (df["distance1"] < 11)]
df_4_s3 = df.loc[(df["station2"] == "新丸子駅") & (df["distance2"] < 11)]
df_c = pd.concat([df_4_s1,df_4_s2,df_4_s3], axis=0,ignore_index=True)
#df_1_s1,df_1_s2,df_1_s3,df_2_s1,df_2_s2,df_2_s3,df_3_s1,df_3_s2,df_3_s3,
#df_c2 = df_c.loc[(df_c['difference'] < 100) & (df_c['difference'] > -100) & (df_c['total_cost'] > 3000000)]
df_c2 = df_c.loc[(df_c['difference'] < -1000) & (df_c['difference'] >-20000)]
#df4 = df_c2.sort_values(["difference",'area'],ascending=False).head(200)
df4 = df_c2.sort_values(['area'],ascending=False).head(200)
print(df4)
dir_save = os.path.join(save_path, 'result1.csv')
df4.to_csv(dir_save, sep = '\t',encoding='utf-16')
'''
'''
df_top = df.sort_values(['difference'],ascending=False).head(20)
dir_save = os.path.join(save_path, 'result2.csv')
df_top.to_csv(dir_save, sep = '\t',encoding='utf-16
'''
'''
df_top = df.sort_values(['difference'],ascending=False).tail(20)
dir_save = os.path.join(save_path, 'result3.csv')
df_top.to_csv(dir_save, sep = '\t',encoding='utf-16')
'''
df_1_s1 = df.loc[("白楽" in str(df["station0"])) & (df["distance0"] < 10)]
df_1_s2 = df.loc[("白楽" in df["station1"]) & (df["distance1"] < 10)]
df_1_s3 = df.loc[("白楽" in df["station2"]) & (df["distance2"] < 10)]
df_c = pd.concat([df_1_s1,df_1_s2,df_1_s3], axis=0,ignore_index=True)
df_c = df_c.sort_values(['rent_adm'],ascending=True)
print(df_c)
