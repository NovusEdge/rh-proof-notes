"""Stream a Lean tree and emit line / 6-line-window hashes for sort|uniq.

usage: python -I dry.py <root> <out_prefix>
Memory stays flat: nothing is held across files except counters.
"""
import os
import re
import sys
from hashlib import blake2b

root, out = sys.argv[1], sys.argv[2]
W = 6
BOILER = re.compile(r"^(import|open|namespace|end|section|set_option|universe|variable|noncomputable section)\b")
DECL = re.compile(r"^(?:private |protected |noncomputable |@\[[^\]]*\] ?)*(theorem|lemma|def|instance|abbrev|structure|class|inductive|example)\b")
WS = re.compile(r"\s+")


def h(s):
    return blake2b(s.encode(), digest_size=8).hexdigest()


c = dict(files=0, lines=0, blank=0, comment=0, boiler=0, code=0, bytes=0)
decls = {}
with open(out + ".lines", "w") as fl, open(out + ".win", "w") as fw, open(out + ".files", "w") as ff:
    for d, _, names in os.walk(root):
        for n in names:
            if not n.endswith(".lean"):
                continue
            p = os.path.join(d, n)
            c["files"] += 1
            c["bytes"] += os.path.getsize(p)
            code, depth = [], 0
            with open(p, encoding="utf-8", errors="replace") as f:
                for raw in f:
                    c["lines"] += 1
                    s = WS.sub(" ", raw).strip()
                    if not s:
                        c["blank"] += 1
                        continue
                    if depth or s.startswith("/-"):
                        c["comment"] += 1
                        depth += s.count("/-") - s.count("-/")
                        depth = max(depth, 0)
                        continue
                    if s.startswith("--"):
                        c["comment"] += 1
                        continue
                    if BOILER.match(s):
                        c["boiler"] += 1
                        continue
                    m = DECL.match(s)
                    if m:
                        decls[m.group(1)] = decls.get(m.group(1), 0) + 1
                    code.append(s)
            c["code"] += len(code)
            hs = [h(s) for s in code]
            if hs:
                fl.write("\n".join(hs) + "\n")
                # whole-file body hash: files identical apart from comments/imports/whitespace
                ff.write(h("".join(hs)) + " " + str(len(hs)) + "\n")
            for i in range(len(hs) - W + 1):
                fw.write(h("".join(hs[i:i + W])) + "\n")

for k, v in c.items():
    print(f"{k}\t{v}")
for k, v in sorted(decls.items(), key=lambda kv: -kv[1]):
    print(f"decl:{k}\t{v}")
