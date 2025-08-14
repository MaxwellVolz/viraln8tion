

## Local LLMs via Docker Compose (WSL + Windows)

This repo uses `docker-compose` to run local LLMs (like **Mistral-7B**) with GPU support in **WSL**. You can control everything via `Docker Desktop`.

---

### How it works

* **Model auto-pulls** on first run via `vllm` and Hugging Face.
* **Compose file** defines the model, port, and GPU access.
* **Docker Desktop GUI** can stop/restart or inspect logs visually.
* **Persistent volume** caching is optional (add if needed).

---

### Wait...What?

A `docker-compose.yml` file defines and launches an LLM container with:

* `vllm/vllm-openai` image (OpenAI-compatible)
* GPU passthrough (`nvidia` runtime)
* Model auto-downloaded from Hugging Face (`HF_TOKEN` optional if public)
* OpenAI-compatible API on `http://localhost:8000/v1`

You’ll see the container in **Docker Desktop → Containers**.

---

### 🚀 Quickstart (WSL)

1. **Set Hugging Face token** (if needed):

```bash
export HF_TOKEN=your_token  # optional if model is public
```

2. **Run the container**:

```bash
docker compose up -d
```

This pulls the model from Hugging Face and starts the API server.

---

### 🔌 Try it out

Make a request from WSL or Windows:

```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mistral-7B-Instruct-v0.1",
    "prompt": "Explain local LLMs in one sentence.",
    "max_tokens": 100
  }'
```

Or use any OpenAI-compatible client (e.g. Postman, Python, VSCode plugins).

---


---

Want a `Makefile`, `.env`, or scripts next?
