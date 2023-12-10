import json
import pymysql
import pandas as pd

db = pymysql.connect(host='wjmax-ubuntu-freetier-db.cshdqhmklshr.ap-northeast-2.rds.amazonaws.com', port=3306, user='root', passwd='wakjmax!', db='wjmax_db', charset='utf8')
cursor = db.cursor()

with open('message.txt','r',encoding='UTF8') as f:
    playDatas = json.loads(f.read())['playDatas']
    
user_key = 'zoocasso'
temp_list = list()
for i in range(len(playDatas)):
    playData = playDatas[i].split("*")
    
    ### user_key 조회하여 변수저장 로직 필요

    title = playData[0]
    if title == "오르트 구름":
        title = "Oort Cloud"
    select_sql = f"SELECT music_key FROM music_tb WHERE `name` = '{title}' LIMIT 1"
    cursor.execute(select_sql)
    db.commit()
    music_key_start = cursor.fetchone()[0]
    for j in range(8):
        temp_dict = dict()
        temp_dict['device_id'] = user_key
        temp_dict['music_key'] = music_key_start+j
        temp_dict['count'] = playData[j+1]
        temp_list.append(temp_dict)
temp_df = pd.DataFrame(temp_list)
print(temp_df)
        # print(f"INSERT INTO playcount_tb (`user_key`, `music_key`, `count`) values ({user_key},{music_key_start+j},{playData[j+1]})")