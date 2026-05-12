#!/usr/bin/env python3
"""Offline AI text-to-speech CLI using Kokoro-82M.

Reads a text file (or stdin) and writes a WAV or MP3 file. Uses CUDA when
available (e.g. RTX 4050) and falls back to CPU otherwise.

Example:
    python zabaudiobooker.py -i book.txt -o book.wav --voice af_heart
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline

SAMPLE_RATE = 24_000

# Kokoro language codes. See https://github.com/hexgrad/kokoro
LANG_CODES = {
    "en-us": "a",
    "en-gb": "b",
    "es": "e",
    "fr": "f",
    "hi": "h",
    "it": "i",
    "ja": "j",
    "pt-br": "p",
    "zh": "z",
}


def select_device(requested: str) -> str:
    if requested == "cuda" and not torch.cuda.is_available():
        print("[warn] CUDA requested but unavailable; falling back to CPU.", file=sys.stderr)
        return "cpu"
    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return requested


def read_text(path: Path | None) -> str:
    if path is None or str(path) == "-":
        return sys.stdin.read()
    return path.read_text(encoding="utf-8")


def synthesize(text: str, voice: str, lang: str, speed: float, device: str) -> np.ndarray:
    pipeline = KPipeline(lang_code=LANG_CODES[lang], device=device)
    chunks: list[np.ndarray] = []
    t0 = time.time()
    total_samples = 0
    for i, (_graphemes, _phonemes, audio) in enumerate(
        pipeline(text, voice=voice, speed=speed)
    ):
        if isinstance(audio, torch.Tensor):
            audio = audio.detach().cpu().numpy()
        chunks.append(audio)
        total_samples += audio.shape[-1]
        secs = total_samples / SAMPLE_RATE
        elapsed = time.time() - t0
        rtf = elapsed / secs if secs > 0 else 0.0
        print(
            f"\r[chunk {i + 1}] audio={secs:.1f}s  elapsed={elapsed:.1f}s  RTF={rtf:.2f}x",
            end="",
            file=sys.stderr,
            flush=True,
        )
    print("", file=sys.stderr)
    if not chunks:
        raise RuntimeError("No audio was generated.")
    return np.concatenate(chunks)


def write_audio(audio: np.ndarray, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    suffix = out.suffix.lower()
    if suffix == ".wav":
        sf.write(out, audio, SAMPLE_RATE)
        return
    if suffix == ".mp3":
        try:
            from pydub import AudioSegment
        except ImportError as e:
            raise SystemExit(
                "MP3 output needs pydub + ffmpeg. `pip install pydub` and install ffmpeg."
            ) from e
        pcm16 = np.clip(audio, -1.0, 1.0)
        pcm16 = (pcm16 * 32767).astype(np.int16)
        seg = AudioSegment(
            pcm16.tobytes(), frame_rate=SAMPLE_RATE, sample_width=2, channels=1
        )
        seg.export(out, format="mp3", bitrate="128k")
        return
    raise SystemExit(f"Unsupported output extension: {suffix} (use .wav or .mp3)")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Offline AI TTS using Kokoro-82M.")
    p.add_argument("-i", "--input", type=Path, help="Input text file (use - for stdin).")
    p.add_argument("-o", "--output", type=Path, required=True, help="Output .wav or .mp3.")
    p.add_argument(
        "--voice",
        default="af_heart",
        help="Kokoro voice id (e.g. af_heart, af_bella, am_michael, bf_emma). "
        "See the Kokoro model card for the full list.",
    )
    p.add_argument(
        "--lang",
        default="en-us",
        choices=sorted(LANG_CODES.keys()),
        help="Language for the front-end (default: en-us).",
    )
    p.add_argument("--speed", type=float, default=1.0, help="Speech speed multiplier.")
    p.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cuda", "cpu"],
        help="Compute device (default: auto).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    device = select_device(args.device)
    print(f"[info] device={device}  voice={args.voice}  lang={args.lang}", file=sys.stderr)
    text = read_text(args.input)
    if not text.strip():
        raise SystemExit("Input text is empty.")
    audio = synthesize(text, args.voice, args.lang, args.speed, device)
    write_audio(audio, args.output)
    duration = audio.shape[-1] / SAMPLE_RATE
    print(f"[done] wrote {args.output} ({duration:.1f}s of audio)", file=sys.stderr)


if __name__ == "__main__":
    main()
