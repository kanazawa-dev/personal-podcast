#!/usr/bin/env python3
import os
import re
import yaml
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
EPISODES_DIR = ROOT / "episodes"
TEMPLATES_DIR = ROOT / "templates"
PUBLIC_DIR = ROOT / "public"
CONFIG_FILE = ROOT / "config.yml"

def parse_frontmatter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return meta, body
    return {}, text

def drive_direct_url(url):
    """Convierte un link compartido de Drive en link de descarga directa."""
    if "drive.google.com" not in url:
        return url
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    return url

def main():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    episodes = []
    for path in sorted(EPISODES_DIR.glob("*.md")):
        with open(path, "r", encoding="utf-8") as f:
            meta, body = parse_frontmatter(f.read())

        date = meta.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()

        audio_url = drive_direct_url(meta.get("audio_url", ""))

        episodes.append({
            "title": meta.get("title", path.stem),
            "date": date.strftime("%Y-%m-%d") if date else "",
            "pub_date": format_datetime(datetime.combine(date, datetime.min.time())) if date else "",
            "duration": meta.get("duration", "00:00"),
            "audio_url": audio_url,
            "audio_size": meta.get("audio_size", 0),
            "description": body,
            "guid": f"{config['base_url']}/episodes/{path.stem}",
        })

    # Ordenar por fecha descendente
    episodes.sort(key=lambda e: e["date"], reverse=True)

    PUBLIC_DIR.mkdir(exist_ok=True)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    # Generar feed RSS
    feed_tpl = env.get_template("feed.xml")
    with open(PUBLIC_DIR / "feed.xml", "w", encoding="utf-8") as f:
        f.write(feed_tpl.render(config=config, episodes=episodes))

    # Generar sitio web
    index_tpl = env.get_template("index.html")
    with open(PUBLIC_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_tpl.render(config=config, episodes=episodes))

    print(f"Generados {len(episodes)} episodios en {PUBLIC_DIR}")

if __name__ == "__main__":
    main()
