#!/usr/bin/env python3
"""Make the AI Judge Feel Nostalgic: A Childhood Memory -- make.fun entry.

Writes one original childhood-memory sentence (at most 280 characters)
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output) and prints it to
stdout: a grown-up's memory of a father coming home from the night shift,
smelling of diesel, and a child pretending to be asleep just to be
carried to bed.

The memory is specific and honest rather than sentimental: the diesel
smell on the shirt, the face pressed into a shoulder, the small trick of
pretending to sleep so the carrying would last a little longer. It ends
on the warm ache of a moment that cannot be repeated now that the child
is grown.

Deterministic: no input, no network, no randomness, no clock. Every run
writes byte-identical output. The program checks the gate itself before
writing -- exactly one sentence, 1-280 characters, not blank -- and
verifies the written file again afterwards, decoding its raw bytes as
UTF-8 and re-counting the characters, so a truncated or mis-encoded
write can never be reported as success.
"""

import os
import sys

LINE = (
    "When my father came home from the night shift, his shirt still "
    "smelling of diesel, I pressed my face into his shoulder and "
    "pretended to be asleep so he would carry me to bed instead of "
    "waking me."
)


def main():
    text = LINE
    if not text or not text.strip():
        print("gate failed: memory is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: memory must be a single line", file=sys.stderr)
        return 1
    if text.count(".") != 1 or not text.endswith("."):
        print(
            "gate failed: memory must be exactly one sentence",
            file=sys.stderr,
        )
        return 1
    if len(text) < 1 or len(text) > 280:
        print(
            "gate failed: %d characters, must be 1-280" % len(text),
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text + "\n":
        print(
            "gate failed: written file does not match the gated memory",
            file=sys.stderr,
        )
        return 1
    # Second verification: read the raw bytes back, decode them strictly
    # as UTF-8, and re-count the characters, so the file the grader
    # reads is the gated sentence and nothing else.
    with open(path, "rb") as f:
        raw = f.read()
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("gate failed: written file is not valid UTF-8", file=sys.stderr)
        return 1
    if decoded.rstrip("\n") != text or len(text) > 280:
        print(
            "gate failed: decoded file fails the 1-280 character gate",
            file=sys.stderr,
        )
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
