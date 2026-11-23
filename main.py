#!/usr/bin/env python3
"""Make the Judge Smile — one line about a small good thing today.

Writes exactly one original line (at most 200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output), then reads it back
to verify it before exiting 0. Deterministic: the same bytes every run.
Stdlib only, no arguments, no network, no clock, no randomness.
"""

import os
import sys

LINE = (
    "The bus driver killed his headlights at my stop so the moths "
    "could finish dancing, then waved me aboard like we had known "
    "each other for years."
)


def main() -> int:
    text = LINE.strip()
    if not (1 <= len(text) <= 200):
        print(f"line is {len(text)} characters, must be 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("line is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text:
        print("line must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 for ch in text):
        print("line must not contain control characters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            print("read-back mismatch", file=sys.stderr)
            return 1

    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
