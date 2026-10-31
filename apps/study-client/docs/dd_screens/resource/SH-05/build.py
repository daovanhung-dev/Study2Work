#!/usr/bin/env python3
"""Build editable SH-05 state-view SVGs and deterministic PNG previews."""

from __future__ import annotations

import html
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
FONT = "Noto Sans, Arial, sans-serif"

STATES = [
    {
        "id": "ACCESS_DENIED",
        "eyebrow": "QUYỀN TRUY CẬP",
        "headline": ("Bạn chưa có quyền", "truy cập"),
        "body": (
            "Tài khoản hiện tại không thể mở trang này.",
            "Bạn có thể quay lại nơi vừa đến hoặc về trang chủ.",
        ),
        "mobile_body": (
            "Tài khoản này không thể mở trang này.",
            "Bạn có thể quay lại hoặc về trang chủ.",
        ),
        "cta": "Quay lại",
    },
    {
        "id": "SESSION_REQUIRED",
        "eyebrow": "XÁC THỰC PHIÊN",
        "headline": ("Phiên đăng nhập cần", "được xác thực lại"),
        "body": (
            "Đăng nhập lại để tiếp tục từ trang bạn đang mở.",
            "Nếu đường dẫn còn hợp lệ, bạn sẽ được đưa trở lại.",
        ),
        "mobile_body": (
            "Đăng nhập lại để tiếp tục.",
            "Bạn sẽ trở lại nếu đường dẫn an toàn.",
        ),
        "cta": "Đăng nhập lại",
    },
    {
        "id": "TOKEN_REFRESH_FAILED",
        "eyebrow": "KHÔI PHỤC PHIÊN",
        "headline": ("Chưa thể khôi phục", "phiên đăng nhập"),
        "body": (
            "Không thể xác nhận phiên hiện tại.",
            "Đăng nhập lại để tiếp tục an toàn.",
        ),
        "mobile_body": (
            "Không thể xác nhận phiên hiện tại.",
            "Đăng nhập lại để tiếp tục an toàn.",
        ),
        "cta": "Đăng nhập lại",
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(x: float, y: float, value: str, size: int, color: str, weight: int = 400,
         anchor: str = "start", spacing: float | None = None) -> str:
    letter = f' letter-spacing="{spacing}px"' if spacing is not None else ""
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
        f'font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}"'
        f'{letter}>{esc(value)}</text>'
    )


def marker(number: int, cx: float, cy: float, tx: float, ty: float, size: int = 24) -> str:
    outer_radius = size / 2
    inner_radius = outer_radius - 1.6
    font_size = 12 if size >= 23 else 10.5
    text_offset = 4.4 if size >= 23 else 3.8
    return (
        f'<g aria-hidden="true" class="element-marker element-marker-{number}">'
        f'<path d="M {cx} {cy} L {tx} {ty}" fill="none" stroke="#073B57" '
        f'stroke-width="1.35" stroke-linecap="round" stroke-opacity="0.72"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{outer_radius}" fill="#FFFFFF" opacity="0.96"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{inner_radius}" fill="#073B57" stroke="#FFFFFF" stroke-width="1.2"/>'
        f'<text x="{cx}" y="{cy + text_offset}" fill="#FFFFFF" font-family="{FONT}" '
        f'font-size="{font_size}px" font-weight="700" text-anchor="middle">{number}</text>'
        "</g>"
    )


def svg_open(width: int, height: int, title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(desc)}</desc>',
        '<defs>',
        '<filter id="haloShadow" x="-20%" y="-20%" width="140%" height="150%">',
        '<feDropShadow dx="0" dy="15" stdDeviation="18" flood-color="#17324D" flood-opacity="0.075"/>',
        '</filter>',
        '</defs>',
    ]


