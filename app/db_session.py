import config

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import insert, select

user=config.DATABASE_CONFIG['user']
password=config.DATABASE_CONFIG['password']
host=config.DATABASE_CONFIG['host']
port=config.DATABASE_CONFIG['port']
dbname=config.DATABASE_CONFIG['dbname']

MYSQLALCHEMY_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(MYSQLALCHEMY_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
db = SessionLocal()

metadata = MetaData()
user_tb = Table("user_tb", metadata, autoload_with=engine)
playlog_tb = Table("playlog_tb", metadata, autoload_with=engine)
playcount_tb = Table("playcount_tb", metadata, autoload_with=engine)
music_tb =  Table("music_tb", metadata, autoload_with=engine)

def insert_user_tb(device_id, insert_time):
    insert_user_tb_sql = insert(user_tb).values(device_id=device_id, insert_date =insert_time)
    db.execute(insert_user_tb_sql)

def insert_playlog_tb(music_key, device_id, total_score, insert_time):
    insert_playlog_tb_sql = insert(playlog_tb).values(music_key=music_key, device_id=device_id, total_score=total_score, insert_date =insert_time)
    db.execute(insert_playlog_tb_sql)

def insert_playcount_tb(device_id,music_key,count):
    insert_playcount_tb_sql = insert(playcount_tb).values(device_id=device_id, music_key=music_key, count=count)
    db.execute(insert_playcount_tb_sql)

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

def db_commit():
    db.commit()

def db_close():
    db.close()