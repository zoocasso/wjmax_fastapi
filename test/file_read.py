import os
import shutil
import pymysql

db = pymysql.connect(host='wjmax-ubuntu-freetier-db.cshdqhmklshr.ap-northeast-2.rds.amazonaws.com', port=3306, user='root', passwd='wakjmax!', db='wjmax_db', charset='utf8')
cursor = db.cursor()

def file_read():
    for music_folder in music_folder_list:
        music_files = os.listdir(f'{input_dir}/{music_folder}')
        try:
            if not os.path.exists(f'{result_dir}/{music_folder}'):
                os.makedirs(f'{result_dir}/{music_folder}')
        except:
            pass
        for music_file in music_files:
            if '.txt' in music_file or '.ogg' in music_file:
                shutil.move(f'{input_dir}/{music_folder}/{music_file}', f'{result_dir}/{music_folder}/{music_file}')


def make_input_dict(result_folder):
    input_dict = dict()
    txt_list = list()
    key4_list = list()
    key6_list = list()
    result_files = os.listdir(f'{result_dir}/{result_folder}')
    for result_file in result_files:
        if '.txt' in result_file:
            all_list.append(result_file)
        if 'Key6' not in result_file and '.ogg' not in result_file:
            output_list.append(result_file)
            key4_list.append(result_file[:-4])

        if 'Key6' in result_file:
            output_list.append(result_file)
            key6_list.append(result_file[:-4])

        if '.ogg' in result_file:
            input_dict['name'] = result_file[:-4]

    new_key4_list = list()
    for key4_level in key4_list:
        key4_level = key4_level.split(' ')[-1]
        if 'Messi' in key4_level or 'messi' in key4_level:
            new_key4_list.append(0)
        if 'Angel' in key4_level or 'angel' in key4_level:
            new_key4_list.append(1)
        if 'Wakgood' in key4_level or 'wakgood' in key4_level:
            new_key4_list.append(2)
        if 'Minsu' in key4_level or 'minsu' in key4_level:
            new_key4_list.append(3)

    new_key6_list = list()
    for key6_level in key6_list:
        key6_level = key6_level.split(' ')[-2]
        if 'Messi' in key6_level or 'messi' in key6_level:
            new_key6_list.append(0)
        if 'Angel' in key6_level or 'angel' in key6_level:
            new_key6_list.append(1)
        if 'Wakgood' in key6_level or 'wakgood' in key6_level:
            new_key6_list.append(2)
        if 'Minsu' in key6_level or 'minsu' in key6_level:
            new_key6_list.append(3)

    
    # if len(key4_list) != len(new_key4_list):
    #     print(1)
    #     print(key4_list)
    #     print(new_key4_list)
    # if len(key6_list) != len(new_key6_list):
    #     print(2)
    #     print(key6_list)
    #     print(new_key6_list)
    new_key4_list.sort()
    new_key6_list.sort()
    input_dict['key4'] = new_key4_list
    input_dict['key6'] = new_key6_list

    return input_dict

def db_insert(input_dict):
    for key4 in input_dict['key4']:
        sql = f"insert into music_tb (`name`,`key_gubun`,`difficulty`) values ('{input_dict['name']}',0,{key4})"
        cursor.execute(sql)
        db.commit()

    for key6 in input_dict['key6']:
        sql = f"insert into music_tb (`name`,`key_gubun`,`difficulty`) values ('{input_dict['name']}',1,{key6})"
        cursor.execute(sql)
        db.commit()

if __name__ == "__main__":
    input_dir = './Music'
    result_dir = './result'
    music_folder_list = os.listdir(input_dir)
    file_read()
    all_list = list()
    output_list = list()
    result_folder_list = os.listdir(result_dir)
    for result_folder in result_folder_list:
        input_dict = make_input_dict(result_folder)
        db_insert(input_dict)