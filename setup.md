# ZabAudioBooker — offline AI TTS (Kokoro-82M)

Offline Python text-to-speech using [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M),
an 82M-parameter Apache-2.0 model. Runs on an RTX 4050 (CUDA) or CPU.

## Install

System dep (used by Kokoro's text frontend):

```bash
# Debian/Ubuntu
sudo apt install espeak-ng ffmpeg
# Arch
sudo pacman -S espeak-ng ffmpeg
# Windows: install espeak-ng from https://github.com/espeak-ng/espeak-ng/releases
```

Python deps — install PyTorch with the right CUDA build first, then the rest:

```bash
python -m venv .venv && source .venv/bin/activate
# RTX 4050 → CUDA 12.1 wheels
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

The Kokoro model weights (~330 MB) download from Hugging Face on first run and
cache under `~/.cache/huggingface`.

## Usage

```bash
# Text file → WAV (uses CUDA automatically if available)
python zabaudiobooker.py -i chapter1.txt -o chapter1.wav

# Pick a voice and speed
python zabaudiobooker.py -i book.txt -o book.mp3 --voice am_michael --speed 1.1

# Pipe from stdin
echo "Hello from an RTX 4050." | python zabaudiobooker.py -i - -o hello.wav

# Force CPU
python zabaudiobooker.py -i book.txt -o book.wav --device cpu
```

### Voices

Kokoro ships bundled voices. A few good starting points:

- `af_heart`, `af_bella`, `af_nicole` — American female
- `am_michael`, `am_adam` — American male
- `bf_emma`, `bf_isabella` — British female
- `bm_george`, `bm_lewis` — British male

See the [model card](https://huggingface.co/hexgrad/Kokoro-82M) for the full list.

### Performance on RTX 4050

Kokoro is small — expect 10–30× real-time on the 4050 (≈1 minute of synthesis
per hour of audio). VRAM usage stays well under 2 GB.
