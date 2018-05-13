import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import time
import os

#显示设置
plt.rcParams['font.sans-serif'] = ['SimHei'] #正确显示中文标签
plt.rcParams['axes.unicode_minus'] = False #正确显示负号
plt.style.use('ggplot') #使用ggplot风格绘图

#导入数据
load_path = 'Data\\CleanData\\'
data_date = '2018-02-24' #数据日期
file_load_name = data_date +'Tokyo_clean.csv'
dir_load = os.path.join(load_path,file_load_name)

df = pd.read_csv(dir_load, sep='\t', encoding = 'utf-16')

#图形化处理数据
win1 = plt.figure(num='区划物件数', figsize = (16,8)) #设置窗口标题、窗口大小
pic3 = win1.add_subplot(121) #设置1×2个图，左右排列这是第一个图
pic3.set_title('各区物件数') #设置标题
pic3.set_xlabel('件')
wardlist = df['city_ward'].unique()
ward_count = []
for w in wardlist:
    ward_count.append([w,len(df[df.city_ward == w])])
df_ward_count = DataFrame(ward_count)
df_ward_count.columns = ['ward','count']
print(df_ward_count)
df_ward_count = df_ward_count.sort_values('count', ascending=False)
df_ward_count = df_ward_count.reset_index(drop=True)

print(df_ward_count)
pic3.barh(df_ward_count.index,df_ward_count['count'],tick_label=df_ward_count['ward'])

plt.show()
#bar = pic3.barh(range(len(df['ward'].value_counts())),df['ward'].value_counts(),tick_label=df['ward'].value_counts().index)
#add_labels_barh(bar)
'''

#导入必要的包
from pandas import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

#修正matplotlib中文字符显示错误
plt.rcParams['font.sans-serif'] = ['SimHei'] #正确显示中文标签
plt.rcParams['axes.unicode_minus'] = False #正确显示负号

#plt.style.use('ggplot') #使用ggplot风格绘图
'''
#导入数据
df = pd.read_csv('2018-02-22suumo_DATA.csv', sep='\t', encoding = 'utf-16')

#列名改成英文方便取值
df.columns = ["index","name","address","ward","city","rooms","DK","K","L","S","age","height","order","area","rent_adm","initial_cost","route1","station1","distance1","route2","station2","distance2","route3","station3","distance3","rent","administration","deposit","gratuity","security","non_refund","depreciation","twoyeartotal"]
drop_idx = [30098] #手動でindexを確認
df = df.drop(drop_idx, axis=0)
#列名日英对照
#マンション名name    住所address    区ward    市町村city    間取りrooms    間取りDK    間取りK    間取りL    間取りS    築年数age    建物高さheight
#階order    専有面積area    賃料+管理費rent_adm    敷/礼/保証金initial_cost    路線1route1    駅1station1    徒歩1distance1    路線2route2    
#駅2station2    徒歩2distance2    路線3route3    駅3station3    徒歩3distance3    賃料rent    管理費administration    
#敷金deposit    礼金gratuity    保証金security    敷引non_refund    償却depreciation

