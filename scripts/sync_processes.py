#!/usr/bin/env python3
# Sync auto du leaderboard : lit le Catalogue des projets IA (Notion) et regenere
# le bloc window.PROCESSES de data.js. TEAM et le reste du fichier ne sont pas touches.
# Lance par GitHub Actions (cron 30 min). Token Notion dans la variable d'env NOTION_TOKEN.
import os, json, urllib.request, urllib.error, pathlib

TOKEN = os.environ["NOTION_TOKEN"]
DS = "87d87923-5f43-4f57-a1e3-e82041d4dc00"  # data source "Catalogue des projets IA"
DATA = pathlib.Path(__file__).resolve().parent.parent / "data.js"


def query_catalogue():
    results, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        req = urllib.request.Request(
            f"https://api.notion.com/v1/data_sources/{DS}/query",
            data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {TOKEN}",
                     "Notion-Version": "2025-09-03",
                     "Content-Type": "application/json"},
            method="POST")
        d = json.load(urllib.request.urlopen(req))
        results += d.get("results", [])
        if d.get("has_more"):
            cursor = d.get("next_cursor")
        else:
            break
    return results


def title(props):
    for v in props.values():
        if v.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in v["title"]).strip()
    return ""


def first_ms(props, name):
    v = props.get(name, {})
    opts = v.get("multi_select", []) if v.get("type") == "multi_select" else []
    return opts[0]["name"] if opts else "?"


def all_people(props, name):
    """Tous les auteurs de la fiche, dans l'ordre du champ Notion."""
    v = props.get(name, {})
    ppl = v.get("people", []) if v.get("type") == "people" else []
    names = [p.get("name", "").strip() for p in ppl]
    return [n for n in names if n] or ["?"]


def jstr(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    cards = query_catalogue()
    procs = []
    for pg in cards:
        p = pg["properties"]
        name = title(p)
        if not name:
            continue
        procs.append((pg["id"], name, all_people(p, "Auteur"), first_ms(p, "BU"), pg.get("url", "")))
    procs.sort(key=lambda x: x[1].lower())

    # author = 1er auteur (porte les points au classement), authors = tous (affichage des pp + noms)
    lines = []
    for pid, name, authors, bu, url in procs:
        alist = ", ".join(f'"{jstr(a)}"' for a in authors)
        lines.append(f'  {{ id: "{pid}", name: "{jstr(name)}", author: "{jstr(authors[0])}", '
                     f'authors: [{alist}], bu: "{jstr(bu)}", notion: "{url}" }},')
    block = "window.PROCESSES = [\n" + "\n".join(lines) + "\n];\n" if procs else "window.PROCESSES = [\n];\n"

    content = DATA.read_text()
    before = content.split("window.PROCESSES", 1)[0]
    after = "window.TEAM" + content.split("window.TEAM", 1)[1]
    new = before + block + "\n" + after

    if new != content:
        DATA.write_text(new)
        print(f"CHANGED ({len(procs)} process)")
    else:
        print(f"NOCHANGE ({len(procs)} process)")


if __name__ == "__main__":
    main()
