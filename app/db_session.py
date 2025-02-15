import os
from dotenv import load_dotenv
load_dotenv()

import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import insert, select

user=os.environ.get('user')
password=os.environ.get('password')
host=os.environ.get('host')
port=os.environ.get('port')
dbname=os.environ.get('dbname')

MYSQLALCHEMY_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(MYSQLALCHEMY_URL, echo=False)
conn = engine.connect()

metadata = MetaData()
user_tb = Table("user_tb", metadata, autoload_with=engine)
playlog_tb = Table("playlog_tb", metadata, autoload_with=engine)
playcount_tb = Table("playcount_tb", metadata, autoload_with=engine)
music_tb =  Table("music_tb", metadata, autoload_with=engine)

def get_db():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_user_tb(db, device_id, insert_time):
    insert_user_tb_sql = insert(user_tb).values(device_id=device_id, insert_date =insert_time)
    db.execute(insert_user_tb_sql)
    db.commit()

def insert_playlog_tb(db, music_key, device_id, total_score, insert_time):
    insert_playlog_tb_sql = insert(playlog_tb).values(music_key=music_key, device_id=device_id, total_score=total_score, insert_date =insert_time)
    db.execute(insert_playlog_tb_sql)

def insert_playcount_tb(db, device_id,music_key,count):
    insert_playcount_tb_sql = insert(playcount_tb).values(device_id=device_id, music_key=music_key, count=count)
    db.execute(insert_playcount_tb_sql)

def insert_pandas_playcount_tb(db, device_id,count_log):
    count_log = count_log.replace("'",'"')
    playDatas = json.loads(count_log)["playDatas"]
    
    temp_list = list()
    for i in range(len(playDatas)):
        playData = playDatas[i].split("*")
        music_title = playData[0]
        if music_title == "오르트 구름":
            music_title = "Oort Cloud"
        music_key = select_music_key(music_title)
        music_key_fetchall = music_key.fetchall()
        music_key_start = music_key_fetchall[0][0]
        
        for j in range(8):
            temp_dict = dict()
            temp_dict['device_id'] = device_id
            temp_dict['music_key'] = music_key_start+j
            temp_dict['count'] = playData[j+1]
            temp_list.append(temp_dict)
    temp_df = pd.DataFrame(temp_list)
    temp_df.to_sql(name='playcount_tb', con=engine, if_exists='append', index=False)



def select_user_tb(device_id):
    select_user_tb_sql = select(user_tb).where(user_tb.c.device_id == device_id)
    result = db.execute(select_user_tb_sql)
    return result

def select_playlog_tb(device_id, music_key):
    select_playlog_tb_sql = select(playlog_tb).where(playlog_tb.c.device_id == device_id).where(playlog_tb.c.music_key == music_key)
    result = db.execute(select_playlog_tb_sql)
    return result

def select_music_key(music_title):
    select_music_key_sql = select(music_tb.c.music_key).where(music_tb.c.name == music_title)
    result = db.execute(select_music_key_sql)
    return result