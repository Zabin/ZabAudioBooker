# ZabAudioBooker

Turn a Markdown file, an EPUB or a PDF into a chaptered audiobook, entirely in
your browser. Powered by [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
(82M parameters, Apache-2.0), which runs client-side through ONNX Runtime Web —
your document never leaves the machine.

One file: **`zabaudiobooker.html`**. Open it in a browser. No install, no build
step, no `npm install`, no API key, no account. (Three small companion files —
`zabaudiobooker.webmanifest`, `sw.js`, `icon.svg` — let a served copy be
installed as an app; see [Installing as an app](#installing-as-an-app) below.
None of them are needed to just open and use the page.)

New to any of this? **[MANUAL.md](MANUAL.md)** walks through it step by step.
**[TESTING.md](TESTING.md)** is a checklist for trying it out and reporting
what breaks.

## Features

- Markdown, EPUB and PDF in, MP3, WAV or M4B out — one file per chapter plus a combined file.
- Drop several documents at once to queue up a batch and generate them unattended.
- Runs on your own machine; nothing is uploaded. Synthesis runs on a background
  thread, so the page stays responsive while a long book is generating.
- WebGPU when the browser exposes it, WASM on the CPU otherwise.
- Understands Markdown structure rather than reading the punctuation aloud.
- Multilingual voices: English (US/GB), Spanish, French, Italian, Portuguese (BR), Hindi, Japanese, Mandarin.
- Adjustable speech speed and a large library of bundled voices — preview any
  voice with a short sample before committing to a full run.
- Your voice, format, speed and other Section 2 settings are remembered
  between visits (in the browser's own storage; nothing is sent anywhere).
- Live progress with a real-time-factor (RTF) readout, an estimated output
  size before you generate anything, and cancellable long runs.
- Installable as an offline app once served over `http(s)` — see below.

## Getting started

```bash
# Just open it
xdg-open zabaudiobooker.html        # macOS: open, Windows: start

# Or serve it, which is the more portable route across browsers
npx serve .                         # or: python3 -m http.server 8000
# then visit the URL it prints, e.g. http://localhost:8000/zabaudiobooker.html
```

The first run downloads the model weights from Hugging Face (roughly 90 MB at
`q8`, up to about 330 MB at `fp32`) and the browser caches them. Everything
after that is offline.

Use Chrome or Edge if you have the choice — they have the best support for what
this relies on. Safari and Firefox may work but are less tested.

### Requirements

A current browser and, on first run only, network access to `cdn.jsdelivr.net`
(for [kokoro-js](https://www.npmjs.com/package/kokoro-js), the MP3 encoder,
and — only if you open an EPUB — the unzip library) and `huggingface.co` (for
the weights). Audio is held in memory while it is generated, so a very long
book on a low-memory machine is better done a few chapters at a time.

Synthesis runs in a Web Worker, which needs a browser with module worker
support (Chrome and Edge; Firefox and Safari support varies) — this is the
same Chrome/Edge recommendation as WebGPU above, not an extra requirement.

## Voices

A few good starting points (full list on the
[model card](https://huggingface.co/hexgrad/Kokoro-82M)):

| Voice id | Description |
| --- | --- |
| `af_heart`, `af_bella`, `af_nicole` | American female |
| `am_michael`, `am_adam` | American male |
| `bf_emma`, `bf_isabella` | British female |
| `bm_george`, `bm_lewis` | British male |

Click **▶ Preview** next to the voice picker to hear a short sample line in
whichever voice and speed are currently selected, before committing to a
full book. The first preview pays the same one-time model download as
generating; after that it's quick.

## What it does with Markdown

The point is that it *understands* Markdown rather than reading the punctuation
out loud. A naive text-to-speech tool given a `.md` file says "hash hash
Introduction"; here the document is parsed into blocks first:

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

## EPUBs

Drop a `.epub` and it goes through the same box as Markdown and PDF: unpacked,
converted to Markdown, and left in the text area for you to check before
generating. Unlike a PDF, an EPUB carries real structure — its own chapter
files in reading order (the spine) and usually a table of contents — so the
conversion is far more reliable than PDF's geometry-guessing:

- Chapters are read in spine order; a spine entry marked `linear="no"`
  (typically an ad or alternate page) is skipped, matching what a normal
  reading app shows by default.
- Chapter titles come from the book's own table of contents (`nav.xhtml` in
  EPUB3, `toc.ncx` in EPUB2) when present, falling back to each chapter's own
  heading, then to "Chapter N".
- A cover page that's just an image contributes no readable text and is
  folded into the chapter after it, the same way a PDF title page is.
- Headings, links, lists, tables, blockquotes and code blocks all convert to
  the same Markdown syntax the hand-written parser above already understands,
  so every Section 2 setting (code handling, table handling, list numbering)
  applies identically regardless of source format.

Unzipping an EPUB is the one place this app reaches for a small CDN library
([fflate](https://github.com/101arrowz/fflate)) rather than hand-rolling
DEFLATE decompression itself — the same trade-off already made for MP3
encoding and PDF parsing.

## PDFs

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
still come out as several short headings rather than one clean block. Rather
than shipping each as its own few-second file, any section under about 20 words
is folded into the next substantial one, or the previous one if it's the last
thing in the document. Nothing is dropped; a title page just becomes a short
preamble spoken before chapter one instead of five separate tracks. The same
rule applies to ordinary Markdown — two headings with nothing meaningful
between them merge the same way.

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

## Output

Pick a heading level to split on and you get one file per chapter plus a
combined file for the whole book, each with an inline player and a download
link. MP3 (128 kbps) keeps an audiobook to a sensible size; WAV is 24 kHz mono
PCM and runs about 170 MB per hour, so prefer MP3 for anything long.

**M4B** produces a single file with real, seekable chapter markers built in —
the format most audiobook and podcast apps expect — instead of a folder of
separate tracks. The trade-off: there's no AAC encoder here, so an M4B is
uncompressed 16-bit PCM under the hood, the same size as WAV. Pick it when
having one file with chapters matters more than file size; pick MP3 when size
matters more. Because the whole point of M4B is chapters embedded in one
file, it never produces separate per-chapter files the way MP3/WAV do — only
the combined file.

Once generation finishes, **Download every file** fires off a browser
download for each track in turn, and **Download all as .zip** bundles all
of them — the combined file and every chapter — into one `.zip` next to it.
The zip is written client-side with no library: the audio is already MP3,
WAV or M4B, so there is nothing to gain from recompressing it, and a plain
uncompressed (STORE) archive needs only a small amount of bookkeeping.

Progress is reported as audio produced, elapsed time, and a live RTF figure:

```
audio=42.3s  elapsed=2.1s  RTF=0.05x
```

(`RTF=0.05x` ≈ 20× faster than real-time.) Long runs can be cancelled mid-way.

### Batch mode

Drop (or pick) more than one file at once — any mix of `.md`, `.epub` and
`.pdf` — and a queue appears above the text box instead of loading straight
into it. Click a queued item to review or fix its converted text before
generating, same as with a single PDF or EPUB; remove one with its `×`; drop
more in later to add to the queue.

**Generate N audiobooks** then walks the queue in order, using whatever
voice, speed and format are currently set in Section 2 for all of them. Each
book's tracks appear under their own heading, and the already-loaded model
carries over from one book to the next rather than reloading — only the
first book in a run pays for the model download. **Download every file** and
**Download all as .zip** cover the whole batch; the zip nests each book's
chapter files under their own folder.

Drop a single file with nothing already queued and it behaves exactly as
before — straight into the text box, no queue in sight.

## Performance

With WebGPU, Kokoro typically runs many times faster than real-time — a
fraction of a minute of GPU time per minute of audio. On WASM/CPU expect
roughly real-time on a modern laptop, which still works, just slowly.

## Installing as an app

Served over `http(s)` (not opened straight from disk — see
[Getting started](#getting-started)), the page registers a small service
worker that caches the app shell itself: the page, its manifest and its icon.
A current browser will then offer to install it (an icon in the address bar,
or a browser menu item — "Install ZabAudioBooker" / "Add to Home Screen"),
after which it opens in its own window with no address bar, works with no
network at all, and keeps working across a restart.

This covers the *app*, not the *model*: the Kokoro weights are still a
separate, much larger download the first time you actually generate
something, cached by the browser as already described. Nothing here changes
the offline story above — it just means the page itself no longer needs a
network fetch to open.

## Project layout

```
.
├── zabaudiobooker.html       # the whole app: Markdown/EPUB/PDF -> audiobook
├── zabaudiobooker.webmanifest # app metadata, for "install as an app"
├── sw.js                     # service worker: caches the app shell offline
├── icon.svg                  # app icon
├── MANUAL.md                 # step-by-step guide
├── TESTING.md                # test checklist and feedback template
├── README.md
└── .gitignore
```

## License

The code in this repository is MIT-licensed. The Kokoro-82M weights it
downloads are Apache-2.0 (see the Hugging Face model card for details).