#给柱状图添加数据标签
def add_labels_bar(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')

def add_labels_barh(rects):
    for rect in rects:
        rect.get_width() / 2
        plt.text(rect.get_width(),rect.get_y(),rect.get_width(),ha='left', va='bottom')


#图形化处理数据
win1 = plt.figure(num='SuumoData图形可视化1', figsize = (16,8)) #设置窗口标题、窗口大小

#图1:総費用と面積関係図
pic1 = win1.add_subplot(121) #设置1×2个图，左右排列这是第一个图
pic1.set_title('総費用と面積関係図') #设置标题
pic1.set_xlabel('面積（平方米）') #设置X、Y轴标签
pic1.set_ylabel('価格（万円）')
pic1.scatter( df['area'], df['twoyeartotal']/10000,marker = '.')

#图2:総費用と築年関係図
pic2 = win1.add_subplot(122)

pic2.set_title('総費用と築年数関係図')
pic2.set_xlabel('築年数')
pic2.set_ylabel('価格（万円）')
pic2.scatter(df['age'], df['twoyeartotal']/10000, marker = '.')

#图3:各区物件数図
win2 = plt.figure(num='SuumoData图形可视化2', figsize = (16,8)) #设置窗口标题、窗口大小
pic3 = win2.add_subplot(121) #设置1×2个图，左右排列这是第一个图
pic3.set_title('各区物件数') #设置标题
pic3.set_xlabel('件')
bar = pic3.barh(range(len(df['ward'].value_counts())),df['ward'].value_counts(),tick_label=df['ward'].value_counts().index)
add_labels_barh(bar)


#图3:各区物件价格箱线图
pic4 = win2.add_subplot(122)
pic4.set_title('各区物件价格箱线图') #设置标题
pic4.set_xlabel('価格（万円）')
#w = []
#for i in df['ward'].value_counts().index:
 #   w.append(df[df['ward'] == i][['twoyeartotal','ward']])
#print(w)
pic4.boxplot(x = df[['ward','twoyeartotal']],vert = False)

'''
#图2:按房间类型分类的价格箱线图
plt.subplot(1,2,2)
plt.title('間取りと総賃料')
plt.xlabel('総賃料') 
plt.ylabel('間取り') 

room_adm_data = {}
rooms = df['rooms'].unique() #查找房型中的独立值
rooms = np.sort(rooms) #排序
#房型分类
for room in rooms:
    #
    room_adm_data[str(room)] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==0)&(df['L']==0)&(df['S']==0),'rent_adm']
    #k
    room_adm_data[str(room) + 'K'] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==1)&(df['L']==0)&(df['S']==0),'rent_adm']
    #DK
    room_adm_data[str(room) + 'DK'] = df.loc[(df['rooms']==room)&(df['DK']==1)&(df['K']==0)&(df['L']==0)&(df['S']==0),'rent_adm']
    #L
    room_adm_data[str(room) + 'L'] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==0)&(df['L']==1)&(df['S']==0),'rent_adm']
    #S
    room_adm_data[str(room) + 'S'] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==0)&(df['L']==0)&(df['S']==1),'rent_adm']
    #LK
    room_adm_data[str(room) + 'LK'] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==1)&(df['L']==1)&(df['S']==0),'rent_adm']
    #LDK
    room_adm_data[str(room) + 'LDK'] = df.loc[(df['rooms']==room)&(df['DK']==1)&(df['K']==0)&(df['L']==1)&(df['S']==0),'rent_adm']
    #SDK
    room_adm_data[str(room) + 'SDK'] = df.loc[(df['rooms']==room)&(df['DK']==1)&(df['K']==0)&(df['L']==0)&(df['S']==1),'rent_adm']
    #SK
    room_adm_data[str(room) + 'SK'] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==1)&(df['L']==0)&(df['S']==1),'rent_adm']
    #LSK
    room_adm_data[str(room) + 'LSK'] = df.loc[(df['rooms']==room)&(df['DK']==0)&(df['K']==1)&(df['L']==1)&(df['S']==1),'rent_adm']
    #LSDK
    room_adm_data[str(room) + 'LSDK'] = df.loc[(df['rooms']==room)&(df['DK']==1)&(df['K']==0)&(df['L']==1)&(df['S']==1),'rent_adm']

rad_df = pd.DataFrame(room_adm_data) #房型列表转换成DataFrame数据
#plt.boxplot(rad_df, vert = False)#失败
rad_df = rad_df.dropna(axis=1, how='all') #去掉没出现的房型
rad_df.boxplot(vert = False) #画箱线图

#图3:物件价格走势图
fig2 = plt.figure(num='SuumoData图形可视化2', figsize = (16,8)) #设置窗口标题、窗口大小
plt.subplot(1,2,1)
plt.title('物件价走势图')
plt.xlabel('') 
plt.ylabel('价格')

plt.plot(range(len(df)),df.sort_values(by=['rent_adm'], ascending = True)['rent_adm'])


#图4:分房型价格走势

plt.subplot(1,2,2)
plt.title('房型价格走势图')
plt.xlabel('') 
plt.ylabel('价格')
for col in rad_df.columns:
    plt.plot(range(len(rad_df)),rad_df.sort_values(by=[col], ascending = True)[col])
plt.legend()

#图5:散点图-房租与面积的关系
fig3 = plt.figure(num='SuumoData图形可视化3', figsize = (16,8)) #设置窗口标题、窗口大小
plt.subplot(1,2,1) #设置1×2个图，左右排列这是第一个图
plt.title('専有面積と総賃料') #设置标题
plt.xlabel('専有面積') #设置X、Y轴标签
plt.ylabel('総賃料')
plt.scatter(df.index, df['rent_adm'], marker = '.') #画散点图
plt.legend() #设置图例（待学习）
plt.show()
'''