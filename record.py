# -*-coding:utf-8-*-
# !/usr/bin/python
import pyaudio
import wave
import sys
import time
import librosa.display
import matplotlib.pyplot as plt

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2 ** 11
RECORD_SECONDS = 3

try:
    WAVE_FILE = sys.argv[1]  # ファイル名をコマンドライン引数で指定
except:
    print('File name is required as an argument.')
    sys.exit(1)

audio = pyaudio.PyAudio()
frames = []


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return None, pyaudio.paContinue


# 波形の生成
def make_wave(file_name):
    y, sr = librosa.load(file_name)  # 音声データの読み込み(戻り値はオーディオ時系列,サンプリングレート)

    recording_sound, _ = librosa.effects.trim(y)  # yをの60db以下の値を無音部分とみなしトリミング
    librosa.display.waveplot(recording_sound, sr=sr)

    plt.savefig("wave.png")
    plt.show()


stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=1,

    # これでinput_device_indexの値が取得できる(マイク)
    # import pyaudio  #録音機能を使うためのライブラリ
    #
    # #オーディオデバイスの情報を取得、マイクのインデックス番号を入手する。
    # iAudio = pyaudio.PyAudio()
    # for x in range(0, iAudio.get_device_count()):
    #     print(iAudio.get_device_info_by_index(x))

    frames_per_buffer=CHUNK,
    start=False,
    stream_callback=callback
)

if __name__ == '__main__':
    stream.start_stream()
    time.sleep(RECORD_SECONDS)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(WAVE_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # 波形の生成用メッソドを呼び出し
    make_wave(sys.argv[1])
