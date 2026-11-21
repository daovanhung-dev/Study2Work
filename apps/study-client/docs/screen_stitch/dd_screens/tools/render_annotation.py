#!/usr/bin/env python3
"""Dựng các điểm đánh dấu được đánh số ổn định lên PNG hiện có mà không sửa ảnh gốc."""
from __future__ import annotations

import argparse
import base64
import html
import json
import os
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SystemExit(f"không phải PNG: {path}")
    return struct.unpack(">II", header[16:24])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_png", type=Path)
    parser.add_argument("marker_json", type=Path)
    parser.add_argument("output_png", type=Path)
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()

    original = args.original_png.resolve()
    marker_file = args.marker_json.resolve()
    output = args.output_png.resolve()
    width, height = png_size(original)
    markers = json.loads(marker_file.read_text(encoding="utf-8"))
    if not isinstance(markers, list) or not markers:
        raise SystemExit("JSON điểm đánh dấu phải là một mảng không rỗng")
    numbers = [m.get("number") for m in markers]
    if len(set(numbers)) != len(numbers) or any(not isinstance(n, int) or n < 1 for n in numbers):
        raise SystemExit("số điểm đánh dấu phải là các số nguyên dương không trùng nhau")
    for marker in markers:
        x, y = marker.get("x"), marker.get("y")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or not (0 <= x < width and 0 <= y < height):
            raise SystemExit(f"điểm đánh dấu nằm ngoài ảnh {width}x{height}: {marker}")

    chrome = os.environ.get("CHROME_BIN") or shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Không tìm thấy Chrome/Chromium; hãy đặt CHROME_BIN")

    image_b64 = base64.b64encode(original.read_bytes()).decode("ascii")
    marker_svg = []
    for marker in markers:
        n, x, y = marker["number"], marker["x"], marker["y"]
        label = html.escape(str(marker.get("label", f"Phần tử {n}")), quote=True)
        marker_svg.append(
            f'<g role="img" aria-label="{label}" transform="translate({x} {y})">'
            '<circle r="13" fill="#0B5F8A" stroke="#FFFFFF" stroke-width="3" '
            'style="filter:drop-shadow(0 1px 2px rgba(7,59,87,.55))"/>'
            f'<text text-anchor="middle" dominant-baseline="central" y=".5" '
            f'font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">{n}</text>'
            '</g>'
        )
    page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
      *{{box-sizing:border-box}}html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden;background:#fff}}
      #frame{{position:relative;width:{width}px;height:{height}px;overflow:hidden}}
      #source{{display:block;width:{width}px;height:{height}px}}
      svg{{position:absolute;inset:0;width:{width}px;height:{height}px;pointer-events:none}}
      </style></head><body><div id="frame">
      <img id="source" alt="Thiết kế màn hình gốc" src="data:image/png;base64,{image_b64}">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" aria-label="Ảnh màn hình có đánh số">{''.join(marker_svg)}</svg>
      </div></body></html>'''

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="study-screen-annotation-") as temp:
        temp_path = Path(temp)
        html_path = temp_path / "render.html"
        html_path.write_text(page, encoding="utf-8")
        cmd = [
            chrome,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={temp_path / 'profile'}",
            f"--force-device-scale-factor={args.scale}",
            f"--window-size={width},{height}",
            f"--screenshot={output}",
            html_path.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out_size = png_size(output)
    if out_size[0] * height != out_size[1] * width:
        raise SystemExit(f"tỷ lệ khung hình ảnh dựng đã đổi: ảnh gốc={width}x{height}, đầu ra={out_size[0]}x{out_size[1]}")
    print(f"đã dựng {output} ({out_size[0]}x{out_size[1]}), số điểm đánh dấu={len(markers)}, ảnh gốc={width}x{height}")


if __name__ == "__main__":
    main()
