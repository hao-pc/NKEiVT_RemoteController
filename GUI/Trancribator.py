import wave
from pathlib import Path
from typing import Tuple
import sys
import numpy as np
import sherpa_onnx
from pydub import AudioSegment

class Trancribator:
    # def __init__(self):
    #     self.recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
    #             encoder="am/encoder.onnx",
    #             decoder="am/decoder.onnx",
    #             joiner="am/joiner.onnx",
    #             tokens="lang/tokens.txt",
    #             num_threads=4,
    #             sample_rate=16000,
    #             decoding_method="greedy_search")
    
    def __init__(self):
        self.recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
                encoder=r"am\encoder.onnx",
                decoder=r"am\decoder.onnx",
                joiner=r"am\joiner.onnx",
                tokens=r"lang\tokens.txt",
                num_threads=4,
                sample_rate=16000,
                decoding_method="greedy_search")
    
    
    def read_wave(self, wave_filename: str) -> Tuple[np.ndarray, int]:
        with wave.open(wave_filename) as f:
            assert f.getnchannels() == 1, f.getnchannels()
            assert f.getsampwidth() == 2, f.getsampwidth()
            num_samples = f.getnframes()
            samples = f.readframes(num_samples)
            samples_int16 = np.frombuffer(samples, dtype=np.int16)
            samples_float32 = samples_int16.astype(np.float32)
            samples_float32 = samples_float32 / 32768
            return samples_float32, f.getframerate()
    def check_format(self, filename):
        if filename[-3:] == "mp3":
            sound = AudioSegment.from_mp3(filename)
            sound.export(filename.replace("mp3", "wav"), format="wav")
            return filename.replace("mp3", "wav")
        else:
            return filename
    def predict(self, filename: str) -> str:
        filename = self.check_format(filename)
        samples, sample_rate = self.read_wave(filename)
        s = self.recognizer.create_stream()
        s.accept_waveform(sample_rate, samples)
        self.recognizer.decode_stream(s)
        return s.result.text

