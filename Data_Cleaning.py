import pandas as pd
import numpy as np
import re
import os
import time

#计时开始
start = time.clock()

load_path = 'Data\\RawData\\'
save_path = 'Data\\CleanData\\'
data_date = '2018-02-24' #数据日期

wardlist = ['sagamihara'] #区域列表
#'yokohama', 'kawasaki', 'sagamihara'
#'tokyo_C', 'tokyo_E', 'tokyo_S', 'tokyo_W', 'tokyo_N'
file_save_name = data_date +'Test_clean.csv'
dir_save = os.path.join(save_path,file_save_name)

#读取CSV数据
df = pd.DataFrame()
for w in wardlist:
    file_load_name = data_date + w + '_RawData.csv'
    dir_load = os.path.join(load_path, file_load_name)
    print('载入 --->',dir_load,'...')
    df_load = pd.read_csv(dir_load, sep='\t', encoding = 'utf-16')
    df = pd.concat([df,df_load], axis=0, ignore_index=True)
df = df.reset_index(drop=True)
print('[数据载入完成]')

print('[开始数据清洗]')
#删除 'Unnamed: 0' 列
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df.reset_index(drop=True)
print('删除 Unnamed: 0 列')

#手动删除某行数据
#print(df.loc[109884]['itemurl'])
#drop_idx = []
#df = df.drop(drop_idx, axis=0)
#df = df.reset_index(drop=True)

#删除租金、交通信息、面积缺失的数据
data_n1 = len(df)
df = df.dropna(subset=['rent'])
df = df.dropna(subset=['locations0'])
df = df.dropna(subset=['area'])
data_n2 = len(df)
df = df.reset_index(drop=True)
print('删除租金、交通信息、面积缺失的数据：')
print(data_n1, ' ---> ', data_n2)

###!!!交通信息!!!###
print('[处理交通信息]')
# df['locations*'] ---> df_locations*['route_station*']['distance*']
# [ＪＲ横浜線/相模原駅 歩11分]
# [ＪＲ横浜線/橋本駅 バス15分 (バス停)下九沢団地 歩7分]
df_locations0 = df['locations0'].str.split(' 歩', expand=True)
df_locations0.columns = ['route_station0', 'distance0']
df_locations1 = df['locations1'].str.split(' 歩', expand=True)
df_locations1.columns = ['route_station1', 'distance1']
df_locations2 = df['locations2'].str.split(' 歩', expand=True)
df_locations2.columns = ['route_station2', 'distance2']
df.drop(['locations0','locations1','locations2'], axis=1, inplace=True)
# df_locations*['route_station*']              df_locations*['distance*']
# [ＪＲ横浜線/相模原駅]                          [11分]
# [ＪＲ横浜線/橋本駅 バス15分 (バス停)下九沢団地]  [7分]
df_locations0_spt = df_locations0['route_station0'].str.split('/', expand=True)
df_locations0_spt.columns = ['route0', 'station0']
df_locations0_spt['distance0'] = df_locations0['distance0']
df_locations1_spt = df_locations1['route_station1'].str.split('/', expand=True)
if len(df_locations1_spt.columns) == 2:
    df_locations1_spt.columns = ['route1', 'station1']
else:
    df_locations1_spt.columns = ['route1', 'station1','']
df_locations1_spt['distance1'] = df_locations1['distance1']
df_locations2_spt = df_locations2['route_station2'].str.split('/', expand=True)
if len(df_locations2_spt.columns) == 2:
    df_locations2_spt.columns = ['route2', 'station2']
else :
    df_locations2_spt.columns = ['route2', 'station2','']
#elselen(df_locations2_spt.columns) == 3:
#    df_locations2_spt.columns = ['route2', 'station2','','']
df_locations2_spt['distance2'] = df_locations2['distance2']
# df_locations*['route_station*'] --->df_locations*_spt['route*']['station*']['distance*']
# df_locations*_spt['route*']   df_locations*_spt['station*']       df_locations*_spt['distance*']
# [ＪＲ横浜線]                   [相模原駅]                           [11分]
# [ＪＲ横浜線]                   [橋本駅 バス15分 (バス停)下九沢団地]   [7分]
#cp932格式解码（否则不能替换字符串）
df_locations0_spt['distance0'].str.encode('cp932')
df_locations1_spt['distance1'].str.encode('cp932')
df_locations2_spt['distance2'].str.encode('cp932')
df_locations0_spt['distance0'] = df_locations0_spt['distance0'].str.replace(u'分', u'')
df_locations1_spt['distance1'] = df_locations1_spt['distance1'].str.replace(u'分', u'')
df_locations2_spt['distance2'] = df_locations2_spt['distance2'].str.replace(u'分', u'')
#df_locations*_spt['station*'] ---> df_stn_bus*.columns = ['station*', 'bus*', 'del']
df_stn_bus0 = df_locations0_spt['station0'].str.split('駅', expand=True)
df_stn_bus1 = df_locations1_spt['station1'].str.split('駅', expand=True)
df_stn_bus2 = df_locations2_spt['station2'].str.split('駅', expand=True)
if len(df_stn_bus0.columns) == 3:
    df_stn_bus0.columns = ['station0', 'bus0', 'del']
