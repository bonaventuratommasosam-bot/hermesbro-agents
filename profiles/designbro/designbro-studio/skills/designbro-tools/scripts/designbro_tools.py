#!/usr/bin/env python3
"""DesignBro Studio tools — logo, palette, typography, brand kit."""
import argparse
import json
from datetime import datetime
from pathlib import Path

from brand_config import brand_context, load

SOCIAL_DIMS = {
    "instagram_post": "1080×1080",
    "instagram_story": "1080×1920",
    "facebook_cover": "820×312",
    "linkedin_banner": "1584×396",
    "x_header": "1500×500",
}


def logo_concept(brand: str, industry: str, keywords: str, style: str = "modern") -> dict:
    return {
        "tool": "logo_concept",
        "timestamp": datetime.now().isoformat(),
        "brand": brand,
        "industry": industry,
        "keywords": keywords,
        "style": style,
        "concepts": [
            {
                "name": "Minimal",
                "description": f"Segno grafico essenziale per {brand} — {keywords}",
                "colors": ["#1a1a2e", "#e94560", "#0f3460"],
                "font": "Inter",
            },
            {
                "name": "Typographic",
                "description": f"Wordmark basato sul nome {brand}",
                "colors": ["#2d3436", "#dfe6e9", "#0984e3"],
                "font": "Playfair Display",
            },
            {
                "name": "Abstract",
                "description": f"Simbolo astratto che evoca {keywords}",
                "colors": ["#6c5ce7", "#a29bfe", "#fd79a8"],
                "font": "Space Grotesk",
            },
        ],
        "tips": [
            "Scalabile: testa a 16px e a 2000px",
            "Monocromatico: deve funzionare in bianco e nero",
            "Memorabile: ridisegnabile a memoria",
        ],
    }


def color_palette(base_color: str, mood: str = "professional", style: str = "modern") -> dict:
    names = {
        "#1a1a2e": "Dark Navy",
        "#e94560": "Coral Red",
        "#0f3460": "Deep Blue",
        "#6c5ce7": "Purple",
        "#00b894": "Mint Green",
        "#fdcb6e": "Golden Yellow",
    }
    return {
        "tool": "color_palette",
        "timestamp": datetime.now().isoformat(),
        "base": base_color,
        "base_name": names.get(base_color.lower(), base_color),
        "mood": mood,
        "style": style,
        "palette": {
            "primary": base_color,
            "secondary": "#dfe6e9",
            "accent": "#e94560",
            "dark": "#1a1a2e",
            "light": "#ffffff",
        },
        "usage": {
            "primary": "Titoli, CTA, elementi chiave",
            "secondary": "Sfondi, bordi, divisori",
            "accent": "Highlight, notifiche",
        },
    }


def typography(industry: str, style: str = "modern") -> dict:
    pairings = {
        "food": "Playfair Display + Inter",
        "tech": "Space Grotesk + JetBrains Mono",
        "fashion": "Cormorant Garamond + Montserrat",
        "finance": "IBM Plex Serif + IBM Plex Sans",
        "legal": "Lora + Source Sans Pro",
        "retail": "DM Sans + Inter",
    }
    return {
        "tool": "typography",
        "timestamp": datetime.now().isoformat(),
        "industry": industry,
        "style": style,
        "pairing": pairings.get(industry, pairings["tech"]),
        "rule": "Max 2 font. Uno per titoli, uno per corpo.",
        "tips": [
            "Corpo: 16-18px web",
            "Line height: 1.5-1.6",
            "Lunghezza riga: 50-75 caratteri",
        ],
    }


def brand_guidelines(brand: str, industry: str, primary: str) -> dict:
    return {
        "tool": "brand_guidelines",
        "timestamp": datetime.now().isoformat(),
        "brand": brand,
        "sections": [
            "Logo usage (min size, clear space, don'ts)",
            f"Color system — primary {primary}",
            f"Typography — industry {industry}",
            "Voice & tone (2-3 adjectives)",
            "Social templates & dimensions",
        ],
        "status": "outline_ready",
    }


def social_dimensions() -> dict:
    return {"tool": "social_dimensions", "formats": SOCIAL_DIMS}


def main() -> None:
    p = argparse.ArgumentParser(description="DesignBro Studio Tools")
    p.add_argument(
        "tool",
        help="logo_concept,color_palette,typography,brand_guidelines,social_dimensions",
    )
    p.add_argument("--brand", default="")
    p.add_argument("--industry", default="")
    p.add_argument("--keywords", default="")
    p.add_argument("--style", default="")
    p.add_argument("--base_color", default="")
    p.add_argument("--mood", default="")
    args = p.parse_args()

    ctx = brand_context(load())
    brand = args.brand or ctx["brand"]
    industry = args.industry or ctx["industry"]
    keywords = args.keywords or ctx["keywords"] or "quality,trust"
    style = args.style or ctx["style"]
    base = args.base_color or ctx["primary_color"]
    mood = args.mood or ctx["mood"]

    tools = {
        "logo_concept": lambda: logo_concept(brand, industry, keywords, style),
        "color_palette": lambda: color_palette(base, mood, style),
        "typography": lambda: typography(industry, style),
        "brand_guidelines": lambda: brand_guidelines(brand, industry, base),
        "social_dimensions": social_dimensions,
    }
    fn = tools.get(args.tool)
    print(json.dumps(fn() if fn else {"error": f"Unknown: {args.tool}"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()