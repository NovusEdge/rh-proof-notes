"""Lower bound on theorems never referenced anywhere in a Lean tree.

usage: python -I unused.py <srcDir>
A theorem counts as unreferenced when its last name component appears in the
tree only at its own declaration(s). Name collisions make dead theorems look
used, so the result under-counts.
"""
import os
import re
import sys
from collections import Counter

src = sys.argv[1]
DECL = re.compile(r"^(?:private |protected |noncomputable |@\[[^\]]*\] ?)*(theorem|lemma)\s+([^\s:({\[]+)")
TOKEN = re.compile(r"[^\W\d][\w'!?]*")


def files():
    for d, _, names in os.walk(src):
        for n in names:
            if n.endswith(".lean"):
                yield os.path.join(d, n)


declared, attributed, body = Counter(), set(), {}
for p in files():
    prev, cur = "", None
    with open(p, encoding="utf-8", errors="replace") as f:
        for raw in f:
            s = raw.strip()
            m = DECL.match(s)
            if m:
                cur = m.group(2).split(".")[-1]
                declared[cur] += 1
                body[cur] = body.get(cur, 0) + 1
                if s.startswith("@[") or prev.startswith("@["):
                    attributed.add(cur)
            elif cur and s and not raw[0].isspace():
                cur = None
            elif cur and s:
                body[cur] += 1
            if s:
                prev = s

seen = Counter()
for p in files():
    with open(p, encoding="utf-8", errors="replace") as f:
        for raw in f:
            for t in TOKEN.findall(raw):
                if t in declared:
                    seen[t] += 1

total = sum(declared.values())
dead = [n for n in declared if seen[n] <= declared[n] and n not in attributed]
dead_decls = sum(declared[n] for n in dead)
all_lines = sum(body.values())
dead_lines = sum(body[n] for n in dead)
print(f"theorems+lemmas={total} distinct_names={len(declared)} attributed_names={len(attributed)}")
print(f"unreferenced={dead_decls} ({100 * dead_decls / total:.1f}%)")
print(f"theorem_lines={all_lines} unreferenced_lines={dead_lines} ({100 * dead_lines / all_lines:.1f}%)")
