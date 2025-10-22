# viraln8tion

Automated viral video pipeline using n8n and AI models with free TTS, captions, music, and publishing.

## Overview

**viraln8tion** automates the creation and publishing of short-form video content. Using n8n as the orchestrator and AI models (DeepSeek, local LLMs) to write scripts, the pipeline generates voiceovers, visuals, captions, and music — and can even auto-upload to social platforms.

## Features

- Script generation using DeepSeek 3.1 or local LLMs
- Text-to-speech with Kokoro TTS (GPU or CPU)
- Automatic captioning using Whisper/WhisperX
- Background music via free audio sources or generated loops
- Video rendering with FFmpeg or Auto-Editor
- Optional uploading to TikTok, YouTube Shorts, etc.
- 100% free and unlimited with self-hosted components
- Local image generation with Stable Diffusion

## Architecture

1. **Trigger**: Scheduled or event-driven n8n workflow
2. **Script Generation**: AI call to generate a short, viral script
3. **TTS**: Convert script to audio using Kokoro TTS
4. **Music**: Add royalty-free or auto-generated background music
5. **Captioning**: Generate subtitle timing and overlay
6. **Rendering**: Merge visuals, audio, and captions using FFmpeg
7. **Publishing**: Upload via APIs or automation

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://github.com/apps/desktop) or Git CLI
- GPU recommended for Stable Diffusion and Kokoro TTS (CPU versions available)
- Optional: [Node.js](https://nodejs.org/en/download) for local development

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/maxwellvolz/viraln8tion.git
cd viraln8tion
```

### 2. Configure Environment

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Services with Docker Compose

```bash
docker compose up -d
```

This will start all services defined in `docker-compose.yml`:
- n8n (automation)
- MinIO (object storage)
- Kokoro TTS (text-to-speech)
- Baserow (database)
- NCA Toolkit (video editing API)

Wait 2-3 minutes for services to fully initialize.

## Service Access

| Service          | Purpose            | URL                                    | Default Credentials   |
| ---------------- | ------------------ | -------------------------------------- | --------------------- |
| n8n              | Automation Tool    | http://localhost:5678                  | Create on first visit |
| MinIO            | Object Storage     | http://localhost:9001                  | admin / password123   |
| Kokoro TTS       | Text-to-Speech     | http://localhost:8880/web              | N/A                   |
| Baserow          | Database UI        | http://localhost:85                    | Create on first visit |
| NCA Toolkit      | Video Editing API  | http://localhost:8080                  | N/A                   |
| Stable Diffusion | Image Generation   | http://localhost:7860 (if configured)  | N/A                   |

## Initial Setup

### MinIO Configuration

1. Open http://localhost:9001
2. Login with `admin` / `password123`
3. Create a bucket named `nca-toolkit`
4. Generate Access and Secret Keys:
   - Navigate to **Access Keys** → **Create access key**
   - Save both keys for later use
5. Update your `.env` file with these keys

### Baserow Database Setup

1. Open http://localhost:85
2. Create a new workspace
3. Create a database named `TikTok`
4. Import the following tables:

**Videos Table** (`Videos.csv`):
```csv
id,Title,Description,Script,Final Video URL,Video + Captions URL,Video + Audio URL,Raw Video URL,TTS Audio,TTS Voice,Scenes,Captions URL,Generative Style,Initial Prompt,Status,Image Provider
1,,,,,,,,,,,,,,,
```

**Scenes Table** (`Scenes.csv`):
```csv
id,Record ID,Prompt,Duration,Image,Video Clip URL,Videos,Image Provider
1,1,,0.00,,,,
```

### n8n Configuration

1. Open http://localhost:5678
2. Create an account
3. Import the workflow JSON (link in n8n folder or documentation)
4. Configure credentials:
   - OpenRouter API (for AI models)
   - Baserow API token
   - MinIO credentials

#### n8n HTTP Request Node Setup

For Baserow integration:
- Method: POST
- Auth: None
- Headers:
  - Name: `Authorization`
  - Value: `Token YOUR_BASEROW_API_TOKEN`
- Body: JSON with required fields

## API Configuration

### OpenRouter

1. Create account at [OpenRouter](https://openrouter.ai/)
2. Copy your API key
3. Add to n8n credentials

### YouTube Upload (Optional)

To enable automated YouTube uploads:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials:
   - Application Type: **Web application**
   - Authorized redirect URI: `http://localhost:5678/rest/oauth2-credential/callback`
5. Copy Client ID and Client Secret to n8n credentials

## Local LLM Setup (Optional)

If you want to avoid API rate limits, run models locally:

### Prerequisites

- Python 3.8+
- Create `local_llm/.env` with: `HF_TOKEN=your_huggingface_token`

### Installation

```bash
cd local_llm
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running Models

Use the included Makefile:

```bash
make tinyllama          # TinyLlama on port 8000
make deepseekcode       # DeepSeek Coder on port 8000
make mistral            # Mistral 7B on port 8000
make stop-all           # Stop all containers
```

### Testing Local LLM

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer test" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/deepseek-coder-1.3b-instruct",
    "messages": [
      {
        "role": "user",
        "content": "Write a short viral video script about AI"
      }
    ]
  }'
```

## Stable Diffusion (Optional)

### Setup

Uncomment the `stable-diffusion` service in `docker-compose.yml`:

```bash
docker compose up -d stable-diffusion
# Wait 2-3 minutes for initialization
```

### Download Models

1. Download [SD-XL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors)
2. Place in `./models` directory

### Test Image Generation

```bash
curl http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "sd_model_checkpoint": "sd_xl_base_1.0.safetensors",
    "prompt": "A cyberpunk city at night, neon lights, ultra detailed",
    "negative_prompt": "blurry, ugly, low quality",
    "steps": 20,
    "width": 576,
    "height": 1024
  }' | jq -r '.images[0]' | base64 -d > result.png
```

## Project Structure

```
viraln8tion/
├── docker-compose.yml      # Service orchestration
├── .env.example            # Environment template
├── docker-data/            # Persistent data (gitignored)
├── local_llm/              # Local LLM setup
├── models/                 # Model files (gitignored)
├── outputs/                # Generated files (gitignored)
├── n8n/                    # n8n workflows
├── stable_diffusion/       # SD configuration
└── README.md               # This file
```

## Troubleshooting

### Services won't start
- Ensure Docker Desktop is running
- Check port conflicts: `docker ps`
- Review logs: `docker compose logs [service_name]`

### GPU not detected
- Ensure NVIDIA drivers are installed
- Install [nvidia-docker2](https://github.com/NVIDIA/nvidia-docker)
- Uncomment GPU sections in `docker-compose.yml`

### Out of memory
- Increase Docker memory allocation in Docker Desktop settings
- Use CPU versions of services instead of GPU

## Contributing

Contributions welcome! Please open an issue or PR.

## License

MIT

## Acknowledgments

- [n8n](https://n8n.io/) - Workflow automation
- [Kokoro TTS](https://github.com/remsky/kokoro-fastapi) - Text-to-speech
- [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui) - Image generation
- [NCA Toolkit](https://github.com/stephengpope/no-code-architects-toolkit) - Video processing
