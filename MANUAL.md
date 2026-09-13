# ZabAudioBooker — User Manual

This manual assumes you have never done anything like this before. Every step
is spelled out. There is nothing to install and no account to create — the whole
tool is one web page you open in your browser.

All the work happens on your own computer. Your document is never uploaded
anywhere.

---

## Step 1: Get the file

1. Go to the project page on GitHub.
2. Click the green **Code** button, then **Download ZIP**.
3. Find the downloaded ZIP in your Downloads folder and unzip it
   (Windows: right-click, *Extract All*. Mac: double-click it).
4. Open the folder that appears. You are looking for a file named
   **`zabaudiobooker.html`**.

## Step 2: Open it

Double-click `zabaudiobooker.html`. It opens in your web browser like any
web page.

Use **Chrome** or **Edge** if you have a choice — they have the best support
for the technology this uses. Safari and Firefox may work but are less tested.

You should see a page headed "ZabAudioBooker" with four numbered sections.

## Step 3: Make your first audiobook

1. **Section 1 — Markdown.** Drag a `.md`, `.epub` or `.pdf` file onto the
   dotted box, or click the box to browse for one. You can also type or paste
   text directly into the large box underneath.

   **Dropping an EPUB** converts its chapters to Markdown automatically, in
   the right order, using the book's own chapter titles where it has them.
   This is much more reliable than a PDF, since an EPUB actually has chapters
   to begin with rather than just positioned text on a page.

   **Dropping a PDF** converts it to Markdown first and puts the result in the
   box. Read it before you generate anything. Running heads, page numbers,
   footnotes and index pages are stripped automatically, but a PDF has no real
   structure, so the conversion is guesswork and sometimes gets it wrong. The
   box is editable precisely so you can fix it. Two-column PDFs come out
   scrambled, and scanned PDFs are refused with an explanation because they
   contain no text at all.

   **Dropping several files at once** (or adding one, then dropping another
   later) queues them up as a batch instead of loading straight into the box —
   see [Making several audiobooks at once](#making-several-audiobooks-at-once)
   below.

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
   voice, `bm_george` a British male one. Click **▶ Preview** to hear a short
   sample in the current voice before committing to a whole book — the first
   preview downloads the same voice model a full run would.

   Whatever you set here — voice, speed, format and the rest — is remembered
   for next time you open the page.

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

## Step 4: Get your files

**Section 4 — Result** appears with a player for each file:

- **Complete book** — the whole document as one file.
- **One file per chapter** — numbered, e.g. `01-chapter-one.mp3`.

Press play to listen in the page, or click **Download** to save. **Download
every file** saves all of them at once (your browser may ask permission to
download multiple files — say yes). **Download all as .zip** does the same
thing but as one file, which is easier to move around or send to someone
else — everything comes out into a single `.zip` you can open normally.

---

## Making several audiobooks at once

Drop more than one file onto the box in one go, or drop a second file after
you've already loaded one — either way, a list appears above the text box
instead of the file loading straight in. Each entry shows its name and
whether it's still converting, ready, or hit an error.

Click an item in the list to check or fix its text before generating, the
same way you would with a single PDF or EPUB. The `×` next to an item
removes it from the list; if you remove all but one, the list disappears and
you're back to the normal single-document view.

With two or more queued, the **Generate audiobook** button changes to
**Generate N audiobooks**. Click it once and it works through the whole list
using whatever voice, speed and format you've set, one book after another —
the model only downloads once, at the start, not once per book. Section 4
lists each book's tracks under its own heading, and **Download every file** /
**Download all as .zip** both cover everything in the batch.

## Every setting explained

| Setting | What it does |
| --- | --- |
| **Voice** | Which voice reads the text. The letters mean accent and gender: `af_` = American female, `am_` = American male, `bf_` = British female, `bm_` = British male. |
| **Speed** | `1` is normal. `1.15` is a common audiobook speed. Below `0.8` or above `1.5` starts to sound unnatural. |
| **Format** | **MP3** for anything long — an hour is about 60 MB. **WAV** is uncompressed and much bigger (about 170 MB per hour), only worth it if you plan to edit the audio. **M4B** is one file with chapters built in, the format most audiobook apps expect — but it's uncompressed too (same size as WAV), and it never makes separate chapter files, only the one combined book. |
| **Split into chapters at** | Where to cut the book into separate files. `Heading 2 (##)` suits most documents. Choose *Don't split* for one single file. A heading with almost nothing after it — a title page, a bare section divider — is folded into the next real chapter automatically, so you don't end up with a pile of one- or two-second files. |
| **Device** | Leave on **Auto**. It uses your graphics card if your browser offers one, otherwise the processor. |
| **Precision** | Leave on **Auto**. Lower precision (`q8`) means a smaller download and faster running; higher (`fp32`) means slightly better audio. |
| **Code blocks** | What to do with code in the document. **Skip silently** is the default. |
| **Tables** | Tables are read row by row as "column name: value", or skipped. |
| **Number ordered lists aloud** | Whether a numbered list is read as "One. Two. Three." or just as sentences. |

## If something goes wrong

| What you see | What to do |
| --- | --- |
| A red box saying it could not load from the CDN | You are offline, or a firewall is blocking it. The first run needs access to `cdn.jsdelivr.net` and `huggingface.co`. Connect and reload the page. |
| Nothing happens when you click Generate | Look for the red box. If there is none, open the browser console (see [Reporting problems](TESTING.md#how-to-capture-a-useful-error)) and check for errors. |
| The page says the download is blocked from your filesystem | Follow the yellow hint on the page: it tells you how to serve the folder locally instead. |
| It is very slow | Your browser is probably using the processor rather than the graphics card. This is normal and still works — expect roughly real time, so an hour of audio takes about an hour. |
| The browser tab crashes on a very long book | The audio is held in memory while it is made. Split the document and do a few chapters at a time. |

### Serving the folder

A couple of browsers refuse to download the model when the page is opened
straight off your disk. If you hit that, serve the folder instead: open a
terminal in the unzipped folder and run one of these, then visit the address
it prints.

```bash
npx serve .                  # needs Node.js
python3 -m http.server 8000  # needs Python; already present on most Macs and Linux
```

Neither is a dependency of the tool itself — they are just two common ways to
put a folder on `http://localhost` for a moment.

Serving the folder this way also lets the browser offer to **install**
ZabAudioBooker as an app (an icon in the address bar, or "Install…" in the
browser menu). Installed, it opens in its own window and works with no
internet connection at all — the app itself, that is; generating still needs
the model downloaded at least once, same as always.

### Starting over

To reclaim the space the downloaded model takes, clear your browser's site data
for the page (in Chrome: **Settings → Privacy → Third-party cookies → See all
site data**, then remove the entry). It will download again next time.

---

## Glossary

| Term | Meaning |
| --- | --- |
| **Kokoro-82M** | The AI voice model itself. 82 million parameters, small enough to run on a laptop. |
| **Model weights** | The downloaded file containing what the AI has learned. Large, downloaded once. |
| **WebGPU** | The browser feature that lets a web page use your graphics card. |
| **WASM** | WebAssembly — the fallback that runs the model on your processor when WebGPU is not available. |
| **RTF** | Real-Time Factor. How long it takes to make audio versus the length of that audio. Lower is faster; `0.05x` is 20 times faster than real time. |
| **Markdown** (`.md`) | A plain-text format where `#` marks a heading and `**bold**` marks bold text. |
| **EPUB** (`.epub`) | The common ebook file format — really a zip file full of chapter pages plus a table of contents. |
| **M4B** | An audiobook file format: one file with chapter markers built in, so a player can jump between chapters and remember where you stopped. |
