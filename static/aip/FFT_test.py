from tkinter import *
import wave
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import numpy as np


def read_wave_data(file_path):
    # open a wave file, and return a Wave_read object
    f = wave.open(file_path, "rb")
    # read the wave's format infomation,and return a tuple
    params = f.getparams()
    # get the info
    nchannels, sampwidth, framerate, nframes = params[:4]
    # Reads and returns nframes of audio, as a string of bytes.
    str_data = f.readframes(nframes)
    # close the stream
    f.close()
    # turn the wave's data to array
    wave_data = np.fromstring(str_data, dtype=np.short)
    # for the data is stereo,and format is LRLRLR...
    # shape the array to n*2(-1 means fit the y coordinate)
    wave_data.shape = -1, 2
    # transpose the data
    wave_data = wave_data.T
    # calculate the time bar
    time = np.arange(0, nframes) * (1.0 / framerate)
    return wave_data, time


def data_fft(data, time, time_start, time_end):
    # 短时fft。截取一段时间内的数据先
    # time_start是开始时间，time_end是结束时间
    t = []
    y = []
    count = 0
    # for i in time:
    for i in range(time.size):
        if ((time[i] >= time_start) & (time[i] <= time_end)):
            count = count + 1
            t = np.append(t, time[i])
            # y = np.append(y, data[:, 0])
            y = np.append(y, data[0][i])  # 只提取左声道
    # print (count)
    
    yy = fft(y)  # 快速傅里叶变换
    yreal = yy.real  # 获取实数部分
    yimag = yy.imag  # 获取虚数部分
    
    yf = abs(fft(y))  # 取绝对值
    yf1 = abs(fft(y)) / len(t)  # 归一化处理
    yf2 = yf1[range(int(len(t) / 2))]  # 由于对称性，只取一半区间
    
    xf = np.arange(len(y))  # 频率
    xf1 = xf
    xf2 = xf[range(int(len(t) / 2))]  # 取一半区间
    
    plt.figure()
    
    plt.subplot(221)
    plt.plot(t, y)
    plt.title('Original wave')
    
    plt.subplot(222)
    plt.plot(xf, yf, 'r')
    plt.title('FFT of Mixed wave(two sides frequency range)', fontsize=7, color='#7A378B')  # 注意这里的颜色可以查询颜色代码表
    
    plt.subplot(223)
    plt.plot(xf1, yf1, 'g')
    plt.title('FFT of Mixed wave(normalization)', fontsize=9, color='r')
    
    plt.subplot(224)
    plt.plot(xf2, yf2, 'b')
    plt.title('FFT of Mixed wave)', fontsize=10, color='#F08080')
    
    plt.show()


def main():
    wave_data, time = read_wave_data('爱上法宣在-迅捷文字转语音.wav')
    print(wave_data, time)
    data_fft(wave_data, time, 1, 2)
    plt.figure()
    # draw the wave
    plt.subplot(211)
    plt.plot(time, wave_data[0])
    plt.subplot(212)
    plt.plot(time, wave_data[1], c="g")
    plt.show()


if __name__ == "__main__":
    main()
