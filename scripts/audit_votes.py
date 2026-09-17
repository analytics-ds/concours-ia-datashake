#!/usr/bin/env python3
"""Audit des votes du concours IA : doublons d'identite, votants hors annuaire,
auto-votes, process orphelins, et recalcul du classement sous plusieurs regles.

Lecture seule : ne supprime jamais un vote. Usage :
    python3 scripts/audit_votes.py
Requiert SUPABASE_CONCOURS_ACCESS_TOKEN dans le .env du master 000 data.
"""
import json, os, re, subprocess, sys, unicodedata, collections, urllib.request

ENV = "/Users/damien.bo/Mon Drive (damien@datashake.fr)/000 Data/.claude/secrets/.env"
ANN = "/Users/damien.bo/Mon Drive (damien@datashake.fr)/000 Data/100🗺️ Areas/datashake/RH/Annuaire datashake - emails.md"
PROJECT = "ejkzpzftytpeladvcfnk"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def secret(key):
    for line in open(ENV, encoding="utf-8"):
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip()
    sys.exit(f"{key} absent de {ENV}")


def sql(query):
    # Cloudflare 1010 sans User-Agent navigateur : ne pas retirer l'en-tete.
    req = urllib.request.Request(
        f"https://api.supabase.com/v1/projects/{PROJECT}/database/query",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": "Bearer " + secret("SUPABASE_CONCOURS_ACCESS_TOKEN"),
                 "Content-Type": "application/json", "User-Agent": UA})
    return json.load(urllib.request.urlopen(req))


def fold(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def annuaire():
    out = {}
    for line in open(ANN, encoding="utf-8"):
        if line.startswith("|"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 2 and re.fullmatch(r"[a-z0-9._-]+@datashake\.fr", c[-1]):
                out[c[-1]] = c[0]
    return out


def data_js():
    js = "global.window={};require('%s/data.js');console.log(JSON.stringify({P:window.PROCESSES,T:window.TEAM}))" % REPO
    return json.loads(subprocess.check_output(["node", "-e", js]))


def main():
    ann, d = annuaire(), data_js()
    votes = sql("select id, process_id, voter_name, created_at from votes order by created_at;")
    P = {p["id"]: p for p in d["P"]}
    name2mail = {fold(n): e for e, n in ann.items()}
    print(f"{len(votes)} votes | {len(P)} process | annuaire {len(ann)} actifs | liste de vote {len(d['T'])}")

    for v in votes:
        n = v["voter_name"].strip().lower()
        v["who"] = n if "@" in n else (name2mail.get(fold(n)) or "NOM:" + fold(n))

    hors = [v for v in votes if "@" not in v["voter_name"]]
    print(f"\n== Votes entres hors interface (saisis en nom) : {len(hors)} ==")
    for v in hors:
        print(f"  {v['created_at'][:16]}  {v['voter_name']:<24} -> {v['who']:<28} {P.get(v['process_id'], {}).get('name', '?')[:40]}")

    g = collections.defaultdict(list)
    for v in votes:
        g[(v["process_id"], v["who"])].append(v)
    dbl = {k: vs for k, vs in g.items() if len(vs) > 1}
    print(f"\n== Doublons (meme personne, meme process, 2 identites) : {sum(len(v) - 1 for v in dbl.values())} votes en trop ==")
    for (pid, who), vs in dbl.items():
        print(f"  {who} x{len(vs)} sur « {P.get(pid, {}).get('name', '?')[:40]} »")
        for v in vs:
            print(f"      id={v['id']:<5} {v['voter_name']:<26} {v['created_at'][:16]}")

    print("\n== Votants hors annuaire (souvent des departs, legitimes a la date du vote) ==")
    for k, n in sorted(collections.Counter(v["who"] for v in votes if v["who"] not in ann).items()):
        print(f"  {k:<32} {n} vote(s)")

    def auto(v):
        p = P.get(v["process_id"])
        nom = ann.get(v["who"], "")
        return bool(p and nom and any(fold(a) == fold(nom) for a in p["authors"]))

    autos = [v for v in votes if auto(v)]
    print(f"\n== Auto-votes (l'auteur vote pour son propre process) : {len(autos)} ==")
    for v in autos:
        print(f"  {v['who']:<30} « {P[v['process_id']]['name'][:40]} » le {v['created_at'][:10]}")

    orph = [v for v in votes if v["process_id"] not in P]
    print(f"\n== Votes orphelins (process absent de data.js) : {len(orph)} ==")
    for v in orph:
        print(f"  id={v['id']} {v['process_id']} par {v['voter_name']} le {v['created_at'][:10]}")

    def board(vs, label):
        cnt = collections.Counter(v["process_id"] for v in vs)
        by = collections.defaultdict(lambda: {"procs": 0, "votes": 0, "bu": ""})
        for pid, p in P.items():
            e = by[" et ".join(p["authors"])]
            e["procs"] += 1; e["votes"] += cnt.get(pid, 0); e["bu"] = p["bu"]
        res = sorted(((k, v["procs"] * 10 + v["votes"] * 15, v["procs"], v["votes"]) for k, v in by.items()),
                     key=lambda x: (-x[1], -x[3]))
        print(f"\n===== {label} =====")
        for i, (k, s, pr, vo) in enumerate(res[:6], 1):
            print(f" {i:>2}. {s:>4} pts  {k:<34} {pr} process · {vo} adoptions")

    board(votes, "ACTUEL (ce qu'affiche le site)")
    seen, s1 = set(), []
    for v in votes:
        if (v["process_id"], v["who"]) not in seen:
            seen.add((v["process_id"], v["who"])); s1.append(v)
    board(s1, f"sans les doublons d'identite (-{len(votes) - len(s1)})")
    s2 = [v for v in s1 if not auto(v)]
    board(s2, f"sans doublons ni auto-votes (-{len(votes) - len(s2)})")


if __name__ == "__main__":
    main()
