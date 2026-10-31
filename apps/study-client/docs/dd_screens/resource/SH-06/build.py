#!/usr/bin/env python3
"""Build editable SH-06 design views and deterministic PNG previews."""

from __future__ import annotations

import html
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
FONT = "Noto Sans, Arial, sans-serif"
PAPER = "SH-06_paper-illustration.png"

STATES = [
    {
        "id": "ROUTE_NOT_FOUND",
        "eyebrow": "TRANG KHÔNG KHẢ DỤNG",
        "headline": ("Trang này không", "tồn tại"),
        "body": (
            "Địa chỉ có thể không chính xác hoặc đã thay đổi.",
            "Hãy tìm khóa học từ danh sách bên dưới.",
        ),
        "mobile_body": (
            "Địa chỉ có thể không chính xác.",
            "Hãy tìm khóa học từ danh sách bên dưới.",
        ),
        "compact_body": (
            "Địa chỉ này có thể đã thay đổi.",
            "Hãy tìm khóa học từ danh sách.",
        ),
    },
    {
        "id": "RESOURCE_NOT_FOUND",
        "eyebrow": "KHÓA HỌC KHÔNG KHẢ DỤNG",
        "headline": ("Không tìm thấy", "khóa học này"),
        "body": (
            "Khóa học này không thể hiển thị tại địa chỉ hiện tại.",
            "Bạn có thể chọn một khóa học khác.",
        ),
        "mobile_body": (
            "Khóa học này hiện không khả dụng.",
            "Bạn có thể chọn một khóa học khác.",
        ),
        "compact_body": (
            "Khóa học này hiện không khả dụng.",
            "Bạn có thể chọn khóa học khác.",
        ),
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(
    x: float,
    y: float,
    value: str,
    size: float,
    color: str,
    weight: int = 400,
    anchor: str = "start",
    spacing: float | None = None,
) -> str:
    letter = f' letter-spacing="{spacing}px"' if spacing is not None else ""
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
        f'font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}"'
        f'{letter}>{esc(value)}</text>'
    )


def marker(number: int, cx: float, cy: float, tx: float, ty: float, size: int = 24) -> str:
    outer = size / 2
    inner = outer - 1.6
    font_size = 12 if size >= 23 else 10.5
    baseline = 4.4 if size >= 23 else 3.8
    return (
        f'<g aria-hidden="true" class="element-marker element-marker-{number}">'
        f'<path d="M {cx} {cy} L {tx} {ty}" fill="none" stroke="#073B57" '
        'stroke-width="1.35" stroke-linecap="round" stroke-opacity="0.72"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{outer}" fill="#FFFFFF" opacity="0.96"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{inner}" fill="#073B57" stroke="#FFFFFF" stroke-width="1.2"/>'
        f'<text x="{cx}" y="{cy + baseline}" fill="#FFFFFF" font-family="{FONT}" '
        f'font-size="{font_size}px" font-weight="700" text-anchor="middle">{number}</text>'
        "</g>"
    )


def svg_open(width: int, height: int, title: str, description: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(description)}</desc>',
        '<defs>',
        '<filter id="haloShadow" x="-20%" y="-20%" width="140%" height="150%">',
        '<feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#17324D" flood-opacity="0.055"/>',
        '</filter>',
        '</defs>',
    ]


def header_desktop() -> list[str]:
    return [
        '<rect width="1440" height="96" fill="#FFFFFF"/>',
        '<path d="M0 95.5H1440" stroke="#D4E2E9" stroke-opacity="0.76"/>',
        '<g id="element-01-brand-mark" aria-hidden="true">',
        '<rect x="160" y="30" width="38" height="38" rx="11" fill="#0B5F8A"/>',
        '<path d="M171.5 39.5h10.7l5.3 5.2v14.2h-16z" fill="none" stroke="#FFFFFF" '
        'stroke-width="1.7" stroke-linejoin="round"/>',
        '<path d="M182.1 39.8v5.1h5.1M175.2 50.1h8.3M175.2 54.2h8.3" fill="none" '
        'stroke="#FFFFFF" stroke-width="1.55" stroke-linecap="round"/>',
        '</g>',
        '<g id="element-02-wordmark" aria-hidden="true">',
        text(210, 58, "Study", 23, "#073B57", 700),
        '</g>',
    ]