def header_desktop() -> list[str]:
    return [
        '<rect width="1440" height="96" fill="#FFFFFF"/>',
        '<path d="M0 95.5H1440" stroke="#D4E2E9" stroke-opacity="0.76"/>',
        '<g aria-label="Study home link">',
        '<rect x="160" y="30" width="38" height="38" rx="11" fill="#0B5F8A"/>',
        '<path d="M171.5 39.5h10.7l5.3 5.2v14.2h-16z" fill="none" stroke="#FFFFFF" '
        'stroke-width="1.7" stroke-linejoin="round"/>',
        '<path d="M182.1 39.8v5.1h5.1M175.2 50.1h8.3M175.2 54.2h8.3" fill="none" '
        'stroke="#FFFFFF" stroke-width="1.55" stroke-linecap="round"/>',
        '</g>',
        text(210, 58, "Study", 23, "#073B57", 700),
    ]


def header_mobile(width: int) -> list[str]:
    x = 24 if width == 390 else 16
    return [
        '<rect width="100%" height="72" fill="#FFFFFF"/>',
        f'<path d="M0 71.5H{width}" stroke="#D4E2E9" stroke-opacity="0.76"/>',
        f'<g aria-label="Study home link"><rect x="{x}" y="18" width="36" height="36" rx="10" fill="#0B5F8A"/>',
        f'<path d="M{x + 11} 26.5h10l5 5v13h-15z" fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-linejoin="round"/>',
        f'<path d="M{x + 21} 26.8v4.8h4.8M{x + 14} 37h8M{x + 14} 41h8" fill="none" stroke="#FFFFFF" stroke-width="1.45" stroke-linecap="round"/>',
        '</g>',
        text(x + 48, 43, "Study", 22, "#073B57", 700),
    ]


def illustration_desktop() -> list[str]:
    return [
        '<g id="element-12-orbit-arcs" aria-hidden="true" fill="none" stroke="#43A5C5" stroke-width="2">',
        '<path d="M830 495C802 420 824 333 891 275c42-37 92-54 147-57" stroke-opacity="0.38"/>',
        '<path d="M1108 226c83 14 142 71 171 155" stroke-opacity="0.33"/>',
        '<path d="M1294 499c-18 100-86 174-184 211" stroke-opacity="0.34"/>',
        '<path d="M956 720c-81-27-132-82-150-153" stroke-opacity="0.28"/>',
        '<circle cx="890" cy="308" r="3.5" fill="#43A5C5" stroke="none"/>',
        '<circle cx="1246" cy="341" r="3.5" fill="#43A5C5" stroke="none"/>',
        '<circle cx="1197" cy="674" r="3" fill="#43A5C5" stroke="none"/>',
        '</g>',
        '<g id="element-08-halo" aria-hidden="true">',
        '<circle cx="1060" cy="455" r="180" fill="#E8F4FA" filter="url(#haloShadow)"/>',
        '<circle cx="1060" cy="455" r="145" fill="#FFFFFF" opacity="0.48"/>',
        '<circle cx="1060" cy="455" r="117" fill="none" stroke="#D4E2E9" stroke-opacity="0.52"/>',
        '<circle cx="946" cy="359" r="5" fill="#43A5C5"/>',
        '<circle cx="1192" cy="476" r="4" fill="#43A5C5"/>',
        '<circle cx="1089" cy="293" r="3.5" fill="#0B5F8A" opacity="0.72"/>',
        '</g>',
        '<g id="element-09-open-threshold" aria-hidden="true">',
        '<ellipse cx="1086" cy="629" rx="125" ry="15" fill="#D8EAF1" opacity="0.74"/>',
        '<path d="M992 626V430a94 94 0 0 1 188 0v196z" fill="#FFFFFF" stroke="#0B5F8A" stroke-width="5" stroke-linejoin="round"/>',
        '<path d="M1014 626V432a72 72 0 0 1 144 0v194" fill="none" stroke="#D4E2E9" stroke-width="2"/>',
        '<path d="M1034 626V435a52 52 0 0 1 104 0v191" fill="none" stroke="#E8F4FA" stroke-width="8" stroke-linecap="round"/>',
        '<path d="M1061 626V445a25 25 0 0 1 50 0v181" fill="none" stroke="#43A5C5" stroke-opacity="0.55" stroke-width="2"/>',
        '</g>',
        '<g id="element-10-interrupted-route" aria-hidden="true">',
        '<path d="M817 624H925" fill="none" stroke="#43A5C5" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 9"/>',
        '</g>',
        '<g id="element-11-route-stop-node" aria-hidden="true">',
        '<circle cx="942" cy="624" r="13" fill="#FFFFFF" stroke="#0B5F8A" stroke-width="3"/>',
        '<circle cx="942" cy="624" r="4" fill="#43A5C5"/>',
        '</g>',
    ]


