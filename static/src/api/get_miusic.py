# -*- coding:utf-8 -*-
# import requests
# res = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=2&w=麻雀&format=json')
# re = requests.get('http://c.y.qq.com/soso/fcgi-bin/music_search_new_platform?t=0& n=5&aggr=1&cr=1&loginUin=0&format=json& inCharset=GB2312&outCharset=utf-8&notice=0& platform=jqminiframe.json&needNewCode=0&p=1&catZhida=0& remoteplace=sizer.newclient.next_song&w=周杰伦')
# ree = requests.get('https://c.y.qq.com/soso/fcgi-bin/music_search_new_platform?searchid=53806572956004615&t=1&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=2&w=没那么简单')
# rsss = requests.get('https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songid=649069&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback')

# from aip import AipSpeech


# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         print(fp.read())
#         return fp.read()
#
#
# get_file_content('I:/work/flask/static/src/api/file/RECORDING/200430-163328.mp3')
# 识别本地文件
# result = client.asr(get_file_content('I:/work/flask/static/src/api/file/RECORDING/200430-163328.mp3'), 'pcm', 16000, {'dev_pid': 1537, })
# print(result)

# from pydub.audio_segment import AudioSegment

import pydub
from pydub import AudioSegment
from pymediainfo import MediaInfo
# from pydub.utils import mediainfo
import os
from aip import AipSpeech

pydub.AudioSegment.converter = r'F:\Program Files (x86)\Python36-32\ffmpeg-2\bin\ffmpeg.exe'
# AudioSegment.converter = 'F:/Program Files (x86)/ffmpeg-2/bin/ffmpeg.exe'
# AudioSegment.ffmpeg = r'F:\Program Files (x86)\Python36-32\ffmpeg-2\bin\ffmpeg.exe'
# AudioSegment.ffprobe = r'F:\Program Files (x86)\Python36-32\ffmpeg-2\bin\ffprobe.exe'

# os.remove(r'I:\work\flask\static\src\api\识别结果.txt')
input_filename = r'I:\work\flask\static\src\api\file\RECORDING\200430-163617'

file_name = input_filename + '.mp3'


def sound_cut(file_name, cut_song_num):
    # try:
    #     ss = r'I:\work\flask\static\src\api\file\RECORDING'
    #     # os.chdir(ss)
    #     sound = AudioSegment.from_mp3(r"I:\work\flask\static\src\api\file\RECORDING\xinx.mp3")  # 加载mp3音频
    #     sound = pydub.AudioSegment.from_file(file_name, format='mp3')
    # except Exception as e:
    #     print(e)
    #     return 'Error'
    # # 单位：ms
    # stat_time = 0
    # end_time = 59
    try:
        # for i in range(cut_song_num):
        #     if i == cut_song_num - 1:  # 判断如果是最后一次截断
        #         cut_song = sound[stat_time * 1000:]  # 截取到最后的时间
        #     else:
        #         cut_song = sound[stat_time * 1000:end_time * 1000]
            save_name = file_name  # r"c:/Users/Administrator/Desktop/save/temp-" + str(i + 1) + '.mp3'  # 设置文件保存名称
            save_name_pcm = r'I:\work\flask\static\src\api\txt.pcm'  # 设置文件保存名称
            # cut_song.export(save_name, format="mp3", tags={'artist': '李斯特', 'album': '最爱'})  # 进行切割
            order_ffmpeg = 'ffmpeg -i {} -f s16le -ar 16000 -ac 1 -acodec pcm_s16le {}'.format(save_name, save_name_pcm)
            os.system(order_ffmpeg)  # 使用ffmpeg命令转化mp3为pcm
            context = baidu_Speech_To_Text(save_name_pcm)
            write_text(context)
            # os.remove(save_name)  # 删除mp3文件
            # os.remove(save_name_pcm)
            # 切割完加入下一段的参数
            # stat_time += 59
            # end_time += 59
            
            # print(save_name)
    except Exception as e:
        print(e)


def get_sond_info(file_name):
    song = MediaInfo.parse(file_name)
    # print(song)
    song = song.to_data()['tracks'][0]
    song_length = str(int(float(song['duration'])))  # 读取文件时长
    song_size = str(round(float(int(song['file_size']) / 1024 / 1024), 2)) + 'M'  # 读取文件大小保留两位小数round(变量,2)
    song_filename = song['folder_name']  # 读取文件地址
    song_format_name = song['format']  # 读取文件格式
    try:
        song_name = song['TAG']['title']  # 读取标题
        song_artist = song['TAG']['artist']  # 读取作家
    except:
        song_name = '暂无'
        song_artist = '暂无'
    
    print('歌名：', song_name, '\n作家', song_artist, '\n歌曲长度', song_length, '\n文件大小', song_size, '\n文件路径', song_filename,
          '\n文件格式', song_format_name)
    
    cut_song_num = int(int(song_length) / 59) + 1  # 每段59s，计算切割段数
    print('切割次数', cut_song_num)
    
    return cut_song_num


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def baidu_Speech_To_Text(filePath):  # 百度语音识别
    # path = r'C:\Users\Administrator\Desktop\save'
    # os.chdir(path)
    APP_ID = '16007067'
    API_KEY = 'F4YeOyGqjRfy2ZrdxZO2Y6pi'
    SECRET_KEY = 'CCwgqsTpO6TD3ebMBzzlVZwHg5w4iz26'
    
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)  # 初始化AipSpeech对象
    # 读取文件
    json = aipSpeech.asr(get_file_content(filePath), 'pcm', 16000, {'dev_pid': 1537, })
    print(json['err_msg'])
    context = ''
    if 'success' in json['err_msg']:
        context = json['result'][0]
        print('成功，返回结果为：', context)
    else:
        print('识别失败！')
    return context


def write_text(text):
    # file1 = open(r'C:\Users\Administrator\Desktop\save\识别结果.txt', 'a', encoding='utf-8')
    # file1.write(text)
    # file1.close()
    print(text)


print(file_name)
cut_song_num = get_sond_info(file_name)
sound_cut(file_name, cut_song_num)
# save_name_pcm = r'I:\music\7.pcm'
# cut_song_num = get_sond_info(save_name_pcm)
# with open(save_name_pcm, 'rb') as f:
#     ss = f.read()
# f.close()
# hh = len(ss) // 2  # 长度临界点：1900000
# print(len(ss))
# with open(r'I:\music\7.pcm', 'wb') as f:
#     f.write(ss[:1900000])
#     f.close()
# with open(r'I:\music\8.pcm', 'wb') as f:
#     f.write(ss[1900000:])
#     f.close()
# name_pcm = r'I:\music\7.pcm'
# context = baidu_Speech_To_Text(name_pcm)
# write_text(context)