else:
    df_stn_bus0.columns = ['station0', 'bus0']
if len(df_stn_bus1.columns) == 3:
    df_stn_bus1.columns = ['station1', 'bus1', 'del']
else:
    df_stn_bus1.columns = ['station1', 'bus1']
if len(df_stn_bus2.columns) == 3:
    df_stn_bus2.columns = ['station2', 'bus2', 'del']
else :
    df_stn_bus2.columns = ['station2', 'bus2']
#else:len(df_stn_bus2.columns) == 2
#    df_stn_bus2.columns = ['station2', 'bus2','del','del2']
# df_stn_bus*['station*']  df_stn_bus*['bus*']         df_stn_bus*['del']
# [相模原]                []                            []
# [橋本]                  [ バス15分 (バス停)下九沢団地]  []
#正则表达式提取出数值
df_stn_bus0['bustime0'] = df_stn_bus0['bus0'].str.extract('(\d{1,2})',expand=True)
df_stn_bus1['bustime1'] = df_stn_bus1['bus1'].str.extract('(\d{1,2})',expand=True)
df_stn_bus2['bustime2'] = df_stn_bus2['bus2'].str.extract('(\d{1,2})',expand=True)
#填充NaN
df_stn_bus0['bustime0'] = df_stn_bus0['bustime0'].fillna('0')
df_stn_bus1['bustime1'] = df_stn_bus1['bustime1'].fillna('0')
df_stn_bus2['bustime2'] = df_stn_bus2['bustime2'].fillna('0')
# df_stn_bus*['bustime*']
# []                          
# [15]
#将整理好的数据保存回df_locations*_spt
df_locations0_spt['station0'] = df_stn_bus0['station0']
df_locations1_spt['station1'] = df_stn_bus1['station1']
df_locations2_spt['station2'] = df_stn_bus2['station2']
#巴士时间为步行的5倍
df_locations0_spt['distance0'] = pd.to_numeric(df_stn_bus0['bustime0'])*5 + pd.to_numeric(df_locations0_spt['distance0'])
df_locations1_spt['distance1'] = pd.to_numeric(df_stn_bus1['bustime1'])*5 + pd.to_numeric(df_locations1_spt['distance1'])
df_locations2_spt['distance2'] = pd.to_numeric(df_stn_bus2['bustime2'])*5 + pd.to_numeric(df_locations2_spt['distance2'])
df_locations0_spt['station0'] = df_locations0_spt['station0'] + '駅'
df_locations1_spt['station1'] = df_locations1_spt['station1'] + '駅'
df_locations2_spt['station2'] = df_locations2_spt['station2'] + '駅'
#合并数据
df = pd.concat([df, df_locations0_spt, df_locations1_spt, df_locations2_spt], axis=1)
df = df.reset_index(drop=True)
###!!!交通信息末尾!!!###

#[others] ---> [deposit][gratuity][security][non_refund][depreciation]
print('[处理费用]')
df_others = df['others'].str.split('/', expand=True)
df_others.columns = ['deposit', 'gratuity', 'security', 'non_refund_depreciation']
#[non_refund_depreciation] ---> [non_refund][depreciation]
df_others_nd = df_others['non_refund_depreciation'].str.split('・', expand=True)
if len(df_others_nd.columns) == 1: #如果depreciation皆为空则填充'0'
    df_others_nd['depreciation'] = '0'
df_others_nd.columns = ['non_refund', 'depreciation']
#删除已分割的数据['non_refund_depreciation']['others']
df_others.drop(['non_refund_depreciation'], axis=1, inplace=True)
df.drop(['others'], axis=1, inplace=True)
#合并数据
df = pd.concat([df, df_others, df_others_nd], axis=1)
df = df.reset_index(drop=True)

