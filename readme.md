## qc_notebooklm

implement a notebooklm 

## pre:

0. create .env by .env.example

1. set up huggingface and get token from it, set HF_TOKEN in .env, exactly, you need to set base_url and api key

2. add ffmpeg on macos or windows

3. pip install poetry   


## run:
```

poetry shell

poetry install

peotry run python podcast_batch.py

```