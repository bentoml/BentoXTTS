This document demonstrates how to build an text-to-speech application using BentoML, powered by [XTTS](https://huggingface.co/coqui/XTTS-v2).

## **Prerequisites**

- You have installed Python 3.8+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/latest/get-started/quickstart.html) first.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See Installation for details.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py`. Run `bentoml serve` in your project directory to start the Service. You may also set environment variable `COQUI_TOS_AGREED` to 1 to accept coqui's TOS.

```python
$ COQUI_TOS_AGREED=1 bentoml serve .

2024-01-18T11:13:54+0800 [INFO] [cli] Starting production HTTP BentoServer from "service:XTTS" listening on http://localhost:3000 (Press CTRL+C to quit)
/workspace/codes/examples/xtts/venv/lib/python3.10/site-packages/TTS/api.py:70: UserWarning: `gpu` will be deprecated. Please use `tts.to(device)` instead.
  warnings.warn("`gpu` will be deprecated. Please use `tts.to(device)` instead.")
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
 > Using model: xtts
```

The server is now active at [http://0.0.0.0:3000](http://0.0.0.0:3000/). You can interact with it using Swagger UI or in other different ways.

CURL

```bash
curl -X 'POST' \
  'http://0.0.0.0:3000/synthesize' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
  "lang": "en"
}' -o output.wav
```

## Deploy the application to BentoCloud

After the Service is ready, you can deploy the application to BentoCloud for better management and scalability. A configuration YAML file (`bentofile.yaml`) is used to define the build options for your application. It is used for packaging your application into a Bento. See [Bento build options](https://docs.bentoml.com/en/latest/concepts/bento.html#bento-build-options) to learn more.

Make sure you have logged in to BentoCloud, then run the following command in your project directory to deploy the application to BentoCloud. Under the hood, this commands automatically builds a Bento, push the Bento to BentoCloud, and deploy it on BentoCloud.

```bash
bentoml deploy .
```

**Note**: Alternatively, you can manually build the Bento, containerize the Bento as a Docker image, and deploy it in any Docker-compatible environment. See [Docker deployment](https://docs.bentoml.org/en/latest/concepts/deploy.html#docker) for details.

Once the application is up and running on BentoCloud, you can access it via the exposed URL.
