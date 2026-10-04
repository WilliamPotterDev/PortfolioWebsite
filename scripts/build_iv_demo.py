"""Build a short IV surface demo GIF from portfolio screenshots."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public" / "projects"
OUT = PUBLIC / "iv-surface-demo.gif"
W, H = 960, 540


def font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\consolab.ttf" if bold else r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\courbd.ttf" if bold else r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def solid(color=(11, 11, 11)) -> Image.Image:
    return Image.new("RGB", (W, H), color)


def fit_contain(src: Image.Image, max_w: int, max_h: int) -> Image.Image:
    img = src.convert("RGB")
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (max_w, max_h), (11, 11, 11))
    canvas.paste(img, ((max_w - img.width) // 2, (max_h - img.height) // 2))
    return canvas


def title_card(title: str, subtitle: str = "") -> Image.Image:
    img = solid()
    draw = ImageDraw.Draw(img)
    title_f = font(34, bold=True)
    sub_f = font(18)
    tw = draw.textbbox((0, 0), title, font=title_f)
    draw.text(((W - (tw[2] - tw[0])) / 2, H * 0.38), title, fill=(255, 255, 255), font=title_f)
    if subtitle:
        sw = draw.textbbox((0, 0), subtitle, font=sub_f)
        draw.text(
            ((W - (sw[2] - sw[0])) / 2, H * 0.38 + 50),
            subtitle,
            fill=(180, 180, 180),
            font=sub_f,
        )
    return img


def captioned(shot: Image.Image, caption: str) -> Image.Image:
    base = solid()
    content = fit_contain(shot, W - 60, H - 90)
    base.paste(content, (30, 22))
    draw = ImageDraw.Draw(base)
    cap_f = font(16)
    cw = draw.textbbox((0, 0), caption, font=cap_f)
    draw.text(((W - (cw[2] - cw[0])) / 2, H - 42), caption, fill=(220, 220, 220), font=cap_f)
    return base


def fade_pair(a: Image.Image, b: Image.Image, steps: int = 8) -> list[Image.Image]:
    frames = []
    for i in range(1, steps + 1):
        frames.append(Image.blend(a, b, i / steps))
    return frames


def main() -> None:
    surface = Image.open(PUBLIC / "iv-surface.png")
    smile = Image.open(PUBLIC / "iv-surface-smile.png")

    cards = [
        title_card("Implied Volatility Surface", "William Potter  ·  Python · Options · Black-Scholes"),
        captioned(surface, "Live options chain  →  inverse Black-Scholes  →  3D IV surface"),
        captioned(smile, "Volatility smile by expiry with liquidity-filtered strikes"),
        title_card("Interactive demo", "Open app on the Projects page"),
    ]

    # duration per frame in ms
    frames: list[Image.Image] = []
    durations: list[int] = []

    def add_hold(img: Image.Image, ms: int):
        frames.append(img.copy())
        durations.append(ms)

    add_hold(cards[0], 2200)
    for i in range(len(cards) - 1):
        fades = fade_pair(cards[i], cards[i + 1], steps=6)
        for f in fades:
            frames.append(f)
            durations.append(70)
        add_hold(cards[i + 1], 3600 if i < len(cards) - 2 else 2400)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB, {len(frames)} frames)")


if __name__ == "__main__":
    main()
