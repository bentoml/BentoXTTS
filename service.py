from __future__ import annotations

import os
from pathlib import Path

import torch
from TTS.api import TTS

import bentoml

MODEL_ID = "tts_models/multilingual/multi-dataset/xtts_v2"

sample_input_data = {
    'text': 'It took me quite a long time to develop a voice and now that I have it I am not going to be silent.',
    'language': 'en',
}

@bentoml.service(
    resources={
        "GPU": 1,
        "memory": "8Gi",
    },
    traffic={"timeout": 300},
)
class XTTS:
    
    def __init__(self) -> None:

        self.gpu = True if torch.cuda.is_available() else False
        self.tts = TTS(MODEL_ID, gpu=self.gpu)

    
    @bentoml.api
    def synthesize(
            self,
            context: bentoml.Context,
            text: str = sample_input_data["text"],
            lang: str = sample_input_data["language"],
    ) -> Path:
        output_path = os.path.join(context.directory, "output.wav")
        self.tts.tts_to_file(
            text,
            file_path=output_path,
            speaker_wav='./female.wav',
            language=lang,
            split_sentences=True,
        )

        return Path(output_path)
