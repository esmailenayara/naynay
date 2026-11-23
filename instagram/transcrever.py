"""Transcreve a fala de um vídeo com o tempo de cada palavra.

Uso:  python3 -I transcrever.py audio.wav ["vocabulário opcional"] > palavras.json
(o vocabulário ajuda a acertar nomes e termos, ex.: "Método NE Face, Carla, Juliana, ml")
(o áudio deve ser WAV mono 16 kHz: ffmpeg -i video.mp4 -vn -ac 1 -ar 16000 audio.wav)
Precisa de:  pip install faster-whisper
O WAV é lido com numpy de propósito: o faster-whisper novo falha ao abrir arquivos
direto com a versão do PyAV instalada neste ambiente.
"""
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel

w = wave.open(sys.argv[1])
audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
modelo = WhisperModel("small", device="cpu", compute_type="int8")
dica = sys.argv[2] if len(sys.argv) > 2 else None
trechos, _ = modelo.transcribe(audio, language="pt", word_timestamps=True, initial_prompt=dica)
palavras = [{"ini": round(p.start, 2), "fim": round(p.end, 2), "texto": p.word.strip()}
            for t in trechos for p in t.words]
json.dump(palavras, sys.stdout, ensure_ascii=False, indent=1)