def header_mobile(width: int) -> list[str]:
    x = 24 if width == 390 else 16
    return [
        '<rect width="100%" height="72" fill="#FFFFFF"/>',
        f'<path d="M0 71.5H{width}" stroke="#D4E2E9" stroke-opacity="0.76"/>',
        f'<g id="element-01-brand-mark" aria-hidden="true"><rect x="{x}" y="18" width="36" height="36" rx="10" fill="#0B5F8A"/>',
        f'<path d="M{x + 11} 26.5h10l5 5v13h-15z" fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-linejoin="round"/>',
        f'<path d="M{x + 21} 26.8v4.8h4.8M{x + 14} 37h8M{x + 14} 41h8" fill="none" stroke="#FFFFFF" stroke-width="1.45" stroke-linecap="round"/>',
        '</g>',
        '<g id="element-02-wordmark" aria-hidden="true">',
        text(x + 48, 43, "Study", 22, "#073B57", 700),
        '</g>',
    ]


def illustration_desktop() -> list[str]:
    return [
        '<g id="element-08-soft-halo" aria-hidden="true">',
        '<circle cx="1060" cy="455" r="190" fill="#E8F4FA" filter="url(#haloShadow)"/>',
        '<circle cx="1060" cy="455" r="153" fill="#FFFFFF" opacity="0.52"/>',
        '<circle cx="1060" cy="455" r="126" fill="none" stroke="#D4E2E9" stroke-opacity="0.42"/>',
        '</g>',
        '<g id="element-09-folded-page-illustration" aria-hidden="true">',
        f'<image href="{PAPER}" x="858" y="250" width="420" height="420" preserveAspectRatio="xMidYMid meet"/>',
        '</g>',
        '<g id="element-12-accent-dots" aria-hidden="true">',
        '<circle cx="900" cy="300" r="3.5" fill="#43A5C5"/>',
        '<circle cx="1240" cy="420" r="4" fill="#43A5C5" opacity="0.86"/>',
        '<circle cx="1204" cy="645" r="3" fill="#43A5C5" opacity="0.78"/>',
        '</g>',
        '<g id="element-10-dotted-route" aria-hidden="true">',
        '<path d="M817 696H930" fill="none" stroke="#43A5C5" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 9"/>',
        '</g>',
        '<g id="element-11-open-endpoint" aria-hidden="true">',
        '<circle cx="948" cy="696" r="14.5" fill="#FFFFFF" stroke="#0B5F8A" stroke-width="3"/>',
        '<circle cx="948" cy="696" r="4" fill="#43A5C5"/>',
        '</g>',
    ]


def desktop_svg(state: dict[str, object], annotated: bool) -> str:
    state_id = str(state["id"])
    kind = "annotated" if annotated else "clean"
    parts = svg_open(
        1440,
        960,
        f"SH-06 {state_id} — {kind} desktop view",
        "Study not-found state design target. The image contains no course identifiers, private data or live API response.",
    )
    parts += ['<rect width="1440" height="960" fill="#F6FAFC"/>']
    parts += header_desktop()
    parts += illustration_desktop()
    parts += [
        '<g id="element-03-state-eyebrow">',
        text(160, 278, str(state["eyebrow"]), 13, "#0B5F8A", 700, spacing=0.55),
        '</g>',
        '<g id="element-04-page-heading">',
        text(160, 350, str(state["headline"][0]), 44, "#073B57", 700),
        text(160, 402, str(state["headline"][1]), 44, "#073B57", 700),
        '</g>',
        '<g id="element-05-supporting-copy">',
        text(160, 455, str(state["body"][0]), 17, "#536A7A", 400),
        text(160, 483, str(state["body"][1]), 17, "#536A7A", 400),
        '</g>',
        '<g id="element-06-primary-action" aria-label="Primary action button">',
        '<rect x="160" y="560" width="224" height="56" rx="10" fill="#0B5F8A"/>',
        '<rect x="160" y="560" width="224" height="56" rx="10" fill="#FFFFFF" opacity="0.035"/>',
        text(272, 595, "Tìm khóa học", 16, "#FFFFFF", 600, anchor="middle"),
        '</g>',
        '<g id="element-07-home-link" aria-label="Secondary home navigation link">',
        text(160, 668, "Về trang chủ", 15, "#0B5F8A", 600),
        '<path d="M259 663h11m-4-4 4 4-4 4" fill="none" stroke="#0B5F8A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        '</g>',
    ]
    if annotated:
        points = [
            (1, 138, 32, 160, 30), (2, 304, 26, 282, 40),
            (3, 138, 261, 160, 264), (4, 138, 327, 160, 312),
            (5, 138, 444, 160, 436), (6, 138, 566, 160, 560),
            (7, 138, 646, 160, 640), (8, 841, 264, 870, 265),
            (9, 1298, 271, 1278, 271), (10, 798, 678, 817, 696),
            (11, 927, 736, 948, 696), (12, 1261, 655, 1204, 645),
        ]
        parts.append('<g id="annotation-layer" aria-label="Element number markers">')
        parts.extend(marker(*point) for point in points)
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def mobile_markers(width: int) -> list[tuple[int, int, int, int, int]]:
    if width == 390:
        return [
            (1, 12, 12, 24, 18), (2, 144, 12, 125, 26),
            (3, 12, 98, 24, 101), (4, 12, 151, 24, 137),
            (5, 12, 247, 24, 239), (6, 12, 309, 24, 323),
            (7, 12, 438, 24, 430), (8, 42, 548, 84, 555),
            (9, 337, 548, 322, 558), (10, 32, 776, 54, 805),
            (11, 151, 822, 129, 805), (12, 337, 735, 278, 775),
        ]
    return [
        (1, 8, 12, 16, 16), (2, 136, 12, 118, 26),
        (3, 8, 88, 16, 101), (4, 8, 130, 16, 137),
        (5, 8, 230, 16, 239), (6, 8, 315, 16, 324),
        (7, 8, 438, 16, 430), (8, 31, 560, 63, 568),
        (9, 289, 560, 271, 560), (10, 10, 766, 37, 788),
        (11, 126, 828, 103, 788), (12, 286, 735, 233, 762),
    ]


