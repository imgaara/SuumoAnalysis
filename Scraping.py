from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time
import os

#各区域网页链接Data
wardlist = []

#横滨
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14101&sc=14102&sc=14103&sc=14104&sc=14105&sc=14106&sc=14107&sc=14108&sc=14109&sc=14110&sc=14111&sc=14112&sc=14113&sc=14114&sc=14115&sc=14116&sc=14117&sc=14118&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'yokohama'
wardlist.append([url,name])
#川崎
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14131&sc=14132&sc=14133&sc=14134&sc=14135&sc=14136&sc=14137&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'kawasaki'
wardlist.append([url,name])
#湘模原
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14151&sc=14152&sc=14153&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'sagamihara'
wardlist.append([url,name])
'''
#东京都心部
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'tokyo_C'
wardlist.append([url,name])
#东京23区東部
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'tokyo_E'
wardlist.append([url,name])

#东京23区南部
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13109&sc=13110&sc=13111&sc=13112&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'tokyo_S'
wardlist.append([url,name])
#东京23区西部
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13114&sc=13115&sc=13120&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'tokyo_W'
wardlist.append([url,name])
#东京23区北部
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13116&sc=13117&sc=13119&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
name = 'tokyo_N'
wardlist.append([url,name])
'''
#wardlist = [['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14114&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1','test']]

