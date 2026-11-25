"""One-Line Laugh-Off — make.fun entry.

Writes the entry line to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output/entry.txt): one funny sentence, at most 200 characters.

Pure standard library only.
"""

import os

ENTRY_LINE = (
    "My spam folder writes better love letters than my inbox \u2014 "
    "even the scammers think I'm worth replying to."
)

CHAR_LIMIT = 200
SENTENCE_ENDINGS = ".!?"


def _must_be_text(value):
    """The entry has to be text before any other rule can run."""
    if not isinstance(value, str):
        raise ValueError("entry must be text, got %s" % type(value).__name__)


def _must_fit(value):
    """The entry has to fit the competition's character budget."""
    if not 1 <= len(value) <= CHAR_LIMIT:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (CHAR_LIMIT, len(value))
        )


def _must_be_one_sentence(value):
    """One sentence, one line, printable characters, ending punctuation."""
    if not value.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in value or "\r" in value:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        raise ValueError("entry must not contain control characters")
    marks = sum(value.count(mark) for mark in SENTENCE_ENDINGS)
    if marks != 1:
        raise ValueError(
            "entry must hold exactly one sentence, got %d terminators" % marks
        )
    if value.rstrip()[-1] not in SENTENCE_ENDINGS:
        raise ValueError("entry must end with sentence punctuation")


def check_entry(value):
    """Run every gate rule from RULES.txt over the entry line."""
    _must_be_text(value)
    value.encode("utf-8")
    _must_fit(value)
    _must_be_one_sentence(value)
    return value


def write_entry(value, output_dir):
    """Write the validated line and prove the disk copy matches it."""
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(value)
    with open(target, "r", encoding="utf-8") as handle:
        saved = handle.read()
    if saved != value:
        raise ValueError("entry.txt on disk differs from the validated line")
    return target


def main():
    line = check_entry(ENTRY_LINE)
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = write_entry(line, directory)
    print(line)
    print("chars: %d (limit %d) -> %s" % (len(line), CHAR_LIMIT, target))


if __name__ == "__main__":
    main()
