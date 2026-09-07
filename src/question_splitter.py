"""Split mixed text/OCR documents into independently routable question blocks."""
from __future__ import annotations

import re


MARKER = re.compile(
    r"(?im)^(?P<indent>[ \t]*)(?:#{1,4}[ \t]*)?"
    r"(?:(?:question|ques(?:tion)?|q)[ \t]*[-:#.]?[ \t]*)?"
    r"(?P<number>\d{1,3})[.) :-]+(?=\S)"
)


def split_questions(text: str) -> list[str]:
    """Return question blocks; conservatively keep uncertain input as one block."""
    source = str(text).replace("\r\n", "\n").strip()
    if not source:
        return []
    matches = list(MARKER.finditer(source))
    if len(matches) < 2:
        return [source]

    numbers = [int(m.group("number")) for m in matches]
    monotonic = sum(b > a for a, b in zip(numbers, numbers[1:]))
    if monotonic < len(numbers) - 2:
        return [source]

    preamble = source[:matches[0].start()].strip()
    blocks: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        block = source[match.start():end].strip()
        if preamble and index == 0:
            block = preamble + "\n\n" + block
        if len(re.findall(r"\w+", block)) >= 3:
            blocks.append(block)
    return blocks if len(blocks) >= 2 else [source]
