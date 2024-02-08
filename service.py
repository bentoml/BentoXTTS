from __future__ import annotations

import os
import typing as t
from pathlib import Path

import bentoml

MODEL_ID = "tts_models/multilingual/multi-dataset/xtts_v2"

sample_input_data = {
    'text': 'It took me quite a long time to develop a voice and now that I have it I am not going to be silent.',
    'language': 'en',
}

@bentoml.service(
    resources={
        "gpu": 1,
        "memory": "8Gi",
    },
    traffic={"timeout": 300},
)
class XTTS:
    def __init__(self) -> None:
        import torch
        from TTS.api import TTS

        self.tts = TTS(MODEL_ID, gpu=torch.cuda.is_available())
    
    @bentoml.api
    def synthesize(
            self,
            context: bentoml.Context,
            text: str = sample_input_data["text"],
            lang: str = sample_input_data["language"],
    ) -> t.Annotated[Path, bentoml.validators.ContentType('audio/*')]:
        output_path = os.path.join(context.temp_dir, "output.wav")
        sample_path = "./female.wav"
        if not os.path.exists(sample_path):
            sample_path = "./src/female.wav"

        self.tts.tts_to_file(
            text,
            file_path=output_path,
            speaker_wav=sample_path,
            language=lang,
            split_sentences=True,
        )
        return Path(output_path)
