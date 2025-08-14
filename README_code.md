


##  Outline

```sh
LLM generates Python code
↓
Save to example.py
↓
Fake typing into headless (nvim / terminal) using pty or expect script
↓
Record session with asciinema (→ .cast)
↓
Render as SVG or video (via svg-term-cli → ffmpeg or moviepy)
↓
Final video asset
```

## Testing Manually



## Setup

```sh

# make a .venv
python -m venv .venv
source .venv/bin/activate

asciinema play counter.cast

sudo apt install ffmpeg 

agg counter.cast counter.gif

sudo add-apt-repository ppa:neovim-ppa/unstable
sudo apt update
sudo apt install neovim

sudo npm install -g pyright

```

## Generate


```sh
python record_nvim.py && agg counter.cast counter.gif && ffmpeg -i counter.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" counter.mp4
```


## Automation

### Python with FastAPI Endpoints

```
source .venv/bin/activate
cd code_bot
uvicorn fastapi_scripter:app --host 0.0.0.0 --port 8000
```



## Backlog Notes

### For Typescript **remotion** is an insanely good solution

```sh
npx remotion render scripts/MyVideo out.mp4
```
