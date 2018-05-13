# Suumo分析预测
## 简介
爬取Suumo.jp网站的房价信息，使用RandomForest模型进行两年总费用的预测。
## 文件结构
- Scraping.py			-爬虫
	 Data_Cleaning.py		-数据清洗
	 Data_OneHotEncode.py	-特征数据独热编码
	 Train_RF.py			-训练模型
	 Data_Query.py			-输出数据查询
	 Data_Graph.py			-图形化
## update
**[2018/5/13|重新上传]**
**[2018/3/11|修复|v1.02]**:
	
	增加内存优化Data_Optimization.py

**[2018/2/26|修复|v1.01]**:

	修复一户建的楼层错误--->Data_Cleaning.py
	
	修改了独热的实现方法--->Data_OneHotEncode.py
	
	重写调参方法--->Train_RF.py

**[2018/2/24|优化|v1.0]**:

	第一个可用版本