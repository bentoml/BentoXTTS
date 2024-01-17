import bentoml
from huggingface_hub import hf_hub_download
import shutil
import os 

model= "coqui/XTTS-v2"

with bentoml.models.create(
    name='xtts-model',
) as model_ref:
    hf_hub_download(model, 'model.pth', local_dir=model_ref.path)
    hf_hub_download(model, 'hash.md5', local_dir=model_ref.path)
    hf_hub_download(model, 'config.json', local_dir=model_ref.path)
    hf_hub_download(model, 'vocab.json', local_dir=model_ref.path)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    shutil.copyfile(os.path.join(dir_path, 'female.wav'), model_ref.path_of('female.wav'))

    print(f"Model saved: {model_ref}")