def Scraping(url,areaname):

    #下载网页导入BeautifulSoup对象化
    print('读取首页中...')
    result = requests.get(url) 
    c = result.content
    soup = BeautifulSoup(c)

    #设置保存文件名
    path = 'Data\\RawData\\'
    filename = time.strftime('%Y-%m-%d', time.localtime()) + areaname + '_RawData.csv'
    dir_file = os.path.join(path, filename)
    #从 <div id="js-bukkenList"> 中提取物件列表 --->summary
    summary = soup.find('div',{'id':'js-bukkenList'})

    #提取总页数
    body = soup.find('body')
    pages = body.find_all('div', {'class':'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n\t</ol>')
    pages_split0 = pages_split[0]
    pages_split1 = pages_split0[-4:]
    pages_split2 = pages_split1.replace('>', '')
    pages_split3 = pages_split2.replace('\"', '')
    pages_split4 = int(pages_split3)
    print('总页数 = ', str(pages_split4))

    #处理页面url
    urls = [] #所有页面URL列表
    urls.append(url) #存入第一页URL（首页单独处理）
    #存入其他页面URL
    for i in range(pages_split4-1):
        pg = str(i + 2)
        url_page = url + '&pn=' + pg
        urls.append(url_page)

    #所有Data列表
    name = [] #名称
    address = [] #地址
    building_type = [] #建筑类型
    locations0 = [] #交通1（最寄駅/徒歩~分）
    locations1 = [] #交通2（最寄駅/徒歩~分）
    locations2 = [] #交通3（最寄駅/徒歩~分）
    age = [] #房龄
    height = [] #建筑高度
    floor = [] #所在层
    rent = [] #月租金
    admin = [] #管理费
    others = [] #其他费用（敷/礼/保証/敷引,償却）
    floor_plan = [] #户型
    area = [] #面积
    itemurl = [] #链接
    
    #爬虫主循环
    print('[爬虫启动]')
    counter = 0 #计数器
    for url in urls:
        #计数
        counter = counter + 1
        print('区域:', areaname, '进度：', str(counter), '/', str(pages_split4))

        #计时开始
        start = time.clock()

        #下载网页导入BeautifulSoup对象化
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c)

        #从 <div id="js-bukkenList"> 中提取物件列表 --->summary
        summary = soup.find('div', {'id':'js-bukkenList'})

        #从 <div class="cassetteitem"> 中提取：名称、地址、交通信息、房龄、建筑高度 --->cassetteitems
        cassetteitems = summary.find_all('div', {'class':'cassetteitem'})
        for i in range(len(cassetteitems)):
            #提取同一房源中的所有物件 --->tbodies
            tbodies = cassetteitems[i].find_all('tbody')

            #提取名称 --->subtitle_rep2
            subtitle = cassetteitems[i].find_all('div', {'class':'cassetteitem_content-title'})
            subtitle = str(subtitle)
            subtitle_rep = subtitle.replace('[<div class="cassetteitem_content-title">', '')
            subtitle_rep2 = subtitle_rep.replace('</div>]', '')

            #提取建筑类型 --->subclass_rep2
            subclass = cassetteitems[i].find_all('div', {'class':'cassetteitem_content-label'})
            subclass = str(subclass)
            subclass_rep = subclass.replace('[<div class="cassetteitem_content-label"><span class="ui-pct ui-pct--util1">', '')
            subclass_rep2 = subclass_rep.replace('</span></div>]', '')

            #提取地址 --->subaddress_rep2
            subaddress = cassetteitems[i].find_all('li', {'class':'cassetteitem_detail-col1'})
            subaddress = str(subaddress)
            subaddress_rep = subaddress.replace('[<li class="cassetteitem_detail-col1">', '')
            subaddress_rep2 = subaddress_rep.replace('</li>]', '')
            
            #存入与房源中物件数相同数量的信息
            for y in range(len(tbodies)):
                name.append(subtitle_rep2) #名称
                address.append(subaddress_rep2) #地址
                building_type.append(subclass_rep2) #建筑类型
    
            #从 <li class="cassetteitem_detail-col2"> 中提取交通信息 --->sublocations
            sublocations = cassetteitems[i].find_all('li', {'class':'cassetteitem_detail-col2'})
            #交通1～交通3
            for x in sublocations:
                cols = x.find_all('div')
                for j in range(len(cols)):
                    text = cols[j].find(text=True)
                    for y in range(len(tbodies)):
                        if j == 0:
                            locations0.append(text)
                        elif j == 1:
                            locations1.append(text)
                        elif j == 2:
                            locations2.append(text)
            
            #从 <li class="cassetteitem_detail-col3"> 中提取房龄、建筑高度 --->col3
            col3 = cassetteitems[i].find_all('li', {'class':'cassetteitem_detail-col3'})
            for x in col3:
                cols = x.find_all('div')
                for k in range(len(cols)):
                    text = cols[k].find(text=True)
                    for y in range(len(tbodies)):
                        if k == 0:
                            age.append(text)
                        else:
                            height.append(text)

        #从 <tbody> 中提取：所在层、月租金、管理费、其他费用、户型、面积、链接 --->tables
        tables = summary.find_all('tbody')
        for i in range(len(tables)):
            rows = tables[i].find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                floor.append(cols[2].text) #所在层
                rent.append(cols[3].text) #月租金
                admin.append(cols[4].text) #管理费
                others.append(cols[5].text) #其他费用
                floor_plan.append(cols[6].text) #户型
                area.append(cols[7].next) #面积

            #从 <td class="ui-text--midium ui-text--bold"> 中提取链接 --->urlcol3
            urlcol = tables[i].find_all('td', {'class':'ui-text--midium ui-text--bold'})
            urlcol2 = urlcol[0].a['href']
            urlcol3 = 'https://suumo.jp' + urlcol2
            itemurl.append(urlcol3)
            
        #和谐爬虫，休息一下
        #time.sleep(10)
        #计时结束
        elapsed = (time.clock() - start)
        print('耗时：',elapsed,'秒')
    
    #把数据转换为Series
    name = Series(name)
    address = Series(address)
    locations0 = Series(locations0)
    locations1 = Series(locations1)
    locations2 = Series(locations2)
    age = Series(age)
    height = Series(height)
    floor = Series(floor)
    rent = Series(rent)
    admin = Series(admin)
    others = Series(others)
    floor_plan = Series(floor_plan)
    area = Series(area)
    building_type = Series(building_type)
    itemurl = Series(itemurl)

    #合并数据为DataFrame
    suumo_df = pd.concat([name, address, locations0, locations1,locations2, age, height, floor, rent, admin, others, floor_plan, area, building_type, itemurl],axis=1)
    
    #列名
    suumo_df.columns=['name', 'address', 'locations0', 'locations1', 'locations2', 'age', 'height', 'floor', 'rent', 'admin', 'others', 'floor_plan', 'area', 'building_type', 'itemurl']
    
    #保存到CSV文件
    print('保存到---> ' + dir_file)
    suumo_df.to_csv(dir_file, sep = '\t',encoding='utf-16')

#计时开始
start = time.clock()

#循环爬虫
for w in wardlist:
    Scraping(w[0],w[1])

#结束计时
elapsed = (time.clock() - start)
print('总耗时：',elapsed,'秒')
#结束提示音
print("\007")