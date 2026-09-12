# ZabAudioBooker

Offline AI text-to-speech powered by [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
(82M parameters, Apache-2.0). Runs fully offline once the weights are cached and
takes advantage of an NVIDIA GPU (developed against an RTX 4050) with a clean
CPU fallback.

Two ways in:

- **`zabaudiobooker.py`** — Python CLI. Plain text in, WAV or MP3 out.
- **`zabaudiobooker.html`** — a single page you open in a browser. Markdown or
  PDF in, a chaptered audiobook out. No Python, no install; Kokoro runs
  client-side.

New to Python, or to any of this? **[MANUAL.md](MANUAL.md)** is a step-by-step
guide that assumes nothing is installed. **[TESTING.md](TESTING.md)** is a
checklist for trying the browser version and reporting what breaks.

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

## Usage — CLI

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

## Browser version — Markdown to audiobook

`zabaudiobooker.html` is self-contained: open it in a browser, drop in a `.md`
file, and get audio back. It runs the same Kokoro-82M model and the same voice
IDs as the CLI, but through ONNX Runtime Web instead of PyTorch. Your document
never leaves the machine.

```bash
# Just open it
xdg-open zabaudiobooker.html        # macOS: open, Windows: start

# Or serve it, which is the more portable route across browsers
python3 -m http.server 8000
# then visit http://localhost:8000/zabaudiobooker.html
```

The first run downloads the model weights from Hugging Face (roughly 90 MB at
`q8`, up to about 330 MB at `fp32`) and the browser caches them. Everything
after that is offline. WebGPU is used when the browser exposes it, otherwise it
falls back to WASM on the CPU.

### PDFs

Drop a `.pdf` on the same box and it is converted to Markdown first, into the
text area, where you can read and correct it before generating anything. A PDF
carries no structure, only positioned glyphs, so the conversion is inference and
it will sometimes be wrong. That is exactly why the Markdown is left in front of
you rather than sent straight to the voice.

What it strips, none of which you want read aloud:

| Removed | How it is recognised |
| --- | --- |
| Running heads and feet | First or last line on a page, detached from the text block, recurring across a quarter of the pages |
| Download stamps | Rotated text, which in a book is never content |
| Page numbers | Bare numerals in the margin bands, arabic or roman |
| Footnote markers | Small glyphs riding above the baseline, digits or `* † ‡ § ¶` |
| Footnote text | Small print sitting below the last full-size line on its page |
| Index and contents pages | Pages mostly made of "entry, 12, 45" lines or dot leaders |

A title page that sets the title, subtitle and byline in different sizes can
still come out as several short headings rather than one clean block — that's
the two-column limitation above. Rather than shipping each as its own
few-second file, any section under about 20 words is folded into the next
substantial one, or the previous one if it's the last thing in the document.
Nothing is dropped; a title page just becomes a short preamble spoken before
chapter one instead of five separate tracks. The same rule applies to
ordinary Markdown — two headings with nothing meaningful between them merge
the same way.

It also reflows wrapped lines back into paragraphs, rejoins words broken across
a line by a hyphen, and promotes larger type to headings, which then feed the
chapter splitter for free.

Some older typesetting maps ligature glyphs onto `ª` and `º`, so "financial"
arrives as "ªnancial" and a voice reads gibberish. That is repaired, but only
on the document's own evidence: the glyph has to be used inside words and never
sit against a digit, so a Spanish or Portuguese ordinal like `1ª` is untouched.

Limits worth knowing. **Two-column layouts will come out scrambled**, because
lines are grouped by vertical position and a two-column page interleaves them.
Tables, equations and figure captions read poorly. A scanned PDF has no text
layer at all; that is detected and refused with an explanation rather than
producing silence. For anything pathological, run it through
[Marker](https://github.com/datalab-to/marker),
[MinerU](https://github.com/opendatalab/MinerU) or
[Docling](https://github.com/docling-project/docling), which are far stronger
converters, and drop the Markdown they give you in here.

Opened from the filesystem, the PDF reader falls back to running on the main
thread, which is slower and freezes the page while it works. Serving the folder
avoids that.

### What it does with Markdown

The point of the browser version is that it *understands* Markdown rather than
reading the punctuation out loud. Feeding a `.md` file to the CLI gets you
"hash hash Introduction"; here the document is parsed into blocks first:

| Markdown | Spoken as |
| --- | --- |
| Headings | The title text, with a pause — and the chapter split point |
| Links | The link text; the URL is dropped |
| Images | The alt text |
| Fenced code | Skipped — or announced, or read aloud, your choice |
| Inline code | Read normally, so `af_heart` stays intact |
| Lists | One sentence per item; ordered lists can be numbered aloud |
| Tables | Flattened row-wise to "header: value", or skipped |
| Blockquotes | Read as ordinary prose |
| Bare URLs, footnotes (marker and definition), YAML front matter, HTML tags, emoji | Removed |

Use the *Preview the text that will be spoken* panel to see exactly what the
model will receive before you commit to a long run.

### Output

Pick a heading level to split on and you get one file per chapter plus a
combined file for the whole book, each with an inline player and a download
link. MP3 (128 kbps) keeps an audiobook to a sensible size; WAV is 24 kHz mono
PCM and runs about 170 MB per hour, so prefer MP3 for anything long.

Once generation finishes, **Download every file** fires off a browser
download for each track in turn, and **Download all as .zip** bundles all
of them — the combined file and every chapter — into one `.zip` next to it.
The zip is written client-side with no library: the audio is already MP3 or
WAV, so there is nothing to gain from recompressing it, and a plain
uncompressed (STORE) archive needs only a small amount of bookkeeping.

Progress is reported the same way the CLI reports it — audio produced, elapsed
time, and a live RTF figure — and long runs can be cancelled mid-way.

### Requirements

A current browser and, on first run only, network access to `cdn.jsdelivr.net`
(for [kokoro-js](https://www.npmjs.com/package/kokoro-js)) and `huggingface.co`
(for the weights). No build step, no `npm install`, no API key. Audio is held in
memory while it is generated, so a very long book on a low-memory machine is
better done a few chapters at a time.

## Project layout

```
.
├── zabaudiobooker.py    # CLI entry point
├── zabaudiobooker.html  # standalone browser app (Markdown -> audiobook)
├── requirements.txt     # Python deps (install torch separately, per CUDA version)
├── README.md
└── .gitignore
```

## License

The CLI code in this repository is MIT-licensed. The Kokoro-82M weights it
downloads are Apache-2.0 (see the Hugging Face model card for details).
