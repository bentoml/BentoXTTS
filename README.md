<div align="center">
    <h1 align="center">Serving XTTS with BentoML</h1>
</div>

[XTTS](https://huggingface.co/coqui/XTTS-v2) is a voice generation model that lets you clone voices into different languages by using just a quick 6-second audio clip.

This is a BentoML example project, demonstrating how to build a text-to-speech inference API server using the XTTS model. See [here](https://github.com/bentoml/BentoML?tab=readme-ov-file#%EF%B8%8F-what-you-can-build-with-bentoml) for a full list of BentoML example projects.

## Prerequisites

- You have installed Python 3.9+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/latest/get-started/quickstart.html) first.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or the [Python documentation](https://docs.python.org/3/library/venv.html) for details.

## Install dependencies

```bash
git clone https://github.com/bentoml/BentoXTTS.git
cd BentoXTTS
pip install -r requirements.txt
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py`. Run `bentoml serve` in your project directory to start the Service. You may also set the environment variable `COQUI_TTS_AGREED=1` to agree to the terms of Coqui TTS.

```python
$ COQUI_TOS_AGREED=1 bentoml serve .

2024-01-18T11:13:54+0800 [INFO] [cli] Starting production HTTP BentoServer from "service:XTTS" listening on http://localhost:3000 (Press CTRL+C to quit)
/workspace/codes/examples/xtts/venv/lib/python3.10/site-packages/TTS/api.py:70: UserWarning: `gpu` will be deprecated. Please use `tts.to(device)` instead.
  warnings.warn("`gpu` will be deprecated. Please use `tts.to(device)` instead.")
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
```

The server is now active at [http://localhost:3000](http://localhost:3000/). You can interact with it using the Swagger UI or in other different ways.

CURL

```bash
curl -X 'POST' \
  'http://localhost:3000/synthesize' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
  "lang": "en"
}' -o output.wav
```

Python client

This client returns the audio file as a `Path` object. You can use it to access or process the file. See [Clients](https://docs.bentoml.com/en/latest/guides/clients.html) for details.

```python
import bentoml

with bentoml.SyncHTTPClient("http://localhost:3000") as client:
        result = client.synthesize(
            text="It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
            lang="en"
        )
```

For detailed explanations of the Service code, see [XTTS: Text to speech](https://docs.bentoml.com/en/latest/use-cases/audio/xtts.html).

## Deploy to BentoCloud

After the Service is ready, you can deploy the application to BentoCloud for better management and scalability. [Sign up](https://www.bentoml.com/) if you haven't got a BentoCloud account.

Make sure you have [logged in to BentoCloud](https://docs.bentoml.com/en/latest/bentocloud/how-tos/manage-access-token.html), then run the following command to deploy it.

```bash
bentoml deploy .
```

Once the application is up and running on BentoCloud, you can access it via the exposed URL.

**Note**: For custom deployment in your own infrastructure, use [BentoML to generate an OCI-compliant image](https://docs.bentoml.com/en/latest/guides/containerization.html).
