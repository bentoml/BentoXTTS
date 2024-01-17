from __future__ import annotations
import bentoml

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

import typing as t
import numpy as np

sample_input_data = {
    'text': 'It took me quite a long time to develop a voice and now that I have it I am not going to be silent.',
    'language': 'en',
}

@bentoml.service(
    resources={"memory": "500MiB"},
    traffic={"timeout": 10},
)
class XTTS:
    model_ref = bentoml.models.get("xtts-model")
    
    def __init__(self) -> None:
        
        self.config = XttsConfig()
        self.config.load_json(self.model_ref.path_of('config.json'))
        self.xtts_model = Xtts.init_from_config(self.config)
        self.xtts_model.load_checkpoint(self.config, checkpoint_dir=self.model_ref.path, eval=True)
        self.xtts_model.cuda()
    
    @bentoml.api
    def synthesize(self, input_data: t.Dict[str, t.Any] = sample_input_data) -> np.ndarray:
        outputs = self.xtts_model.synthesize(
            input_data['text'],
            self.config,
            speaker_wav=self.model_ref.path_of('female.wav'),
            gpt_cond_len=3,
            language=input_data.get('language', 'en'),
        )

        # # Option 1: write ndarray into bytes in the format of a .wav file
        # from scipy.io.wavfile import write
        # import io
        # byte_io = io.BytesIO()
        # write(byte_io, self.config.audio['output_sample_rate'], outputs['wav'])
        # return byte_io

        #  # Option 2: write to a .wav file
        # from scipy.io.wavfile import write
        # import os
        # file_path = os.path.join(context.directory, 'output.wav')
        # write(file_path, self.config.audio['output_sample_rate'], outputs['wav'])

        return outputs['wav']