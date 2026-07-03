#!/usr/bin/env python3
"""Update content/*/_index.md to icon + images.primary (client-owned assets)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
IMAGES_DIR = ROOT / "static" / "images"

SECTIONS: dict[str, str] = {
    "promotions": "zumi-mondays-thursdays-roll-promos.png",
    "appetizers": "niwatori-gyoza.png",
    "sashimi": "ahi-tuna-sashimi.png",
    "nigiri": "maguro-nigiri.png",
    "maki-roll": "ahi-tuna-maki.png",
    "uramaki": "cali-crunch-roll.png",
    "veggie-roll": "green-forest-roll.png",
    "add-ons": "hiyashi-wakame.png",
}

WEIGHTS: dict[str, str] = {
    "promotions": "1",
    "appetizers": "2",
    "sashimi": "3",
    "nigiri": "4",
    "maki-roll": "5",
    "uramaki": "6",
    "veggie-roll": "7",
    "add-ons": "8",
}


def img(name: str) -> str:
    return f"images/{name}"


def body_after_frontmatter(raw: str) -> str:
    if raw.count("---") < 2:
        return raw.strip()
    return raw.split("---", 2)[2].strip()


def update_section_index(section: str, image_file: str) -> None:
    path = CONTENT / section / "_index.md"
    if not path.exists():
        return
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"^title:\s*(.+)$", raw, re.M)
    title = title_m.group(1).strip().strip('"') if title_m else section.replace("-", " ").title()
    weight = WEIGHTS.get(section, "1")
    body = body_after_frontmatter(raw)

    lines = [
        "---",
        f"title: {title}",
        f"weight: {weight}",
        f"icon: {img(image_file)}",
        "images:",
        f"    primary: {img(image_file)}",
        "---",
    ]
    if body:
        lines.extend(["", body])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def update_home_index() -> None:
    path = CONTENT / "_index.md"
    body = body_after_frontmatter(path.read_text(encoding="utf-8"))
    if not body.strip():
        body = "<p>Zumi Sushi & More – fresh sushi and Japanese-inspired cuisine.</p>"
    text = (
        "---\n"
        'title: "Zumi Sushi & More"\n'
        f"image: {img('zumi-chefs-roll.png')}\n"
        "images:\n"
        f"    - image: {img('zumi-chefs-roll.png')}\n"
        f"    - image: {img('atlantic-royale-roll.png')}\n"
        f"    - image: {img('ahi-tuna-sashimi.png')}\n"
        f"    - image: {img('maguro-nigiri.png')}\n"
        "slideshow:\n"
        f"    - image: {img('zumi-chefs-roll.png')}\n"
        f"    - image: {img('dragon-bite-roll.png')}\n"
        f"    - image: {img('atlantic-royale-roll.png')}\n"
        f"    - image: {img('ahi-tuna-sashimi.png')}\n"
        f"    - image: {img('zumi-mondays-thursdays-roll-promos.png')}\n"
        f"    - image: {img('las-vegas-roll.png')}\n"
        "---"
    )
    text += f"\n\n{body}\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    slideshow = [
        "zumi-chefs-roll.png",
        "dragon-bite-roll.png",
        "atlantic-royale-roll.png",
        "ahi-tuna-sashimi.png",
        "zumi-mondays-thursdays-roll-promos.png",
        "las-vegas-roll.png",
    ]
    missing = [f"{s} → {f}" for s, f in SECTIONS.items() if not (IMAGES_DIR / f).exists()]
    for name in ["zumi-chefs-roll.png", "atlantic-royale-roll.png", "maguro-nigiri.png"] + slideshow:
        if not (IMAGES_DIR / name).exists():
            missing.append(f"home → {name}")

    if missing:
        print("Missing images:")
        for line in missing:
            print(f"  {line}")
        return

    for section, image_file in SECTIONS.items():
        update_section_index(section, image_file)

    update_home_index()

    credits = "\n".join(
        f"- {name} — Zumi Sushi & More (client-owned)" for name in sorted(set(SECTIONS.values()))
    )
    (IMAGES_DIR / "IMAGE_CREDITS.txt").write_text(
        "Section photos (client-owned menu photography):\n" + credits + "\n",
        encoding="utf-8",
    )
    print("Section headers updated.")


if __name__ == "__main__":
    main()
