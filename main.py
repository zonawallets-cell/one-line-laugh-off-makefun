"""One-Line Laugh-Off — writes one funny line to /output/entry.txt.

Pure stdlib (os only). The line is a single sentence of at most 200
characters, validated before it is written.
"""

import os

LINE = "My spam folder writes better love letters than my inbox \u2014 even the scammers think I'm worth replying to."


def validate(line):
    """Enforce the gate: single sentence, 1-200 chars, UTF-8 encodable."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    line.encode("utf-8")
    if not 1 <= len(line) <= 200:
        raise ValueError("line must be 1-200 characters, got %d" % len(line))
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line, no line breaks")
    terminators = sum(line.count(c) for c in ".!?")
    if terminators != 1:
        raise ValueError("line must be a single sentence, got %d terminators" % terminators)
    if line.rstrip()[-1] not in ".!?":
        raise ValueError("line must end with sentence punctuation")
    return True


def main():
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
