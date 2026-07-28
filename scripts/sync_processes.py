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


def rich(blk, key):
    return "".join(t.get("plain_text", "") for t in blk.get(key, {}).get("rich_text", []))


def pitch(page_id):
    """Resume court du process = section "Interet" de la fiche Notion.

    Sert a la page de partage (vote.html) : le collegue qui recoit le lien doit
    comprendre a quoi sert l'outil sans ouvrir Notion. Vide si la fiche n'a pas
    de section Interet ou si l'appel echoue (le leaderboard marche sans).
    """
    try:
        req = urllib.request.Request(
            f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100",
            headers={"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2025-09-03"})
        blocks = json.load(urllib.request.urlopen(req)).get("results", [])
    except Exception:
        return ""

    parts, inside = [], False
    for b in blocks:
        t = b.get("type", "")
        if t.startswith("heading_"):
            head = rich(b, t).strip().lower()
            if inside:
                break
            inside = head.startswith("int") and "r" in head  # "Interet" / "Intérêt"
            continue
        if inside and t in ("paragraph", "bulleted_list_item", "numbered_list_item"):
            txt = rich(b, t).strip()
            if txt:
                parts.append(txt)

    text = " ".join(parts)
    if len(text) > 320:
        cut = text[:320].rsplit(" ", 1)[0]
        text = cut + "..."
    return text


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
        procs.append((pg["id"], name, all_people(p, "Auteur"), first_ms(p, "BU"),
                      pg.get("url", ""), pitch(pg["id"])))
    procs.sort(key=lambda x: x[1].lower())

    # author = 1er auteur (porte les points au classement), authors = tous (affichage des pp + noms)
    lines = []
    for pid, name, authors, bu, url, txt in procs:
        alist = ", ".join(f'"{jstr(a)}"' for a in authors)
        lines.append(f'  {{ id: "{pid}", name: "{jstr(name)}", author: "{jstr(authors[0])}", '
                     f'authors: [{alist}], bu: "{jstr(bu)}", notion: "{url}", '
                     f'pitch: "{jstr(txt)}" }},')
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
