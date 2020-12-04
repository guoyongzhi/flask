from os import system
import sys

# sys.path.append('/home/wbl/Desktop/my-share/rasberry')
from static.aip.mp3_to_char import change_to_chr


def recording():
    system('sudo arecord -Dhw:0,0 -d 5 -f cd -r 44100 -c 2 -t wav test.wav')
    system('ffmpeg -y  -i test.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 test.pcm')
    print(change_to_chr('test.pcm'))


if __name__ == '__main__':
    recording()