df['rent'].str.encode('cp932')
df['deposit'].str.encode('cp932')
df['gratuity'].str.encode('cp932')
df['security'].str.encode('cp932')
df['non_refund'].str.encode('cp932')
df['depreciation'].str.encode('cp932')
df['admin'].str.encode('cp932')
df['age'].str.encode('cp932')
df['area'].str.encode('cp932')

#删除数值类型数据中的文字
df['rent'] = df['rent'].str.replace(u'万円', u'')
df['deposit'] = df['deposit'].str.replace(u'万円', u'')
df['gratuity'] = df['gratuity'].str.replace(u'万円', u'')
df['security'] = df['security'].str.replace(u'万円', u'')
df['non_refund'] = df['non_refund'].str.replace(u'万円', u'')
df['depreciation'] = df['depreciation'].str.replace(u'万円', u'')
df['admin'] = df['admin'].str.replace(u'円', u'')
df['age'] = df['age'].str.replace(u'新築', u'0')
df['age'] = df['age'].str.replace(u'築', u'')
df['age'] = df['age'].str.replace(u'年', u'')
df['area'] = df['area'].str.replace(u'm', u'')

#[-] ---> [0]
df['admin'] = df['admin'].replace('-',0)
df['deposit'] = df['deposit'].replace('-',0)
df['gratuity'] = df['gratuity'].replace('-',0)
df['security'] = df['security'].replace('-',0)
df['non_refund'] = df['non_refund'].replace('-',0)
df['non_refund'] = df['non_refund'].replace('実費',0)
df['depreciation'] = df['depreciation'].replace('-',0)

#[None] ---> [0]
df['depreciation'] = [0 if x is None else x for x in df['depreciation']]

#文字列转换为数值
df['rent'] = pd.to_numeric(df['rent'])
df['admin'] = pd.to_numeric(df['admin'])
df['deposit'] = pd.to_numeric(df['deposit'])
df['gratuity'] = pd.to_numeric(df['gratuity'])
df['security'] = pd.to_numeric(df['security'])
df['non_refund'] = pd.to_numeric(df['non_refund'])
df['depreciation'] = pd.to_numeric(df['depreciation'])
df['age'] = pd.to_numeric(df['age'])
df['area'] = pd.to_numeric(df['area'])

#转换单位
df['rent'] = df['rent'] * 10000
df['deposit'] = df['deposit'] * 10000
df['gratuity'] = df['gratuity'] * 10000
df['security'] = df['security'] * 10000
df['non_refund'] = df['non_refund'] * 10000
df['depreciation'] = df['depreciation'] * 10000

#月租金 + 管理费 = 实际月租
df['rent_adm'] = df['rent'] + df['admin']
#其他费用（礼金押金保证金） + 中介手续费(月租+税) = 初期费用
df['initial_cost'] = df['deposit'] + df['gratuity'] + df['security'] + df['rent']*1.08
#两年间总费用
df['total_cost'] = df['rent_adm'] * 24 + df['initial_cost']

#df['address'] ---> ['city']['ward']['addr']
print('[处理地址]')
df_address = df['address'].str.split('区', expand=True)
df_address.columns = ['city_ward','addr']
df_address['city_ward'] = df_address['city_ward'].str.replace('神奈川県','')
df_address['city_ward'] = df_address['city_ward'] + '区'
df = pd.concat([df, df_address], axis=1)
df.drop(['address'], axis=1, inplace=True)
df = df.reset_index(drop=True)

#数值化所在层
#df['floor'] ---> df_floor['floor_min','floor_max']
df_floor = df['floor'].str.split('-', expand=True)
df_floor.columns = ['floor_min','floor_max']
#解码病删除多余文字
df_floor['floor_min'].str.encode('cp932')
df_floor['floor_max'].str.encode('cp932')
df_floor['floor_min'] = df_floor['floor_min'].str.replace(u'階', u'')
df_floor['floor_max'] = df_floor['floor_max'].str.replace(u'階', u'')
df_floor['floor_min'] = df_floor['floor_min'].str.replace(u'B', u'-')
df_floor['floor_max'] = df_floor['floor_max'].str.replace(u'B', u'-')
df_floor['floor_min'] = df_floor['floor_min'].str.replace(u'M', u'')
df_floor['floor_max'] = df_floor['floor_max'].str.replace(u'M', u'')