def desktop_svg(state: dict[str, object], annotated: bool) -> str:
    state_id = str(state["id"])
    title = f"SH-05 {state_id} — {'annotated' if annotated else 'clean'} desktop view"
    parts = svg_open(1440, 960, title, "Study access recovery state view; the image is a design handoff and contains no live account data.")
    parts += ['<rect width="1440" height="960" fill="#F6FAFC"/>']
    parts += header_desktop()
    parts += illustration_desktop()
    parts += [
        '<g id="element-03-eyebrow">',
        text(160, 278, str(state["eyebrow"]), 13, "#0B5F8A", 700, spacing=0.55),
        '</g>',
        '<g id="element-04-headline">',
        text(160, 350, str(state["headline"][0]), 44, "#073B57", 700),
        text(160, 402, str(state["headline"][1]), 44, "#073B57", 700),
        '</g>',
        '<g id="element-05-supporting-copy">',
        text(160, 455, str(state["body"][0]), 17, "#536A7A", 400),
        text(160, 483, str(state["body"][1]), 17, "#536A7A", 400),
        '</g>',
        '<g id="element-06-primary-action" aria-label="Primary action button">',
        '<rect x="160" y="560" width="224" height="56" rx="9" fill="#0B5F8A"/>',
        text(272, 595, str(state["cta"]), 16, "#FFFFFF", 600, anchor="middle"),
        '</g>',
        '<g id="element-07-home-link" aria-label="Secondary home navigation link">',
        text(160, 668, "Về trang chủ", 15, "#0B5F8A", 600),
        '<path d="M259 663h11m-4-4 4 4-4 4" fill="none" stroke="#0B5F8A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        '</g>',
    ]
    if annotated:
        points = [
            (1, 138, 32, 160, 49), (2, 304, 26, 282, 45),
            (3, 138, 261, 160, 276), (4, 138, 327, 160, 345),
            (5, 138, 444, 160, 455), (6, 138, 566, 160, 582),
            (7, 138, 646, 160, 662), (8, 851, 270, 881, 290),
            (9, 968, 307, 991, 328), (10, 798, 608, 818, 624),
            (11, 928, 660, 940, 638), (12, 1262, 247, 1241, 270),
        ]
        parts.append('<g id="annotation-layer" aria-label="Element number markers">')
        parts.extend(marker(*point) for point in points)
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def mobile_svg(state: dict[str, object], annotated: bool, width: int = 390) -> str:
    height = 844
    gutter = 24 if width == 390 else 16
    main_width = width - gutter * 2
    scale = 0.58 if width == 390 else 0.51
    translate_x = width / 2 - 1060 * scale
    translate_y = 665 - 455 * scale
    headline_size = 32 if width == 390 else 28
    title = f"SH-05 {state['id']} — {'annotated' if annotated else 'clean'} mobile view"
    parts = svg_open(width, height, title, "Study access recovery state view adapted to a narrow screen; no live account data is shown.")
    parts += [f'<rect width="{width}" height="{height}" fill="#F6FAFC"/>']
    parts += header_mobile(width)
    parts += [
        '<g transform="translate(' + f'{translate_x:.2f} {translate_y:.2f}' + ') scale(' + f'{scale:.3f}' + ')" aria-hidden="true">',
        *illustration_desktop(),
        '</g>',
        '<g id="element-03-eyebrow">',
        text(gutter, 116, str(state["eyebrow"]), 12, "#0B5F8A", 700, spacing=0.45),
        '</g>',
        '<g id="element-04-headline">',
        text(gutter, 166, str(state["headline"][0]), headline_size, "#073B57", 700),
        text(gutter, 204, str(state["headline"][1]), headline_size, "#073B57", 700),
        '</g>',
        '<g id="element-05-supporting-copy">',
        text(gutter, 257, str(state["mobile_body"][0]), 16 if width == 390 else 15, "#536A7A", 400),
        text(gutter, 282, str(state["mobile_body"][1]), 16 if width == 390 else 15, "#536A7A", 400),
        '</g>',
        '<g id="element-06-primary-action" aria-label="Primary action button">',
        f'<rect x="{gutter}" y="328" width="{main_width}" height="54" rx="9" fill="#0B5F8A"/>',
        text(width / 2, 362, str(state["cta"]), 16, "#FFFFFF", 600, anchor="middle"),
        '</g>',
        '<g id="element-07-home-link" aria-label="Secondary home navigation link">',
        text(gutter, 420, "Về trang chủ", 15, "#0B5F8A", 600),
        '<path d="M' + f'{gutter + 99}' + ' 415h11m-4-4 4 4-4 4" fill="none" stroke="#0B5F8A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        '</g>',
    ]
    if annotated:
        if width == 390:
            points = [
                (1, 12, 12, 24, 25), (2, 177, 12, 150, 31),
                (3, 12, 98, 24, 112), (4, 12, 151, 24, 164),
                (5, 12, 247, 24, 258), (6, 12, 355, 24, 355),
                (7, 12, 414, 24, 414), (8, 53, 553, 88, 571),
                (9, 141, 579, 154, 597), (10, 32, 764, 55, 764),
                (11, 126, 804, 126, 766), (12, 337, 536, 320, 554),
            ]
        else:
            points = [
                (1, 4, 12, 16, 24), (2, 147, 12, 136, 29),
                (3, 4, 98, 16, 112), (4, 4, 151, 16, 164),
                (5, 4, 247, 16, 258), (6, 4, 345, 16, 355),
                (7, 4, 414, 16, 414), (8, 42, 557, 70, 571),
                (9, 117, 584, 128, 602), (10, 25, 765, 45, 764),
                (11, 104, 796, 110, 767), (12, 278, 538, 260, 553),
            ]
        parts.append('<g id="annotation-layer" aria-label="Element number markers">')
        parts.extend(marker(*point, size=20) for point in points)
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def render_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    if not CHROME:
        raise RuntimeError("Không tìm thấy Chrome/Chromium để xuất PNG.")
    with tempfile.TemporaryDirectory(prefix="study-sh05-chrome-") as profile:
        command = [
            CHROME,
            "--headless=new",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--user-data-dir={profile}",
            f"--screenshot={png_path}",
            svg_path.as_uri(),
        ]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0 or not png_path.exists():
        raise RuntimeError(f"Chrome không xuất được {png_path.name}: {result.stderr[-1200:]}")


def build(render: bool = True) -> list[Path]:
    outputs: list[Path] = []
    for state in STATES:
        state_id = str(state["id"])
        for variant, source in (("desktop", desktop_svg), ("mobile", mobile_svg)):
            width, height = (1440, 960) if variant == "desktop" else (390, 844)
            for kind, annotated in (("clean", False), ("annotated", True)):
                stem = f"SH-05_{state_id}_{variant}_{kind}"
                svg_path = ROOT / f"{stem}.svg"
                png_path = ROOT / f"{stem}.png"
                svg = source(state, annotated) if variant == "desktop" else source(state, annotated, width)
                svg_path.write_text(svg + "\n", encoding="utf-8")
                outputs.append(svg_path)
                if render:
                    render_png(svg_path, png_path, width, height)
                    outputs.append(png_path)
    return outputs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-render", action="store_true", help="Write SVG sources without PNG rendering")
    args = parser.parse_args()
    written = build(render=not args.no_render)
    print(f"Wrote {len(written)} assets under {ROOT}")
