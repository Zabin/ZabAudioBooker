# ZabAudioBooker

Offline AI text-to-speech in Python, powered by [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
(82M parameters, Apache-2.0). Runs fully offline once the weights are cached and
takes advantage of an NVIDIA GPU (developed against an RTX 4050) with a clean
CPU fallback.

## Features

- Single-file CLI — text file or stdin in, WAV or MP3 out.
- Auto device selection: uses CUDA if available, otherwise CPU.
- Streaming progress with per-chunk real-time-factor (RTF) readout.
- Multilingual front-end: English (US/GB), Spanish, French, Italian, Portuguese (BR), Hindi, Japanese, Mandarin.
- Adjustable speech speed and a large library of bundled voices — no voice cloning, no internet calls.

## Requirements

- Python 3.10+
- An NVIDIA GPU with CUDA 12.x (optional; CPU works too)
- `espeak-ng` — used by Kokoro's text frontend for phoneme fallback
- `ffmpeg` — only needed for MP3 output

### System packages

```bash
# Debian / Ubuntu
sudo apt install espeak-ng ffmpeg

# Arch
sudo pacman -S espeak-ng ffmpeg

# macOS (Homebrew)
brew install espeak-ng ffmpeg

# Windows
#   espeak-ng:  https://github.com/espeak-ng/espeak-ng/releases
#   ffmpeg:     https://www.gyan.dev/ffmpeg/builds/
```

### Python install

Install PyTorch with the right CUDA build *first*, then the rest:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# RTX 40-series → CUDA 12.1 wheels
pip install torch --index-url https://download.pytorch.org/whl/cu121
# CPU-only alternative:
# pip install torch --index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt
```

The Kokoro model weights (~330 MB) are downloaded from Hugging Face on first
run and cached under `~/.cache/huggingface`. After that, no network is needed.

## Usage

```bash
# Text file → WAV (CUDA used automatically when available)
python zabaudiobooker.py -i chapter1.txt -o chapter1.wav

# Pick a voice and a slightly faster pace
python zabaudiobooker.py -i book.txt -o book.mp3 --voice am_michael --speed 1.1

# Pipe from stdin
echo "Hello from an RTX 4050." | python zabaudiobooker.py -i - -o hello.wav

# Force CPU (useful for debugging or low-VRAM situations)
python zabaudiobooker.py -i book.txt -o book.wav --device cpu

# British English
python zabaudiobooker.py -i story.txt -o story.wav --lang en-gb --voice bf_emma
```

### CLI options

| Flag | Default | Description |
| --- | --- | --- |
| `-i, --input` | *(stdin)* | Input text file. Use `-` to read from stdin. |
| `-o, --output` | *(required)* | Output `.wav` or `.mp3`. |
| `--voice` | `af_heart` | Kokoro voice id (see below). |
| `--lang` | `en-us` | Front-end language: `en-us`, `en-gb`, `es`, `fr`, `hi`, `it`, `ja`, `pt-br`, `zh`. |
| `--speed` | `1.0` | Speech speed multiplier. |
| `--device` | `auto` | `auto`, `cuda`, or `cpu`. |

### Voices

A few good starting points (full list on the
[model card](https://huggingface.co/hexgrad/Kokoro-82M)):

| Voice id | Description |
| --- | --- |
| `af_heart`, `af_bella`, `af_nicole` | American female |
| `am_michael`, `am_adam` | American male |
| `bf_emma`, `bf_isabella` | British female |
| `bm_george`, `bm_lewis` | British male |

## Performance

On an RTX 4050 (6 GB) Kokoro typically runs **10–30× real-time** — roughly one
minute of GPU time per hour of audio. VRAM usage stays well under 2 GB, so it
coexists happily with a desktop session. On CPU expect roughly real-time on a
modern laptop.

The CLI prints an RTF readout after every chunk so you can see throughput live:

```
[info] device=cuda  voice=af_heart  lang=en-us
[chunk 12] audio=42.3s  elapsed=2.1s  RTF=0.05x
[done] wrote chapter1.wav (42.3s of audio)
```

(`RTF=0.05x` ≈ 20× faster than real-time.)

## Project layout

```
.
├── zabaudiobooker.py    # CLI entry point
├── requirements.txt     # Python deps (install torch separately, per CUDA version)
├── README.md
└── .gitignore
```

## License

The CLI code in this repository is MIT-licensed. The Kokoro-82M weights it
downloads are Apache-2.0 (see the Hugging Face model card for details).
