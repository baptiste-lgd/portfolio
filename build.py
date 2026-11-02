"""Construit le site : un dossier dans photos/ = une grille (un projet).
Nom du dossier : "2026 - Nom du projet"  ->  année 2026, titre "Nom du projet".
La première photo (ordre alphabétique) sert de couverture."""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
PHOTOS = ROOT / "photos"
OUT = ROOT / "dist"
EXT = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

def nat(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

projects = []
folders = sorted(PHOTOS.iterdir(), key=lambda p: nat(p.name)) if PHOTOS.exists() else []
for d in folders:
    if not d.is_dir() or d.name.startswith("."):
        continue
    imgs = sorted((f.name for f in d.iterdir() if f.suffix.lower() in EXT), key=nat)
    if not imgs:
        continue
    m = re.match(r"^\s*(\d{4})\s*[-_–]\s*(.+)$", d.name)
    year, title = (m.group(1), m.group(2).strip()) if m else ("", d.name.strip())
    projects.append({"title": title, "year": year,
                     "images": [f"photos/{d.name}/{n}" for n in imgs]})

projects.sort(key=lambda p: p["year"] or "0", reverse=True)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copy(ROOT / "index.html", OUT / "index.html")
if PHOTOS.exists():
    shutil.copytree(PHOTOS, OUT / "photos")
(OUT / "projects.json").write_text(json.dumps(projects, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(projects)} projet(s) :", ", ".join(p["title"] for p in projects))