#替换['floor_max']中的None ---> ''
print('[处理楼层信息]')
df_floor['floor_max'] = df_floor['floor_max'].fillna('')
#填充['floor_max']中的空值为'floor_min'
df_floor.loc[df_floor['floor_max'] =='','floor_max'] = df_floor['floor_min']
#数值化
df_floor['floor_min'] = pd.to_numeric(df_floor['floor_min'])
df_floor['floor_max'] = pd.to_numeric(df_floor['floor_max'])
#求出楼层数
df_floor['floor_n'] = df_floor['floor_max'] - df_floor['floor_min'] + 1
df_floor.drop(['floor_min'], axis=1, inplace=True)
df_floor = df_floor.fillna(0)
df = pd.concat([df, df_floor], axis=1)
df.drop(['floor'], axis=1, inplace=True)
df = df.reset_index(drop=True)

#处理建筑高度
print('[处理建筑高度信息]')
df['height'].str.encode('cp932')
df['height'] = df['height'].str.replace(u'地下1地上', u'')
df['height'] = df['height'].str.replace(u'地下2地上', u'')
df['height'] = df['height'].str.replace(u'地下3地上', u'')
df['height'] = df['height'].str.replace(u'地下4地上', u'')
df['height'] = df['height'].str.replace(u'地下5地上', u'')
df['height'] = df['height'].str.replace(u'地下6地上', u'')
df['height'] = df['height'].str.replace(u'地下7地上', u'')
df['height'] = df['height'].str.replace(u'地下8地上', u'')
df['height'] = df['height'].str.replace(u'地下9地上', u'')
df['height'] = df['height'].str.replace(u'平屋', u'1')
df['height'] = df['height'].str.replace(u'階建', u'')
df['height'] = pd.to_numeric(df['height'])
df = df.reset_index(drop=True)

#处理房型信息
print('[处理房型信息]')
df['DK'] = 0
df['K'] = 0
df['L'] = 0
df['S'] = 0
df['floor_plan'].str.encode('cp932')
df['floor_plan'] = df['floor_plan'].str.replace(u'ワンルーム', u'1')
df_size = len(df)
print('[DK]')
for x in range(df_size):
    if 'DK' in df['floor_plan'][x]: #DK
        df.loc[x,'DK'] = 1
df['floor_plan'] = df['floor_plan'].str.replace(u'DK',u'')
print('[K]')
for x in range(df_size):
    if 'K' in df['floor_plan'][x]: #K
        df.loc[x,'K'] = 1        
df['floor_plan'] = df['floor_plan'].str.replace(u'K',u'')
print('[L]')
for x in range(df_size):
    if 'L' in df['floor_plan'][x]: #L
        df.loc[x,'L'] = 1        
df['floor_plan'] = df['floor_plan'].str.replace(u'L',u'')
print('[S]')
for x in range(df_size):
    if 'S' in df['floor_plan'][x]: #S
        df.loc[x,'S'] = 1        
df['floor_plan'] = df['floor_plan'].str.replace(u'S',u'')
df['rooms'] = pd.to_numeric(df['floor_plan'])
df.drop(['floor_plan'], axis=1, inplace=True)
df = df.reset_index(drop=True)
#重新排列列的顺序
cols = ['name', 'building_type', 'rooms', 'DK', 'K', 'L', 'S',
        'area', 'age', 'height', 'floor_max', 'floor_n',
        'city_ward', 'addr',
        'route0', 'station0', 'distance0',
        'route1', 'station1', 'distance1',
        'route2', 'station2', 'distance2',
        'rent', 'admin', 'deposit', 'gratuity', 'security', 'non_refund', 'depreciation',
        'rent_adm', 'initial_cost', 'total_cost',
        'itemurl']
df = df[cols]

#修复一户建的楼层数
Onebuilding1 = (df['building_type'] == '賃貸一戸建て')
df.loc[Onebuilding1, 'floor_max'] = df.loc[Onebuilding1, 'height']
df.loc[Onebuilding1, 'floor_n'] = df.loc[Onebuilding1, 'height']
Onebuilding2 = (df['building_type'] == '賃貸テラス・タウンハウス')
df.loc[Onebuilding2, 'floor_max'] = df.loc[Onebuilding2, 'height']
df.loc[Onebuilding2, 'floor_n'] = df.loc[Onebuilding2, 'height']

print('保存到 --->',dir_save,'...')
df.to_csv(dir_save, sep = '\t',encoding='utf-16')

#结束计时
elapsed = (time.clock() - start)/60
print('总耗时：',elapsed,'分')
#结束提示音
print("\007")