def mobile_svg(state: dict[str, object], annotated: bool, width: int = 390) -> str:
    height = 844
    gutter = 24 if width == 390 else 16
    content_width = width - gutter * 2
    scale = 0.58 if width == 390 else 0.51
    translate_x = width / 2 - 1060 * scale
    translate_y = 665 - 455 * scale
    heading_size = 32 if width == 390 else 28
    body_size = 16 if width == 390 else 15
    mobile_body = state["mobile_body"] if width == 390 else state["compact_body"]
    kind = "annotated" if annotated else "clean"
    parts = svg_open(
        width,
        height,
        f"SH-06 {state['id']} — {kind} {width}px mobile view",
        "Study not-found state adapted for a narrow screen. All text and recovery actions remain visible.",
    )
    parts += [f'<rect width="{width}" height="{height}" fill="#F6FAFC"/>']
    parts += header_mobile(width)
    parts += [
        f'<g transform="translate({translate_x:.2f} {translate_y:.2f}) scale({scale:.3f})" aria-hidden="true">',
        *illustration_desktop(),
        '</g>',
        '<g id="element-03-state-eyebrow">',
        text(gutter, 116, str(state["eyebrow"]), 12, "#0B5F8A", 700, spacing=0.45),
        '</g>',
        '<g id="element-04-page-heading">',
        text(gutter, 166, str(state["headline"][0]), heading_size, "#073B57", 700),
        text(gutter, 204, str(state["headline"][1]), heading_size, "#073B57", 700),
        '</g>',
        '<g id="element-05-supporting-copy">',
        text(gutter, 257, str(mobile_body[0]), body_size, "#536A7A", 400),
        text(gutter, 282, str(mobile_body[1]), body_size, "#536A7A", 400),
        '</g>',
        '<g id="element-06-primary-action" aria-label="Primary action button">',
        f'<rect x="{gutter}" y="328" width="{content_width}" height="54" rx="10" fill="#0B5F8A"/>',
        text(width / 2, 362, "Tìm khóa học", 16, "#FFFFFF", 600, anchor="middle"),
        '</g>',
        '<g id="element-07-home-link" aria-label="Secondary home navigation link">',
        text(gutter, 420, "Về trang chủ", 15, "#0B5F8A", 600),
        f'<path d="M{gutter + 99} 415h11m-4-4 4 4-4 4" fill="none" stroke="#0B5F8A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        '</g>',
    ]
    if annotated:
        parts.append('<g id="annotation-layer" aria-label="Element number markers">')
        badge_size = 20 if width == 390 else 16
        parts.extend(marker(*point, size=badge_size) for point in mobile_markers(width))
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def render_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    if not CHROME:
        raise RuntimeError("Không tìm thấy Chrome/Chromium để xuất PNG.")
    with tempfile.TemporaryDirectory(prefix="study-sh06-chrome-") as profile:
        command = [
            CHROME,
            "--headless=new",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
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
        viewports = (("desktop", 1440, 960), ("mobile", 390, 844), ("compact", 320, 844))
        for variant, width, height in viewports:
            for kind, annotated in (("clean", False), ("annotated", True)):
                stem = f"SH-06_{state_id}_{variant}_{kind}"
                svg_path = ROOT / f"{stem}.svg"
                png_path = ROOT / f"{stem}.png"
                svg = desktop_svg(state, annotated) if variant == "desktop" else mobile_svg(state, annotated, width)
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
