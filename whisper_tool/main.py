import whisper 
import os
import numpy as np
try:
    import tensorflow  # required in Colab to avoid protobuf compatibility issues
except ImportError:
    pass

import torch
import pandas as pd
import whisper
import torchaudio
import streamlit as st

from tqdm.notebook import tqdm

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class LibriSpeech(torch.utils.data.Dataset):
    """
    A simple class to wrap LibriSpeech and trim/pad the audio to 30 seconds.
    It will drop the last few seconds of a very small portion of the utterances.
    """
    def __init__(self, split="test-clean", device=DEVICE):
        self.dataset = torchaudio.datasets.LIBRISPEECH(
            root=os.path.expanduser("~/.cache"),
            url=split,
            download=True,
        )
        self.device = device

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        audio, sample_rate, text, _, _, _ = self.dataset[item]
        assert sample_rate == 16000
        audio = whisper.pad_or_trim(audio.flatten()).to(self.device)
        mel = whisper.log_mel_spectrogram(audio)
        
        return (mel, text)

dataset = LibriSpeech("test-clean")
loader = torch.utils.data.DataLoader(dataset, batch_size=16)

st.title('Carga de archivos de audio')

#Cargar audio
uploaded_file = st.file_uploader("Carga un archivo de audio", type="mp3")
if uploaded_file is not None:
    st.warning("Waiting for file to be uploaded and processed...")
    audio_whisper = whisper.load_audio(uploaded_file)
    model = whisper.load_model("base")
    result = model.transcribe(audio_whisper)
    transcripcion = result["text"]

    #obtener la ruta del archivo cargado
    ruta = uploaded_file.name
    f = open(ruta,"w+")
    text_file = open(ruta,"w")

    #write string to file
    text_file.write(transcripcion)

    #close file
    text_file.close()

    #Descargar el archivo
    st.download_button(
        label="Descargar transcripción",
        data=text_file,
        file_name= ruta+'.txt',
        mime='text/plain')
else: 
    st.warning("No file uploaded")