from comtypes.client import CreateObject
import comtypes.client
import time

try:
    from comtypes.gen import SpeechLib  # comtypes
    engine = CreateObject("SAPI.SpVoice")
    stream = CreateObject("SAPI.SpFileStream")
except ImportError:
    # Generate the SpeechLib lib and any associated files
    engine = comtypes.client.CreateObject("SAPI.SpVoice")
    stream = comtypes.client.CreateObject("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib


def char_to_wav(theText='你说什么呢?'):
    """
    利用原生语音合成
    :param theText:
    :return:
    """
    filename = str(int(time.time()))
    outfile = filename + "-audio.wav"
    stream.Open(outfile, SpeechLib.SSFMCreateForWrite)
    engine.AudioOutputStream = stream
    # theText = '你说什么呢'
    engine.speak(theText)
    stream.Close()
    return outfile


if __name__ == '__main__':
    char_to_wav()
