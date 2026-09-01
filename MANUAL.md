# ZabAudioBooker — User Manual

This manual assumes you have never used Python, never opened a terminal, and
have nothing installed. Every step is spelled out.

---

## Start here: you probably don't need Python

ZabAudioBooker comes in two versions. They use the same AI voice model and
produce the same quality of audio.

| | **Browser version** | **Command-line version** |
| --- | --- | --- |
| File | `zabaudiobooker.html` | `zabaudiobooker.py` |
| Do you need Python? | **No** | Yes |
| Anything to install? | **Nothing** | Python, PyTorch, and 3 other pieces |
| Reads Markdown (`.md`) files? | **Yes, properly** | No — it would read the `#` symbols out loud |
| Splits a book into chapters? | **Yes** | No |
| Time to first audio | About 5 minutes | About 30–60 minutes |
| Uses your graphics card | Yes, if your browser supports it | Yes, if you have an NVIDIA card |

**If you are not sure, use the browser version.** Go to
[Part 1](#part-1--the-browser-version-no-python-needed) and ignore Part 2
entirely. Part 2 exists for people who want to run it from a terminal or
automate it.

Both versions do all the work on your own computer. Your document is never
uploaded anywhere.

---

## Part 1 — The browser version (no Python needed)

### Step 1: Get the file

1. Go to the project page on GitHub.
2. Click the green **Code** button, then **Download ZIP**.
3. Find the downloaded ZIP in your Downloads folder and unzip it
   (Windows: right-click, *Extract All*. Mac: double-click it).
4. Open the folder that appears. You are looking for a file named
   **`zabaudiobooker.html`**.

### Step 2: Open it

Double-click `zabaudiobooker.html`. It opens in your web browser like any
web page.

Use **Chrome** or **Edge** if you have a choice — they have the best support
for the technology this uses. Safari and Firefox may work but are less tested.

You should see a page headed "ZabAudioBooker" with four numbered sections.
There is nothing to install and no account to create.

### Step 3: Make your first audiobook

1. **Section 1 — Markdown.** Drag a `.md` file onto the dotted box, or click
   the box to browse for one. You can also type or paste text directly into
   the large box underneath.

   No Markdown file handy? Paste this in to try it out:

   ```
   # My First Audiobook

   This is the opening paragraph.

   ## Chapter One

   Here is some text that will become the first chapter.
   ```

2. **Check the summary line** under the box. It tells you the word count and
   roughly how many minutes of audio you will get. Use this to sanity-check
   before starting something long.

3. **Section 2 — Voice & output.** The defaults are fine for a first run.
   You can change the voice if you like; `af_heart` is a good American female
   voice, `bm_george` a British male one.

4. **Section 3 — Generate.** Before clicking anything, expand
   **"Preview the text that will be spoken"**. This shows you exactly what the
   voice will read — headings kept, code blocks removed, links read as their
   text without the web address. If something looks wrong here, it will sound
   wrong too, so fix it now.

5. Click **Generate audiobook**.

### What happens on the first run

**The first time only**, your browser downloads the AI voice model. This is
roughly 90 MB to 330 MB depending on the Precision setting. You will see a
progress bar and a "Downloading model" message. This needs an internet
connection and can take a few minutes.

After that the model is saved in your browser, and everything works offline.

Once the download finishes, synthesis begins. The status line shows how much
audio has been produced, how long it has taken, and an "RTF" figure — that is
how fast it is running. `RTF 0.05x` means it is producing audio 20 times
faster than real time. You can click **Cancel** at any point.

### Step 4: Get your files

**Section 4 — Result** appears with a player for each file:

- **Complete book** — the whole document as one file.
- **One file per chapter** — numbered, e.g. `01-chapter-one.mp3`.

Press play to listen in the page, or click **Download** to save. **Download
every file** saves all of them at once (your browser may ask permission to
download multiple files — say yes).

### Every setting explained

| Setting | What it does |
| --- | --- |
| **Voice** | Which voice reads the text. The letters mean accent and gender: `af_` = American female, `am_` = American male, `bf_` = British female, `bm_` = British male. |
| **Speed** | `1` is normal. `1.15` is a common audiobook speed. Below `0.8` or above `1.5` starts to sound unnatural. |
| **Format** | **MP3** for anything long — an hour is about 60 MB. **WAV** is uncompressed and much bigger (about 170 MB per hour), only worth it if you plan to edit the audio. |
| **Split into chapters at** | Where to cut the book into separate files. `Heading 2 (##)` suits most documents. Choose *Don't split* for one single file. |
| **Device** | Leave on **Auto**. It uses your graphics card if your browser offers one, otherwise the processor. |
| **Precision** | Leave on **Auto**. Lower precision (`q8`) means a smaller download and faster running; higher (`fp32`) means slightly better audio. |
| **Code blocks** | What to do with code in the document. **Skip silently** is the default. |
| **Tables** | Tables are read row by row as "column name: value", or skipped. |
| **Number ordered lists aloud** | Whether a numbered list is read as "One. Two. Three." or just as sentences. |

### If something goes wrong

| What you see | What to do |
| --- | --- |
| A red box saying it could not load from the CDN | You are offline, or a firewall is blocking it. The first run needs access to `cdn.jsdelivr.net` and `huggingface.co`. Connect and reload the page. |
| Nothing happens when you click Generate | Look for the red box. If there is none, open the browser console (see [Reporting problems](TESTING.md#how-to-capture-a-useful-error)) and check for errors. |
| The page says the download is blocked from your filesystem | Follow the yellow hint on the page: it tells you how to serve the folder locally instead. |
| It is very slow | Your browser is probably using the processor rather than the graphics card. This is normal and still works — expect roughly real time, so an hour of audio takes about an hour. |
| The browser tab crashes on a very long book | The audio is held in memory while it is made. Split the document and do a few chapters at a time. |

---

## Part 2 — The command-line version (this one needs Python)

Only do this if you actually want the terminal version. **The browser version
above is easier and does more.**

Also know this up front: **the command-line version reads plain text, not
Markdown.** Give it a `.md` file and it will say "hash hash Chapter One" out
loud. Use the browser version for Markdown.

### What you are about to do, in plain English

Five things, in order:

1. **Install Python.** A programming language. The tool is written in it, so
   your computer needs it to run the tool.
2. **Open a terminal.** A window where you type commands instead of clicking.
3. **Create a "virtual environment".** A private folder for this project's
   ingredients, so it cannot break anything else on your computer. It is just
   a folder — deleting it undoes everything.
4. **Install the ingredients** with a tool called `pip`, which comes with
   Python and downloads code libraries for you.
5. **Run the tool.**

Throughout, lines in `boxes like this` are things you type into the terminal
and then press Enter.

### Step 1: Install Python

**Windows**

1. Go to [python.org/downloads](https://www.python.org/downloads/).
2. Click the big yellow **Download Python** button.
3. Run the installer. **Before clicking Install, tick the box at the bottom
   that says "Add python.exe to PATH".** This matters. If you miss it, the
   terminal will not find Python and you will have to reinstall.
4. Click **Install Now** and wait.

**Mac**

1. Go to [python.org/downloads](https://www.python.org/downloads/).
2. Download the macOS installer and run it, clicking through the defaults.

(macOS has a version of Python built in, but it is old and awkward to install
things into. Use the one from python.org.)

**Linux (Ubuntu or Debian)**

Open a terminal and run:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

You will need Python 3.10 or newer.

### Step 2: Open a terminal

- **Windows:** press the Start button, type `powershell`, open **Windows
  PowerShell**.
- **Mac:** press Cmd+Space, type `terminal`, press Enter.
- **Linux:** press Ctrl+Alt+T.

Check Python arrived. Type this and press Enter:

```bash
python3 --version
```

On Windows, type `python --version` instead.

You should see something like `Python 3.12.1`. If you instead see "command not
found" or "not recognized", Python is not installed, or on Windows you missed
the "Add python.exe to PATH" tickbox — reinstall and tick it.

### Step 3: Get the project onto your computer

Download the ZIP as described in [Part 1, Step 1](#step-1-get-the-file), and
unzip it.

Now point the terminal at that folder. Type `cd`, then a space, then drag the
unzipped folder from your file manager onto the terminal window — it fills in
the path for you. Press Enter.

```bash
cd /path/to/ZabAudioBooker
```

Check you are in the right place:

```bash
ls          # Mac and Linux
dir         # Windows
```

You should see `zabaudiobooker.py` listed.

### Step 4: Create the virtual environment

```bash
python3 -m venv .venv
```

(Windows: use `python` instead of `python3` in this and every command below.)

Nothing appears to happen for a few seconds, and then you get your prompt
back. A hidden folder called `.venv` has been created.

Now **activate** it:

```bash
source .venv/bin/activate          # Mac and Linux
.venv\Scripts\activate             # Windows PowerShell
```

Your prompt now starts with `(.venv)`. That tells you the environment is
active.

> **Windows note:** if you get *"running scripts is disabled on this system"*,
> run this once, then try activating again:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

**You must activate the environment every time you open a new terminal.** If a
command later fails with "module not found", this is almost always the reason —
check for `(.venv)` in your prompt.

### Step 5: Install PyTorch

PyTorch is the engine that runs the AI model. It has to be installed first and
separately, because which version you need depends on your hardware.

**If you do not have an NVIDIA graphics card, or you are not sure**, install
the processor-only version. It is smaller and always works:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**If you do have an NVIDIA graphics card** and want the speed, go to
[pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/),
choose your system in the picker, and run the command it gives you. That page
is always current, which is why we send you there rather than printing a
command that may go stale.

This download is large — expect several hundred megabytes and a few minutes.

### Step 6: Install everything else

```bash
pip install -r requirements.txt
```

### Step 7: Install the two helper programs

These are ordinary programs, not Python packages. `espeak-ng` helps the model
pronounce unusual words. `ffmpeg` is only needed if you want MP3 output.

```bash
# Mac (needs Homebrew from brew.sh)
brew install espeak-ng ffmpeg

# Ubuntu or Debian
sudo apt install espeak-ng ffmpeg

# Arch
sudo pacman -S espeak-ng ffmpeg
```

**Windows:** download and install each manually —
[espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases) and
[ffmpeg builds](https://www.gyan.dev/ffmpeg/builds/).

### Step 8: Your first run

Make a plain text file called `test.txt` containing a sentence or two. Then:

```bash
python3 zabaudiobooker.py -i test.txt -o test.wav
```

The **first run downloads the voice model** (about 330 MB), so it will pause a
while. After that it is cached and works offline.

You will see progress like this:

```
[info] device=cuda  voice=af_heart  lang=en-us
[chunk 12] audio=42.3s  elapsed=2.1s  RTF=0.05x
[done] wrote test.wav (42.3s of audio)
```

`RTF=0.05x` means it ran 20 times faster than real time. When it finishes,
`test.wav` is in the folder. Open it in any music player.

### Everyday use

```bash
# A text file to a WAV
python3 zabaudiobooker.py -i chapter1.txt -o chapter1.wav

# A different voice, slightly faster, saved as MP3
python3 zabaudiobooker.py -i book.txt -o book.mp3 --voice am_michael --speed 1.1

# British English
python3 zabaudiobooker.py -i story.txt -o story.wav --lang en-gb --voice bf_emma

# Force the processor instead of the graphics card
python3 zabaudiobooker.py -i book.txt -o book.wav --device cpu
```

### All the options

| Option | Default | What it does |
| --- | --- | --- |
| `-i`, `--input` | reads what you type | The text file to read. Use `-` to pipe text in. |
| `-o`, `--output` | **required** | Where to save. Must end in `.wav` or `.mp3`. |
| `--voice` | `af_heart` | Which voice. Same IDs as the browser version. |
| `--lang` | `en-us` | `en-us`, `en-gb`, `es`, `fr`, `hi`, `it`, `ja`, `pt-br`, `zh`. Must match your voice. |
| `--speed` | `1.0` | Speech speed. |
| `--device` | `auto` | `auto`, `cuda` (NVIDIA card), or `cpu`. |

### Command-line troubleshooting

| What you see | What it means |
| --- | --- |
| `command not found: python3` | Python is not installed, or on Windows was installed without "Add to PATH". Try `python` instead of `python3`. |
| `No module named 'kokoro'` (or `torch`) | The virtual environment is not active. Check your prompt shows `(.venv)`; if not, re-run the activate command from Step 4. |
| `running scripts is disabled on this system` | Windows PowerShell. Run the `Set-ExecutionPolicy` line in Step 4. |
| `MP3 output needs pydub + ffmpeg` | `ffmpeg` is missing. See Step 7. |
| `Unsupported output extension` | Your `-o` filename must end in `.wav` or `.mp3`. |
| `Input text is empty` | The input file is empty, or you gave a path that does not exist. |
| It reads `#` and `*` out loud | You gave it a Markdown file. Use the browser version for those. |
| CUDA warnings, then it runs anyway | Harmless. It could not find your graphics card and used the processor instead. |

### Starting over

Delete the `.venv` folder. That removes everything installed in Step 5 and 6,
and changes nothing else on your computer. To reclaim the downloaded model as
well, delete the `huggingface` folder inside your user cache directory
(`~/.cache/huggingface` on Mac and Linux).

---

## Glossary

| Term | Meaning |
| --- | --- |
| **Terminal** / **PowerShell** | A window where you type commands instead of clicking. |
| **Python** | The programming language the command-line tool is written in. |
| **pip** | Python's installer. It fetches code libraries for you. |
| **Virtual environment** (`.venv`) | A private folder holding this project's libraries, so they cannot clash with anything else. |
| **PyTorch** | The engine that runs AI models. |
| **Kokoro-82M** | The AI voice model itself. 82 million parameters, small enough to run on a laptop. |
| **Model weights** | The downloaded file containing what the AI has learned. Large, downloaded once. |
| **WebGPU** | The browser feature that lets a web page use your graphics card. |
| **RTF** | Real-Time Factor. How long it takes to make audio versus the length of that audio. Lower is faster; `0.05x` is 20 times faster than real time. |
| **Markdown** (`.md`) | A plain-text format where `#` marks a heading and `**bold**` marks bold text. |
