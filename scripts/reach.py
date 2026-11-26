"""Import reachability from Main, and renamed-clone window hashes.

usage: python -I reach.py <srcDir> <out_prefix> <root_module>...
"""
import os
import re
import sys
from hashlib import blake2b

src, out, roots = sys.argv[1], sys.argv[2], sys.argv[3:]
W = 6
IMPORT = re.compile(r"^(?:public |private )?(?:meta )?import (?:all )?([\w.«»']+)")
SKIP = re.compile(r"^(import|open|namespace|end|section|set_option|universe|variable|--)")
# ponytail: identifiers and numerals collapse to one token each, so any two
# statements with the same symbol skeleton match; this over-counts short lines,
# which the 6-line window offsets. A real Type-2 check needs the Lean parser.
IDENT = re.compile(r"[^\W\d][\w.'!?₀-₉]*")
NUM = re.compile(r"\d+")
WS = re.compile(r"\s+")

imports, nlines = {}, {}
with open(out + ".nwin", "w") as fw:
    for d, _, names in os.walk(src):
        for n in names:
            if not n.endswith(".lean"):
                continue
            p = os.path.join(d, n)
            mod = os.path.relpath(p, src)[:-5].replace(os.sep, ".")
            deps, hs, cnt = [], [], 0
            with open(p, encoding="utf-8", errors="replace") as f:
                for raw in f:
                    cnt += 1
                    s = raw.strip()
                    if not s:
                        continue
                    m = IMPORT.match(s)
                    if m:
                        deps.append(m.group(1))
                        continue
                    if SKIP.match(s):
                        continue
                    s = WS.sub("", NUM.sub("0", IDENT.sub("i", s)))
                    hs.append(blake2b(s.encode(), digest_size=8).hexdigest())
            imports[mod], nlines[mod] = deps, cnt
            for i in range(len(hs) - W + 1):
                fw.write(blake2b("".join(hs[i:i + W]).encode(), digest_size=8).hexdigest() + "\n")

seen, stack = set(), [r for r in roots if r in imports]
while stack:
    m = stack.pop()
    if m in seen:
        continue
    seen.add(m)
    stack.extend(d for d in imports[m] if d in imports and d not in seen)

total = sum(nlines.values())
reach = sum(nlines[m] for m in seen)
print(f"modules={len(imports)} reachable={len(seen)} ({100 * len(seen) / len(imports):.1f}%)")
print(f"lines={total} reachable_lines={reach} ({100 * reach / total:.1f}%)")
by = {}
for m in imports:
    k = m.split(".")[0]
    a = by.setdefault(k, [0, 0, 0, 0])
    a[0] += 1
    a[2] += nlines[m]
    if m in seen:
        a[1] += 1
        a[3] += nlines[m]
for k, a in sorted(by.items(), key=lambda kv: -kv[1][2]):
    print(f"{k}\tfiles={a[0]}\treach={a[1]}\tlines={a[2]}\treach_lines={a[3]}")
