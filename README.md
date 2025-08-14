# autom8n

Automated viral video pipeline using n8n and DeepSeek 3.1 with free TTS, captions, music, and publishing.

## Overview

`autom8n` automates the creation and publishing of shortform video content. Using n8n as the orchestrator and `DeepSeek 3.1` to write scripts, the pipeline generates voiceovers, visuals, captions, and music — and can even auto-upload.

## Features

- Script generation using DeepSeek 3.1
- Text-to-speech with local TTS engines (e.g., Piper, Bark, Coqui)
- Automatic captioning using Whisper or WhisperX
- Background music via free audio sources or generated loops
- Video rendering with FFmpeg or Auto-Editor
- Optional uploading/posting to TikTok, YouTube Shorts, etc.
- 100% free and unlimited with self-hosted components

## Architecture

1. **Trigger**: Scheduled or event-driven n8n workflow
2. **Script Generation**: DeepSeek call to generate a short, viral script
3. **TTS**: Convert script to audio using a local TTS engine
4. **Music**: Add royalty-free or auto-generated background music
5. **Captioning**: Generate subtitle timing and overlay with Whisper
6. **Rendering**: Merge visuals, audio, and captions using FFmpeg
7. **Publishing**: Upload via APIs or headless browser automation

## Requirements

- Node.js
- Docker (optional, for Whisper or n8n)
- Python (for Whisper/WhisperX)
- n8n (self-hosted or desktop)
- DeepSeek 3.1 (local model or API)
- FFmpeg
- A local TTS engine (Piper recommended)

## Prereq's

