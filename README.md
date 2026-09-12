# ZabAudioBooker

Turn a Markdown file or a PDF into a chaptered audiobook, entirely in your
browser. Powered by [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
(82M parameters, Apache-2.0), which runs client-side through ONNX Runtime Web —
your document never leaves the machine.

One file: **`zabaudiobooker.html`**. Open it in a browser. No install, no build
step, no `npm install`, no API key, no account.

New to any of this? **[MANUAL.md](MANUAL.md)** walks through it step by step.
**[TESTING.md](TESTING.md)** is a checklist for trying it out and reporting
what breaks.

## Features

- Markdown and PDF in, MP3 or WAV out — one file per chapter plus a combined file.
- Runs on your own machine; nothing is uploaded.
- WebGPU when the browser exposes it, WASM on the CPU otherwise.
- Understands Markdown structure rather than reading the punctuation aloud.
- Multilingual voices: English (US/GB), Spanish, French, Italian, Portuguese (BR), Hindi, Japanese, Mandarin.
- Adjustable speech speed and a large library of bundled voices — no voice cloning, no internet calls after the first run.
- Live progress with a real-time-factor (RTF) readout, and cancellable long runs.

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
(for [kokoro-js](https://www.npmjs.com/package/kokoro-js)) and `huggingface.co`
(for the weights). Audio is held in memory while it is generated, so a very
long book on a low-memory machine is better done a few chapters at a time.

## Voices

A few good starting points (full list on the
[model card](https://huggingface.co/hexgrad/Kokoro-82M)):

| Voice id | Description |
| --- | --- |
| `af_heart`, `af_bella`, `af_nicole` | American female |
| `am_michael`, `am_adam` | American male |
| `bf_emma`, `bf_isabella` | British female |
| `bm_george`, `bm_lewis` | British male |

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

Once generation finishes, **Download every file** fires off a browser
download for each track in turn, and **Download all as .zip** bundles all
of them — the combined file and every chapter — into one `.zip` next to it.
The zip is written client-side with no library: the audio is already MP3 or
WAV, so there is nothing to gain from recompressing it, and a plain
uncompressed (STORE) archive needs only a small amount of bookkeeping.

Progress is reported as audio produced, elapsed time, and a live RTF figure:

```
audio=42.3s  elapsed=2.1s  RTF=0.05x
```

(`RTF=0.05x` ≈ 20× faster than real-time.) Long runs can be cancelled mid-way.

## Performance

With WebGPU, Kokoro typically runs many times faster than real-time — a
fraction of a minute of GPU time per minute of audio. On WASM/CPU expect
roughly real-time on a modern laptop, which still works, just slowly.

## Project layout

```
.
├── zabaudiobooker.html  # the whole app: Markdown/PDF -> audiobook
├── MANUAL.md            # step-by-step guide
├── TESTING.md           # test checklist and feedback template
├── README.md
└── .gitignore
```

## License

The code in this repository is MIT-licensed. The Kokoro-82M weights it
downloads are Apache-2.0 (see the Hugging Face model card for details).
