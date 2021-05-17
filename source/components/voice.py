import struct
from pyaudio import *
pa = PyAudio()
SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
stream = pa.open(format=paInt16, channels=1,
                 rate=SAMPLING_RATE, input=True, frames_per_buffer=1000)


def getVolumn():
    """玩家麦克风音量获取"""
    string_audio_data = stream.read(1000)
    volumn = max(struct.unpack('1000h', string_audio_data))
    return volumn