1. Docker Desktop
2. [Github](https://github.com/apps/desktop)
3. **Optional** [NodeJS](https://nodejs.org/en/download) 


## Setup

1. Clone the repo:

```bash
git clone https://github.com/maxwellvolz/viraln8tion.git
cd viraln8tion
```

### Run Services in Docker Containers

| Service          | Purpose         | Access                                             |
| ---------------- | --------------- | -------------------------------------------------- |
| n8n              | Automation Tool | [Console](http://localhost:5678/setup)             |
| MiniIO           | Object Storage  | admin :: password123 [console](http://minnio:9001) |
| Kokoro TTS       | Text-to-Speech  | [Console](http://localhost:8880/web)               |
| Baserow          | Database UI     | [Console](http://host.docker.internal:85)          |
| Stable Diffusion | Free Image Gen  | [Console](http://host.docker.internal:7860)        |

MiniIO
http://host.docker.internal:9001
Kokoro TTS

NCA Toolkit
http://host.docker.internal:8080


Run all 4 of these in separate Terminals (cuz they take a while):

```sh
# n8n
docker run -d --name n8n -p 5678:5678 -e WEBHOOK_URL=http://host.docker.internal:5678 -e N8N_DEFAULT_BINARY_DATA_MODE=filesystem -v C:\Docker\n8n-data:/home/node/.n8n docker.n8n.io/n8nio/n8n

# miniIO
docker run -p 9000:9000 -p 9001:9001 --name miniio -v C:\Docker\minio-data:/data -e MINIO_ROOT_USER=admin -e MINIO_ROOT_PASSWORD=password123 quay.io/minio/minio:RELEASE.2025-04-22T22-12-26Z server /data --console-address ":9001"

# Kokoro TTS
docker run -d --gpus all -p 8880:8880 --name kokoro-tts ghcr.io/remsky/kokoro-fastapi-gpu:v0.2.2

# Only if ur hardware sucks - Kokoro TTS CPU Edition
docker run -p 8880:8880 --name kokoro-tts-cpu ghcr.io/remsky/kokoro-fastapi-cpu:v0.2.2

# Baserow
docker run -d --name baserow -e BASEROW_PUBLIC_URL=http://host.docker.internal:85 -v C:\Docker\baserow-data:/baserow/data -p 85:80 -p 443:443 --restart unless-stopped --shm-size=256mb baserow/baserow:1.32.5
```

> Activate n8n key - from email


### Verify Setups

Check `Docker Desktop` or the `Consoles` listed above.

1. [n8n](http://localhost:5678)
   1. Make Account
2. [MiniIO](http://localhost:9001/browser)
   1. Make Account
   2. Make Database `nca-toolkit`
   3. Generate Access and Secret Keys using the default root credentials
   4. Save these for later
3. [Kokoro](http://localhost:8880/web)
4. [Baserow](http://host.docker.internal:85/)
   1. Create Workspace
   2. Create Database `TikTok`
      1. Add Tables `Videos` and `Scenes`

#### Database Table Setup - EZ Mode

1. Save a .csv
2. Import as View for `Videos` and `Scenes`

Videos
```csv
id,Title,Description,Script,Final Video URL,Video + Captions URL,Video + Audio URL,Raw Video URL,TTS Audio,TTS Voice,Scenes,Captions URL,Generative Style,Initial Prompt,Status,Image Provider
1,,,,,,,,,,,,,,,
```

Scenes
```csv
id,Record ID,Prompt,Duration,Image,Video Clip URL,Videos,Image Provider
1,1,,0.00,,,,
```

### Install NCA Toolkit

| Service     | Purpose           | Access  |
| ----------- | ----------------- | ------- |
| NCA Toolkit | Video Editing API | Console |

Usage:
- images to videos
- combine clips
- transcribe clips

Replace `your_access_key` and `your_secret_key` with the values from MiniIO:

```sh
docker run -d -p 8080:8080 --name nca-toolkit -e API_KEY=thekey -e S3_ENDPOINT_URL=http://host.docker.internal:9000 -e S3_ACCESS_KEY=your_access_key -e S3_SECRET_KEY=your_secret_key -e S3_BUCKET_NAME=nca-toolkit -e S3_REGION=None stephengpope/no-code-architects-toolkit:latest
```

---

## OpenRouter 

1. [Make Account](https://openrouter.ai/)
2. Copy Api Key
3. Add to [n8n](http://localhost:5678/home/credentials)


---

## n8n Automation

1. Import [JSON](https://drive.google.com/file/d/1EGCWHhfXQ_k4krF29rFgktrdzOwvqPY7)
2. Duplicate
3. Disconnect all but first lane
4. Double-click `On form submission` and open the `Test URL`


http://host.docker.internal:85/api-docs/database/163

then Settings

amazing facts about linus torvalds


## n8n Setup

### Node -> HTTP Request

- Method: Post
- Auth: None
- Send Headers: True
  - Name: Authorization
  - Value: Token enter_your_baserow_api_token
- Send Body: True
  - Name: Title, Value: {value}


## Rate Limited? Local LLM Setup

### Prereq's

- Python
- 

Make `/local_llm/.env` with: `HF_TOKEN=your_huggingface_key`

### Setup

```sh
cd local_llm
.venv\Scripts\activate
pip install -r requirements.txt
```
### Run it

```sh
cd local_llm
make tinyllama          # Spin up tinyllama on port 8000
make tinyllama-down     # Stop tinyllama container
make deepseekcode       # Spin up DeepSeekCode on port 8000
make deepseekcode-down  # Stop DeepSeekCode container
make mistral            # Spin up Mistral 7B on port 8000
make mistral-down       # Stop Mistral container
make stop-all           # Kill all running containers
```

## Postman - Test LLM Endpoint

- Type: POST
- URL: http://localhost:8000/v1/chat/completions

Headers

- Authorization | Bearer Test
- Content-Type  | application/json

Body

Model Names: `deepseek-ai/deepseek-coder-1.3b-instruct`, `mistralai/Mistral-7B-Instruct-v0.1`, `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

raw:

```json
{  
   "model": "deepseek-ai/deepseek-coder-1.3b-instruct",  
   "messages": 
   [    
      {      
      "role": "user",      
      "content": "solve the fibonacci sequence with python using a list comp"    
      }  
   ]
}
```


## Youtube Credentials

To **automate posting to YouTube using n8n**, you need to use the **YouTube node** (which uses the YouTube Data API v3). Here's a full setup that lets you upload videos programmatically.

---

## ✅ Requirements

1. **Google Cloud project**
2. **YouTube Data API v3 enabled**
3. **OAuth2 credentials**
4. **n8n YouTube node configured**

---

## 🔧 Setup Guide

### 1. **Create OAuth Credentials**

* Go to: [https://console.cloud.google.com/](https://console.cloud.google.com/)
* Create a project or use existing one.
* Enable **YouTube Data API v3**
* Go to **APIs & Services → Credentials**


Thanks — that screenshot confirms you're using an **OAuth Client for “Desktop App”**, not for “Web App”.

### 🔥 Problem:

**Desktop App clients do not support redirect URI configuration** — that’s why you don’t see that option.

### 🔧 Fix:

You need to create a **new OAuth 2.0 Client ID of type “Web Application”**, which allows setting redirect URIs.

---

## ✅ Correct Steps:

1. In **Google Cloud → Credentials**
2. Click **Create Credentials → OAuth Client ID**
3. Choose:

   ```
   Application Type: Web application
   ```
4. Set name: `n8n YouTube Uploader`
5. Add **Authorized Redirect URI**:

   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```
6. Save. You’ll get a new **Client ID** and **Client Secret**.

---

## 🔁 Then in n8n:

1. Go to **Credentials → New → YouTube OAuth2**
2. Use the new Web Client ID + Secret
3. It will now **redirect correctly** and allow you to sign in

---



## Stable Diffusion Locally


### Pre-reqs

```sh
mkdir models outputs
```


### 

docker-compose.yml

```yml
services:
   ...
  stable-diffusion:
    image: siutin/stable-diffusion-webui-docker:latest-cuda-12.1.1
    container_name: sd
    command: ["bash", "webui.sh", "--api", "--listen"]
    ports:
      - "7860:7860"
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    volumes:
      - ./models:/app/stable-diffusion-webui/models
      - ./outputs:/app/stable-diffusion-webui/outputs
    restart: unless-stopped
```


### Run Service

```sh
docker compose up -d stable-diffusion
# wait 2 minutes
```

### Test Image

> Note: Stable Diffusion WebUI API (AUTOMATIC1111-based) returns a base64-encoded PNG, not a raw image file.
> We can convert to a `.png` to view the result.

```sh
curl http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cyberpunk-styled close-up of a grieving parent'\''s hands cradling a jar filled with dirt instead of ashes, illuminated by a flickering neon sign outside a dimly lit funeral home. The jar reflects eerie blue and purple hues, casting long shadows on the teardrop-streaked face in the background.",
    "negative_prompt": "blurry, ugly, deformed, bad anatomy, low quality, abstract, cropped, out of frame, messy, bad lighting, text, watermark, distorted, wrong perspective",
    "steps": 20,
    "width": 576,
    "height": 1024
  }' | jq -r '.images[0]' | base64 -d > result.png
```

### Upgrade to `SD-XL` model

[Download](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors)

Place in /models


```sh
curl http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "sd_model_checkpoint": "sdxl_base_1.0.safetensors",
    "prompt": "A cyberpunk-styled close-up of a grieving parent'\''s hands cradling a jar filled with dirt instead of ashes, illuminated by a flickering neon sign outside a dimly lit funeral home. The jar reflects eerie blue and purple hues, casting long shadows on the teardrop-streaked face in the background.",
    "negative_prompt": "blurry, ugly, deformed, bad anatomy, low quality, abstract, cropped, out of frame, messy, bad lighting, text, watermark, distorted, wrong perspective",
    "steps": 20,
    "width": 576,
    "height": 1024
  }' | jq -r '.images[0]' | base64 -d > result.png
```


### Add LoRA Models

[Download from here](https://civitai.com/models/312530?modelVersionId=1962475)


## Test Subjects - HN

[Dynamic Programming](https://news.ycombinator.com/item?id=44603349)