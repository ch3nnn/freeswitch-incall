# -*- coding:utf-8 -*-

# Author: ChenTong
# Date: 2021/11/15 10:25

import contextlib
import os
import time
import wave

from loguru import logger
from pydub import AudioSegment

from settings import config


class Frame(object):
    """Represents a "frame" of audio data."""

    def __init__(self, byte, timestamp, duration):
        self.bytes = byte
        self.timestamp = timestamp
        self.duration = duration


class WaveUtils:

    @staticmethod
    def readChunk(f, size):
        """按size大小读取文件"""
        pcmData = f.read(size)
        size = len(pcmData)
        return pcmData, size

    @staticmethod
    def frameGenerator(frameDurationMs, audio, sample_rate=8000):
        """从 PCM 音频数据生成音频帧
        获取所需的帧持续时间（以毫秒为单位）、PCM 数据和采样率。
        Yields 请求持续时间的帧
        """
        n = int(sample_rate * (frameDurationMs / 1000.0) * 2)
        offset = 0
        timestamp = 0.0
        duration = (float(n) / sample_rate) / 2.0
        while offset + n <= len(audio):
            yield Frame(audio[offset:offset + n], timestamp, duration)
            timestamp += duration
            offset += n

    @staticmethod
    def searchQuestionPlay(playFiles: str, playbackVariables="{isNoSound=true}") -> list:
        """查找.wav播放语音文件

        @param playFiles: 模板播放文件
        @param playbackVariables: 特殊播放变量  "{var1=val1,var2=val2}sounds/soundFile.wav"
        """
        playFiles = playFiles if playFiles else ""
        playFiles = list(filter(None, playFiles.split(";")))
        playFiles.reverse()
        playFilesList = []
        for index, pl in enumerate(playFiles):
            if ".wav" in pl:
                filePath = os.path.join(config.TEMPLATE_FILE_PATH, pl)
                if not os.path.exists(filePath):  # 判断语音文件存在
                    logger.error(f"play file not find: {filePath}")
                    raise FileNotFoundError(f"play file not find: {filePath}")
                if os.path.getsize(filePath) == 0:  # 判断语音文件大小
                    raise ValueError(f"play file size 0: {filePath}")
            else:
                pass
                # TODO TTL 文字语音合成
                # filePath = SpeechEngine.tts_play(pl, config.TTS_FILE_PATH + pl)
                # logger.info(f"TTS content is : {pl} TTS engine is: {SpeechEngine.__name__}")
            if index == 0:  # 最后一个录音添加设置特定播放变量 标识当前问题所有语音播放完毕
                filePath = playbackVariables + filePath
            playFilesList.append(filePath)
        return playFilesList

    @staticmethod
    def waitFileCreate(path: str, isChannelHangup: bool):
        """等待freeswitch创建录音文件

        1. 当录音文件存在返回true
        2. 当文件路径不存在会一直等待挂断信号并结束ESLRequestHandler连接

        @param path: 创建录音文件路径
        @param isChannelHangup:  当前通话是否挂断
        @return: bool
        """
        while True:
            if os.path.exists(path if path else ""):
                logger.info(f"freeswitch create record success to open file: {path}")
                return True
            elif isChannelHangup:
                return False
            time.sleep(0.2)
            logger.warning(f"waiting freeswitch create record wave file : {path}")

    @staticmethod
    def writeWave(audioData, wavPath, sampleRate=8000):
        """写入一个.wav文件
        获取路径，PCM音频数据和采样率
        """
        sliceFilePath = wavPath[0:-4] + '_chunk-%002d.wav' % (time.time(),)
        with contextlib.closing(wave.open(sliceFilePath, 'wb')) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sampleRate)
            wf.writeframes(audioData)
        logger.debug(f"sliceFilePath: {sliceFilePath}")
        return sliceFilePath

    @staticmethod
    def splitChunkWave(wavPath, startTime, endTime, chunkNo=0):
        """切割分片wave文件

        :param wavPath: freeswitch创建记录波形文件路径
        :param startTime: 截取开始时间
        :param endTime: 截取结束时间
        :param chunkNo: 分片编号

        :return: 生成分片wave路径
        """
        sound = AudioSegment.from_wav(wavPath)
        # 创建一个静音的音频段  以毫秒为单位截取[begin, end]区间的音频
        cutWav = AudioSegment.silent(duration=1000) + sound[startTime:endTime]
        chunkWavePath = wavPath[0:-4] + '_chunk-%002d.wav' % chunkNo
        cutWav.export(chunkWavePath, format='wav')  # 存储新的wav文件
        return chunkWavePath

    @staticmethod
    def concatWave(*args):
        """将多个wav文件拼接"""
        tmp = [arg for arg in args if arg]
        return ";".join(tmp)
