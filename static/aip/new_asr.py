from aip import AipSpeech
import os
from uuid import uuid4
from wav2pcm import wav_to_pcm

APP_ID = '14452531'
API_KEY = 'zdU6ldOh7CeQvFFzw9GWhwZr'
SECRET_KEY = 'h5eVzR2G4EPFf78uzceC1zHL6Qj88RCY'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# client.setConnectionTimeoutInMillis(5000)  # 建立连接的超时时间（单位：毫秒)
# client.setSocketTimeoutInMillis(10000)  # 通过打开的连接传输数据的超时时间（单位：毫秒）
# 语音合成
def new_synthesis(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,  # 音量，取值0-15，默认为5中音量
        'spd': 5,  # 语速，取值0-9，默认为5中语速
        'pit': 5,  # 音调，取值0-9，默认为5中语调
        'per': 4  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    })
    audio_file_path = str(uuid4()) + ".mp3"
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(audio_file_path, 'wb') as f:
            f.write(result)
    return audio_file_path


# 读取文件
def get_file_content(pcm_file_path):
    with open(pcm_file_path, 'rb') as fp:
        return fp.read()


# 语音识别
def new_asr(filePath):
    # 将录音机文件wma转换成pcm
    pcm_file_path = wav_to_pcm(filePath)

    # 识别本地文件
    res = client.asr(get_file_content(pcm_file_path), 'pcm', 16000, {
        'dev_pid': 1536,
    })
    try:
        text = res.get('result')[0]
    except Exception as e:
        text = "对不起,没有听清你说的啥,请再说一遍。"
    os.remove(pcm_file_path)
    return text


if __name__ == '__main__':
    new_asr('audio.wma')