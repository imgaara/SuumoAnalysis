import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib #jbolib模块
import matplotlib.pyplot as plt
import os
import time

#计时开始
start = time.clock()

#显示设置
plt.rcParams['font.sans-serif'] = ['SimHei'] #正确显示中文标签
plt.rcParams['axes.unicode_minus'] = False #正确显示负号
plt.style.use('ggplot') #使用ggplot风格绘图

#导入特征数据
load_path = 'Data\\OneHotedData\\'
load_path2 = 'Data\\CleanData\\'
save_path = 'Data\\PredictedData\\'
data_date = '2018-02-24' #数据日期
file_load_name = data_date + 'Kanagawa_Train_Data.csv'
file_load_name2 = data_date + 'Kanagawa_clean.csv'
file_save_name = data_date + 'Kanagawa_Predicted.csv'
dir_save = os.path.join(save_path, file_save_name)
dir_load = os.path.join(load_path, file_load_name)
dir_load2 = os.path.join(load_path2, file_load_name2)
df = pd.read_csv(dir_load, sep='\t', encoding = 'utf-16')
print('已载入数据包')
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df.fillna(0)

# 列出对结果有影响的字段
predictors = []
for i in df.columns:
    predictors.append(i)
predictors.remove('total_cost')

#随机划分训练集和测试集
train_feature,test_feature, train_target, test_target = train_test_split(df[predictors],    #所要划分的样本特征集
                                                                         df['total_cost'], #所要划分的样本结果
                                                                         test_size = 0.1, #样本占比，如果是整数的话就是样本的数量
                                                                         random_state = 66)  #随机数的种子。

#调参
'''
print("调参开始")
def perparameter(parameter_range,train_feature,test_feature, train_target, test_target):
    results = []
    for para in parameter_range:
        alg = RandomForestRegressor(n_estimators=111,
                                    criterion = 'mse',
                                    max_features = 0.8,
                                    max_depth = 40,
                                    min_samples_split =3,
                                    min_samples_leaf = 1,
                                    max_leaf_nodes = None,
                                    bootstrap = True,
                                    oob_score = True,
                                    warm_start = False, #是否热启动
                                    n_jobs=-1,verbose=1)
        alg.fit(train_feature, train_target)
        predict = alg.predict(test_feature)
        ob_pnt = alg.score(test_feature ,test_target)
        pnt = (test_target.max() - (test_target - predict).std())/test_target.max()
        print((para, ob_pnt,pnt))
        results.append((para, ob_pnt, pnt))
    return(results)
parameter_range = list(np.arange(1,10,1))

results = perparameter(parameter_range, train_feature, test_feature, train_target, test_target)
#图1:n_estimators
best_result = max(results, key=lambda x: x[1])
best_result_value = best_result[0]
print(best_result)

re_df = pd.DataFrame(results)
re_df.columns = ['para','ob_pnt','pnt']

win = plt.figure(num='模型调参', figsize = (16,8)) #设置窗口标题、窗口大小
pic1 = win.add_subplot(121) #设置2×4个图，这是第一个图
pic1.set_title('n_estimators') #设置标题
pic1.set_xlabel('Values') #设置X、Y轴标签
pic1.set_ylabel('Points')
pic1.plot(re_df['para'],re_df['pnt'])
pic1 = win.add_subplot(122) #设置2×4个图，这是第一个图
pic1.set_title('n_estimators') #设置标题
pic1.set_xlabel('Values') #设置X、Y轴标签
pic1.set_ylabel('Points')
pic1.plot(re_df['para'],re_df['ob_pnt'])

plt.show()

'''
print('正式开始')
'''
###训练模型
alg = RandomForestRegressor(n_estimators=111,
                            criterion = 'mse',
                            max_features = 0.8,
                            max_depth = 40,
                            min_samples_split =3,
                            min_samples_leaf = 1,
                            max_leaf_nodes = None,
                            bootstrap = True,
                            oob_score = True,
                            warm_start = False, #是否热启动
                            n_jobs=-1,verbose=1)
alg.fit(train_feature, train_target)

#保存模型
joblib.dump(alg, "train_model.pkl", compress = 3)
'''
#读取模型
alg = joblib.load("train_model.pkl")
#测试模型
print('模型得分：', alg.oob_score_, alg.score(test_feature ,test_target))

#保存预测值
predicted_value = alg.predict(df[predictors])

df2 = pd.read_csv(dir_load2, sep='\t', encoding = 'utf-16')
df2['predicted_value'] = predicted_value
df2['difference'] = df2['predicted_value'] - df2['total_cost']
df2.to_csv(dir_save, sep = '\t', encoding = 'utf-16')

#结束计时
elapsed = (time.clock() - start)
print('总耗时：',elapsed,'秒')
#结束提示音
print("\007")