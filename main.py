"""Two-Sentence Horror entry for make.fun competition
u-suroto-two-sentence-horror-acea9253.

Writes one horror story of exactly two sentences, up to 400 characters
total, to $MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).

Pure Python stdlib, deterministic, no network, no reads outside the repo.
The program refuses to emit anything outside 1-400 characters or anything
that is not exactly two sentences.
"""

import os
import re
import sys

STORY = (
    "I mounted the camera above the crib the day we brought our daughter "
    "home, and for three weeks the little screen in the kitchen showed her "
    "breathing softly beneath her blanket, rising and falling in the dark. "
    "Tonight the blanket lies flat and the crib is empty, the nursery door "
    "still locked from the inside \u2014 and the screen still shows her "
    "breathing."
)

MAX_CHARS = 400

# Split on a sentence-ending mark (. ! ?) followed by whitespace or end.
_SENTENCE_END = re.compile(r"[.!?](?=\s|$)")


def count_sentences(text):
    """Count sentences: a sentence ends at . ! or ? followed by space/end."""
    text = text.strip()
    if not text:
        return 0
    return len(_SENTENCE_END.findall(text))


def main():
    text = STORY.strip()

    if not 1 <= len(text) <= MAX_CHARS:
        print(
            "Refusing to emit: story is %d chars, must be 1-%d."
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    n = count_sentences(text)
    if n != 2:
        print(
            "Refusing to emit: story has %d sentences, must be exactly 2."
            % n,
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    print("Wrote %s (%d chars, %d sentences)." % (out_path, len(text), n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
