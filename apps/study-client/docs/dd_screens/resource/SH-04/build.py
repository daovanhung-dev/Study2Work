#!/usr/bin/env python3
"""Dựng package SH-04 từ SVG và render PNG bằng Chrome headless cục bộ."""

from __future__ import annotations

import base64
import html
import re
import shutil
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1440, 960
FONT = "Noto Sans, Arial, sans-serif"
PALETTE = {
    "primary": "#0B5F8A", "hover": "#084968", "deep": "#073B57",
    "sky": "#43A5C5", "soft": "#E8F4FA", "page": "#F6FAFC",
    "surface": "#FFFFFF", "text": "#17324D", "muted": "#536A7A",
    "border": "#D4E2E9", "error": "#B42318",
}

ELEMENTS = [
    {"n": 1, "name": "Study brand mark", "box": (160, 30, 38, 38), "marker": (146, 49), "content": "Glyph trang mở trong brand link.", "font": "N/A; vector trắng, stroke 1.8px", "visual": "Ô ocean 38×38px, radius 11px; glyph trang mở cân giữa.", "semantic": "Ảnh trang trí trong anchor có accessible name ‘Study, Trang chủ’.", "event": "Click/tap link → `/` (SH-01).", "states": "Hover/pressed theo anchor; focus-visible ring 2px `#0B5F8A`, offset 2px.", "validation": "Không có.", "responsive": "Giữ 38×38px; hit area của link ≥44×44px ở mọi breakpoint.", "source": "STATIC_UI; shared auth brand SH-02/03."},
    {"n": 2, "name": "Study wordmark", "box": (210, 34, 82, 30), "marker": (306, 49), "content": "Study", "font": "Noto Sans 23/30/700 `#073B57`", "visual": "Text thuần bên phải mark; không nền/border.", "semantic": "Nội dung anchor brand link tới SH-01.", "event": "Click/tap → `/` (SH-01).", "states": "Hover/pressed `#084968`; focus-visible 2px ring ở anchor.", "validation": "Không có.", "responsive": "Không ẩn/không wrap ở mobile.", "source": "STATIC_UI; style khớp SH-02/03."},
    {"n": 3, "name": "Editorial eyebrow", "box": (212, 536, 300, 18), "marker": (181, 545), "content": "STUDY · XÁC THỰC EMAIL", "font": "Noto Sans 13/18/700; tracking .4px; `#FFFFFF`", "visual": "Chữ hoa vừa phải; accent bar cyan 3×18px ở x=194.", "semantic": "Text tĩnh, không tương tác.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Wrap có kiểm soát trong cột hẹp; không làm mất nội dung.", "source": "STATIC_UI."},
    {"n": 4, "name": "Editorial heading", "box": (212, 572, 408, 88), "marker": (197, 616), "content": "Rõ ràng ở / từng trạng thái.", "font": "Noto Sans 36/44/700 `#FFFFFF`", "visual": "H2 hai dòng, căn trái, không effect trên chữ.", "semantic": "H2 mô tả nguyên tắc hiển thị state.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Giảm font theo viewport; không tràn 320px.", "source": "STATIC_UI."},
    {"n": 5, "name": "Editorial supporting copy", "box": (212, 696, 404, 52), "marker": (197, 722), "content": "Mỗi bước chỉ phản ánh điều hệ thống đã xác nhận.", "font": "Noto Sans 16/26/400 `#E8F4FA`", "visual": "Hai dòng gọn, line-height 26px, căn trái.", "semantic": "Paragraph tĩnh.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Wrap tự nhiên, không ellipsis/crop.", "source": "STATIC_UI."},
    {"n": 6, "name": "Request-receipt artwork", "box": (185, 220, 470, 270), "marker": (173, 220), "content": "Request folio dạng giấy với silhouette rõ, các dòng metadata trừu tượng và vòng hình học thưa; không có chữ.", "font": "N/A; vector source, PNG alpha trong suốt.", "visual": "Artwork Study ocean-blue tương phản rõ, paper layer có depth nhẹ; chỉ dùng token palette, không phong bì/checkmark.", "semantic": "Decorative group `aria-hidden=true`.", "event": "Không click/focus.", "states": "Không có hover/pressed.", "validation": "Không có nội dung delivery/verification hoặc dữ liệu người dùng.", "responsive": "Giữ aspect ratio; có thể ẩn ở mobile.", "source": "Original vector asset `request-status-hero.svg/png`."},
    {"n": 7, "name": "Status card surface", "box": (736, 176, 544, 608), "marker": (1300, 187), "content": "Surface của page SH-04.", "font": "N/A.", "visual": "Surface trắng; border 1px `#D4E2E9`; radius 16px; shadow 0 18px 48px rgba(7,59,87,.07); padding 48px.", "semantic": "Page surface; click nền không action.", "event": "Không có event riêng.", "states": "Không hover/focus/pressed; không elevation shift.", "validation": "Chứa trạng thái response API #02, không thêm form.", "responsive": "Desktop 544px; tablet max-width 600px; mobile full width trong gutter 16px, padding 24px.", "source": "STATIC_UI; auth family SH-02/03."},
    {"n": 8, "name": "Card eyebrow", "box": (784, 224, 270, 18), "marker": (760, 233), "content": "TRẠNG THÁI YÊU CẦU", "font": "Noto Sans 13/18/700; tracking .5px; `#536A7A`", "visual": "Small uppercase label, căn trái.", "semantic": "Text tĩnh định danh vùng.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Không wrap tại chiều rộng mobile card.", "source": "STATIC_UI."},
    {"n": 9, "name": "H1 `Trạng thái yêu cầu`", "box": (784, 260, 448, 48), "marker": (760, 284), "content": "Trạng thái yêu cầu", "font": "Noto Sans 40/48/700 `#073B57`", "visual": "Heading một dòng, hierarchy chính.", "semantic": "H1 duy nhất của page.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Co font khi hẹp; dấu tiếng Việt không clip.", "source": "STATIC_UI."},
    {"n": 10, "name": "Helper", "box": (784, 320, 448, 26), "marker": (760, 333), "content": "Yêu cầu đã được tiếp nhận.", "font": "Noto Sans 16/26/400 `#536A7A`", "visual": "Một dòng ngắn dưới H1.", "semantic": "Paragraph trạng thái.", "event": "Không có.", "states": "Sau response dùng `role=status`, `aria-live=polite`, `aria-atomic=true`; không cướp focus.", "validation": "Chỉ render như `accepted` sau HTTP 202; không biến thành delivery claim.", "responsive": "Wrap theo card nếu cần.", "source": "API #02 message `Yêu cầu gửi email xác thực đã được chấp nhận.`; rút gọn UI, status từ data."},
    {"n": 11, "name": "Status summary surface", "box": (784, 400, 448, 152), "marker": (1300, 410), "content": "Nhóm hai hàng status và hairline divider.", "font": "N/A.", "visual": "Nền `#F6FAFC`, border `#D4E2E9` 1px, radius 12px; không shadow.", "semantic": "Status group có accessible label `Trạng thái yêu cầu và gửi email`.", "event": "Không tương tác.", "states": "Không hover/focus/pressed; thay nội dung theo response state.", "validation": "Hai kết quả độc lập: request accepted và email delivery chưa xác nhận.", "responsive": "Giữ hai cặp label/value; stack label trên value ở 320px.", "source": "API #02 `data.status`; current provider không trả delivery status."},
    {"n": 12, "name": "Request status icon", "box": (808, 416, 28, 32), "marker": (760, 434), "content": "Outline glyph phiếu nhận yêu cầu.", "font": "N/A; 1.8px vector stroke `#0B5F8A`.", "visual": "Biểu tượng folder/tray mở, không checkmark, 28×32px.", "semantic": "Decorative cạnh label status; không thay text.", "event": "Không click/focus.", "states": "Không có.", "validation": "Không encode delivery success.", "responsive": "Giữ 28×32px hoặc ẩn nếu layout xếp chồng.", "source": "STATIC_UI."},
    {"n": 13, "name": "Request label `Yêu cầu`", "box": (852, 428, 110, 22), "marker": (760, 466), "content": "Yêu cầu", "font": "Noto Sans 15/22/600 `#17324D`", "visual": "Label căn trái trong hàng thứ nhất.", "semantic": "Static status label.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Stack trên value; không truncate.", "source": "STATIC_UI."},
    {"n": 14, "name": "Accepted badge `Đã tiếp nhận`", "box": (1096, 422, 112, 28), "marker": (1248, 436), "content": "Đã tiếp nhận", "font": "Noto Sans 13/20/600 `#0B5F8A`", "visual": "Pill ocean-soft, không dùng success-green.", "semantic": "Text status lấy từ `data.status=accepted`.", "event": "Không tương tác.", "states": "Không hover/focus/pressed.", "validation": "Chỉ xuất hiện khi response 202 có status accepted.", "responsive": "Có thể left-align trong stacked layout.", "source": "API #02 response, default provider source."},
    {"n": 15, "name": "Email label `Gửi email`", "box": (808, 492, 120, 22), "marker": (760, 503), "content": "Gửi email", "font": "Noto Sans 15/22/600 `#17324D`", "visual": "Label căn trái ở hàng thứ hai.", "semantic": "Static status label.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Stack trên value; không truncate.", "source": "STATIC_UI."},
    {"n": 16, "name": "Email state `Chưa xác nhận đã gửi`", "box": (1000, 492, 208, 22), "marker": (1248, 503), "content": "Chưa xác nhận đã gửi", "font": "Noto Sans 14/20/600 `#536A7A`", "visual": "Text muted căn phải; không dùng warning/error color.", "semantic": "Explanatory value: response không xác nhận delivery.", "event": "Không có.", "states": "Không hover/focus/pressed.", "validation": "Không suy `status=accepted` thành email sent.", "responsive": "Stack dưới label, căn trái khi hẹp.", "source": "Current provider/view; no delivery field in ActionResult."},
    {"n": 17, "name": "CTA `Đến trang đăng nhập`", "box": (784, 636, 448, 56), "marker": (760, 664), "content": "Đến trang đăng nhập", "font": "Noto Sans 16/24/600, trắng.", "visual": "Ocean fill phẳng `#0B5F8A`, radius 10px, shadow nhẹ, full-width.", "semantic": "Anchor styled as primary button → `/login` (SH-02).", "event": "Click/tap → SH-02 ở accepted state; `INVALID_HANDOFF` dùng cùng CTA #17 để quay về `/register`; không tạo API call.", "states": "Hover/pressed `#084968` trong 140ms; focus-visible 2px ring; navigation luôn dùng link, không loading/disabled.", "validation": "Không khẳng định đăng nhập chắc chắn thành công; API #03 status/account gate còn là dependency.", "responsive": "Full width; cao 56px, hit target đạt yêu cầu.", "source": "SH-04 inventory navigation; SH-02 target route."},
]


def page_defs() -> str:
    return '''<defs>
      <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="24" flood-color="#073B57" flood-opacity=".07"/></filter>
      <filter id="badgeShadow" x="-35%" y="-35%" width="170%" height="170%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#073B57" flood-opacity=".22"/></filter>
    </defs>'''


def hero_svg() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="470" height="270" viewBox="0 0 470 270">
  <defs>
    <filter id="softShadow" x="-35%" y="-35%" width="170%" height="180%"><feDropShadow dx="0" dy="12" stdDeviation="11" flood-color="#073B57" flood-opacity=".16"/></filter>
  </defs>
  <ellipse cx="235" cy="226" rx="126" ry="13" fill="#0B5F8A" opacity=".075"/>
  <circle cx="235" cy="132" r="111" fill="#E8F4FA"/>
  <circle cx="235" cy="132" r="97" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity=".92"/>
  <path d="M93 148c0-46 24-84 62-103M315 40c38 23 62 63 62 107M87 173c20 12 43 17 66 13m164 7c25 4 48-3 66-18" fill="none" stroke="#43A5C5" stroke-width="1.5" stroke-linecap="round" opacity=".72"/>
  <path d="M114 74c16-19 35-31 55-37m132 1c20 7 38 21 53 40" fill="none" stroke="#0B5F8A" stroke-width="1.2" stroke-linecap="round" opacity=".3"/>
  <circle cx="110" cy="100" r="9" fill="#E8F4FA" stroke="#43A5C5" stroke-width="1.5"/><circle cx="110" cy="100" r="3.5" fill="#0B5F8A"/>
  <circle cx="359" cy="160" r="8" fill="#E8F4FA" stroke="#43A5C5" stroke-width="1.5"/><circle cx="359" cy="160" r="2.5" fill="#0B5F8A"/>
  <circle cx="321" cy="54" r="3.5" fill="#0B5F8A" opacity=".66"/><circle cx="146" cy="207" r="3" fill="#0B5F8A" opacity=".55"/>
  <g transform="translate(144 23) rotate(-4 91 103)" filter="url(#softShadow)">
    <rect x="12" y="10" width="184" height="208" rx="19" fill="#43A5C5" opacity=".16"/>
    <rect x="0" y="0" width="184" height="208" rx="19" fill="#FFFFFF" stroke="#D4E2E9" stroke-width="1.4"/>
    <path d="M19 20h34" stroke="#43A5C5" stroke-width="4" stroke-linecap="round"/>
    <circle cx="160" cy="25" r="7" fill="#E8F4FA" stroke="#43A5C5" stroke-width="1.4"/>
    <circle cx="160" cy="25" r="2.4" fill="#0B5F8A"/>
    <path d="M20 49h118" stroke="#073B57" stroke-width="3.2" stroke-linecap="round" opacity=".9"/>
    <path d="M20 63h95M20 72h127" stroke="#D4E2E9" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M20 91h144" stroke="#D4E2E9" stroke-width="1.2"/>
    <rect x="17" y="104" width="150" height="57" rx="12" fill="#E8F4FA"/>
    <circle cx="35" cy="125" r="6" fill="#0B5F8A"/>
    <path d="M49 124h92M49 135h69" stroke="#D4E2E9" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="153" cy="146" r="3.2" fill="#43A5C5"/>
    <path d="M20 178h143M20 188h105" stroke="#D4E2E9" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M0 201h184" stroke="#D4E2E9" stroke-width="1.2"/>
    <circle cx="23" cy="201" r="2.2" fill="#D4E2E9"/><circle cx="161" cy="201" r="2.2" fill="#D4E2E9"/>
  </g>
</svg>'''

def screen_svg(art_data: str, annotated: bool = False) -> str:
    c = PALETTE
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">', page_defs()]
    out += [f'<rect width="1440" height="960" fill="{c["page"]}"/>',
            '<rect width="1440" height="96" fill="#FFFFFF"/>',
            f'<path d="M0 95.5H1440" stroke="{c["border"]}" stroke-opacity=".7"/>',
            '<rect x="160" y="176" width="520" height="608" rx="16" fill="#073B57" stroke="#0B5F8A"/>',
            '<rect x="736" y="176" width="544" height="608" rx="16" fill="#FFFFFF" stroke="#D4E2E9" filter="url(#cardShadow)"/>']

    # Shared Study brand header.
    out += ['<a href="/" aria-label="Study, Trang chủ">',
            '<rect x="160" y="30" width="38" height="38" rx="11" fill="#0B5F8A"/>',
            '<path d="M169 39h8l8 7v14h-16z" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round"/>',
            '<path d="M177 39v8h8M172.5 51.5h9M172.5 55.5h9" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>',
            f'<text x="210" y="58" font-family="{FONT}" font-size="23px" font-weight="700" fill="#073B57">Study</text>', '</a>']

    # Editorial panel and original request-folio artwork.
    out += [f'<image x="185" y="220" width="470" height="270" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{art_data}"/>',
            '<rect x="194" y="536" width="3" height="18" rx="1.5" fill="#43A5C5"/>',
            f'<text x="212" y="550" font-family="{FONT}" font-size="13px" font-weight="700" letter-spacing=".4px" fill="#FFFFFF">STUDY · XÁC THỰC EMAIL</text>',
            f'<text x="212" y="610" font-family="{FONT}" font-size="36px" font-weight="700" letter-spacing="-.5px" fill="#FFFFFF">Rõ ràng ở</text>',
            f'<text x="212" y="654" font-family="{FONT}" font-size="36px" font-weight="700" letter-spacing="-.5px" fill="#FFFFFF">từng trạng thái.</text>',
            f'<text x="212" y="716" font-family="{FONT}" font-size="16px" font-weight="400" fill="#E8F4FA">Mỗi bước chỉ phản ánh điều hệ thống</text>',
            f'<text x="212" y="742" font-family="{FONT}" font-size="16px" font-weight="400" fill="#E8F4FA">đã xác nhận.</text>']

    # Response status card.
    out += [f'<text x="784" y="238" font-family="{FONT}" font-size="13px" font-weight="700" letter-spacing=".5px" fill="#536A7A">TRẠNG THÁI YÊU CẦU</text>',
            f'<text x="784" y="298" font-family="{FONT}" font-size="40px" font-weight="700" letter-spacing="-.6px" fill="#073B57">Trạng thái yêu cầu</text>',
            f'<text x="784" y="339" font-family="{FONT}" font-size="16px" font-weight="400" fill="#536A7A">Yêu cầu đã được tiếp nhận.</text>',
            '<rect x="784" y="400" width="448" height="152" rx="12" fill="#F6FAFC" stroke="#D4E2E9"/>',
            # An open receiving-tray glyph, not a verification checkmark.
            '<path d="M810 425h24v16c0 4-3 7-7 7h-10c-4 0-7-3-7-7z" fill="none" stroke="#0B5F8A" stroke-width="1.8" stroke-linejoin="round"/>',
            '<path d="M822 417v18m0 0-6-6m6 6 6-6" fill="none" stroke="#0B5F8A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<text x="852" y="445" font-family="{FONT}" font-size="15px" font-weight="600" fill="#17324D">Yêu cầu</text>',
            '<rect x="1096" y="422" width="112" height="28" rx="14" fill="#E8F4FA"/>',
            f'<text x="1152" y="441" text-anchor="middle" font-family="{FONT}" font-size="13px" font-weight="600" fill="#0B5F8A">Đã tiếp nhận</text>',
            '<path d="M808 472H1208" stroke="#D4E2E9" stroke-width="1"/>',
            f'<text x="808" y="508" font-family="{FONT}" font-size="15px" font-weight="600" fill="#17324D">Gửi email</text>',
            f'<text x="1208" y="508" text-anchor="end" font-family="{FONT}" font-size="14px" font-weight="600" fill="#536A7A">Chưa xác nhận đã gửi</text>',
            '<a href="/login" aria-label="Đến trang đăng nhập">',
            '<rect x="784" y="636" width="448" height="56" rx="10" fill="#0B5F8A"/>',
            f'<text x="1008" y="671" text-anchor="middle" font-family="{FONT}" font-size="16px" font-weight="600" fill="#FFFFFF">Đến trang đăng nhập</text>', '</a>']

    if annotated:
        for element in ELEMENTS:
            n = element["n"]
            x, y = element["marker"]
            if n == 7:
                out.append('<path d="M1280 187h8" stroke="#0B5F8A" stroke-width="1.2" opacity=".8"/>')
            out.append(f'<g filter="url(#badgeShadow)"><circle cx="{x}" cy="{y}" r="12" fill="#0B5F8A" stroke="#FFFFFF" stroke-width="2"/><text x="{x}" y="{y+4}" text-anchor="middle" font-family="{FONT}" font-size="11px" font-weight="700" fill="#FFFFFF">{n}</text></g>')

    out.append('</svg>')
    return "\n".join(out)


def screen_document() -> str:
    rows: list[str] = []
    for element in ELEMENTS:
        x, y, w, h = element["box"]
        mx, my = element["marker"]
        cells = [f"**#{element['n']} — {element['name']}**<br>{html.escape(element['content'])}",
                 f"`x={x}, y={y}, w={w}, h={h}` px<br>Marker center `({mx}, {my})`.",
                 f"{element['visual']}<br><br>**Font:** {element['font']}",
                 element["semantic"], element["event"], element["states"],
                 f"**Validation/loading:** {element['validation']}<br><br>**Responsive:** {element['responsive']}<br><br>**Source:** {element['source']}"]
        rows.append("| " + " | ".join(cell.replace("|", "&#124;").replace("\n", " ") for cell in cells) + " |")

    return f'''# SH-04 — Đặc tả thiết kế màn hình handoff xác thực email

> **Status:** `DESIGN_TARGET / NOT_IMPLEMENTED`. Study Web runtime/router chưa có trong checkout. Screenshot là design artifact, không chứng minh form/route/API client đang chạy.

## Tóm tắt

- **Screen:** SH-04 — Handoff xác thực email; route mục tiêu `/register/verification`; actor Guest; AC-01; API #02.
- **Canvas:** 1440×960px; header trắng cao 96px; content max-width 1120px; auth shell chia 520px + 56px + 544px.
- **Purpose:** Hiển thị riêng hai sự thật: request được provider chấp nhận và trạng thái gửi email chưa được xác nhận. Không gọi request acceptance là email delivery hoặc verified.
- **Style:** Study ocean palette; panel trái là một dark accent `#073B57`, card phải giữ light surface. Request folio riêng, không dùng phong bì/checkmark.
- **Font:** Noto Sans với fallback `Arial, sans-serif`, đã có trong design assets; không nạp font mạng.
- **Không thuộc screen:** OTP/link confirm, resend, inbox navigation, CAPTCHA, profile info, email address, token, operation polling, email verification success.

## Bố cục và tokens

| Vùng | Bounds | Thông số |
|---|---:|---|
| Header | `0,0,1440,96` | Nền `#FFFFFF`, hairline `#D4E2E9`; brand anchor trái. |
| Editorial panel | `160,176,520,608` | Ocean-deep `#073B57`, viền `#0B5F8A`, radius 16px; artwork sáng ở trên, copy trắng cuối panel. |
| Status surface | `736,176,544,608` | `#FFFFFF`, border `#D4E2E9`, radius 16px, diffuse shadow, padding 48px. |
| Status summary | `784,400,448,152` | Nền `#F6FAFC`, border `#D4E2E9`, radius 12px; hai hàng, không shadow. |
| Primary action | `784,636,448,56` | Link đến SH-02, primary ocean. |

Tokens: primary `#0B5F8A`; hover/pressed `#084968`; heading `#073B57`; accent `#43A5C5` (decorative only); soft `#E8F4FA`; page `#F6FAFC`; surface `#FFFFFF`; text `#17324D`; muted `#536A7A`; border `#D4E2E9`; error `#B42318`. Accepted không dùng success-green.

## Bản đồ element và hành vi

Mỗi marker trong `SH-04_annotated.png` khớp đúng một hàng. `SH-04_clean.png` giữ cùng screen, bỏ riêng lớp marker. Cỡ chữ ghi `font-size/line-height/weight` px.

| Element / nội dung | Bounds + marker | Visual, typography, màu | Semantic | Click/tap | Hover/focus/pressed/state | Validation/loading/responsive/source |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Expected flow và current source

| Hạng mục | Expected từ inventory/catalog | Current source được đọc | Thiết kế giữ đúng ranh giới |
|---|---|---|---|
| Choreography | SH-03 gọi #01; lấy `data.id`/`data.email`; SH-04 gửi body `{{user_id,email}}` đến #02; sau 202 liên kết SH-02. | #01 hiện chỉ log `verification_dispatch_pending`; không gọi #02. API #02 route public, không Bearer, không DB; gọi provider đồng bộ. | Link đến SH-02 là target điều hướng; không nói transition đã chạy/wired. Handoff identity transport còn open. |
| HTTP 202 | `DESIGN_OPERATION_ACCEPTED`, `ActionResult.status`/optional `reason`. | View ánh xạ `status`, optional `reason`; default stub trả `accepted`. | Hàng `Yêu cầu` phản ánh status `accepted`; không thêm operation id, poll hay retry. |
| Email delivery | API mục tiêu gửi mã/link nếu verification được bật; F01 nhắc accepted không chứng minh sent/verified. | Stub hiện không gửi email, không tạo token/link; response không có delivery field. | Hàng `Gửi email` ghi `Chưa xác nhận đã gửi`; không chỉ dẫn inbox/spam hoặc dùng success-green. |
| Errors | API #02 422 validation, 500 provider failure. | 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`/safe message; provider raw details không trả ra. | `SCREEN.md` mô tả error state an toàn; không thêm resend/auto retry. |
| Confirm/resend | Catalog không có endpoint xác nhận OTP/link. | Không có token lifecycle, verification endpoint, retry worker/rate-limit contract. | Không thiết kế OTP/link/resend/verified state; ghi open decisions. |
| Runtime | Page `/register/verification`, Guest, AC-01, trạng thái accepted/stub/no-delivery/error. | `apps/study-client/` không có Study Web runtime/router. API #02 DD `Draft — Needs Confirmation`. | Toàn bộ route/UI là `DESIGN_TARGET / NOT_IMPLEMENTED`. |

### State matrix

| State | Trigger | Hành vi |
|---|---|---|
| `HANDOFF_LOADING` | Có `user_id/email`, request #02 đang chờ | Announce polite status, chỉ gửi một request; CTA #17 vẫn là link navigation, không khóa khi dispatch đang chờ; không hiển thị PII trong URL, không gửi duplicate. |
| `ACCEPTED_STUB` | HTTP 202, `data.status=accepted` | State trong ảnh chính; request `Đã tiếp nhận`, email `Chưa xác nhận đã gửi`; không auto retry/poll. |
| `UNMAPPED_PROVIDER_STATUS` | HTTP 202 có `status` ngoài tập UI được duyệt | Hiện trạng thái trung tính “Trạng thái chưa được xác định”; không render raw `reason` hoặc suy ra delivery. |
| `INVALID_HANDOFF` | Thiếu context hoặc 422 | Không call lại; message an toàn; CTA #17 đổi nhãn/đích về SH-03 chỉ trong state này. |
| `DISPATCH_ERROR` | 500 hoặc không có response | “Chưa thể tiếp nhận yêu cầu lúc này.”; không suy đoán delivery outcome; không auto retry. |
| `NO_DELIVERY_CONFIRMATION` | Default stub accepted, không gửi thư | Giữ status email rõ ràng; không gợi ý kiểm tra inbox/spam; không resend. |

## Navigation và screen liên quan

| Element/state | Sự kiện | Đích |
|---|---|---|
| Brand #1/#2 | Click/tap | SH-01 `/`. |
| CTA #17 | Click/tap | SH-02 `/login` theo inventory. Link này không khẳng định account đã được verify hoặc login thành công. |
| CTA #17 trong `INVALID_HANDOFF` | Click/tap | Đổi nhãn thành `Quay lại đăng ký` và về SH-03 `/register`; dùng lại cùng control slot, không phải child screen. |

SH-04 không có child page/modal. SH-05/SH-06 là state view độc lập. API #18 không được gọi vì #02 không trả `operation_id`.

## Accessibility và responsive

- H1 duy nhất; tab order: brand → CTA. Static screen không trap focus.
- Sau API response, cập nhật một `role=status`, `aria-live=polite`, `aria-atomic=true`, không tự chuyển focus. Status group có accessible label và text riêng cho acceptance/delivery.
- Không dựa vào màu/icon để biểu thị status. Không dùng checkmark xanh vì có thể bị hiểu là email verified.
- Normal text ≥4.5:1; boundary ≥3:1; focus ring ≥2px và không clip; controls ≥44px; CTA 56px.
- 1440px: hai cột 520/56/544. 768–1023px: card max-width 600px; panel có thể thu/ẩn. 320–767px: gutter 16px, card padding 24px; status cặp label/value stack; CTA full-width 56px; art ẩn được; không horizontal scroll. Tôn trọng `prefers-reduced-motion`.

## Open decisions / giới hạn

1. API #02 DD còn Draft; provider thật, acceptance boundary và `status/reason` enum chưa được xác nhận.
2. API #01 không gọi #02; caller, feature gate và lỗi dispatch sau commit chưa được quyết.
3. User-email handoff/PII transport qua route và direct-entry behavior chưa có Study Web contract.
4. Verification token/link/expiry/confirmation, resend/idempotency/rate limit/abuse-control chưa có source/contract.
5. API #03 có account-status gate; CTA route tới SH-02 không hứa đăng nhập thành công.

## Asset package

- `SH-04_clean.png`, `SH-04_annotated.png` — 1440×960.
- `SH-04_clean.svg`, `SH-04_annotated.svg` — editable vector source; artwork PNG embed bên trong.
- `request-status-hero.svg`, `request-status-hero.png` — original transparent request-receipt artwork.
- `PLAN.md`, `SCREEN.md`, `build.py`, `SH-04_design_handoff_v2.zip`.
'''


def render(svg_path: Path, output_path: Path, size: tuple[int, int]) -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if chrome is None:
        raise RuntimeError("Không tìm thấy Chrome/Chromium headless để render SVG.")
    with tempfile.TemporaryDirectory(prefix="sh04-chrome-") as profile:
        args = [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
                "--disable-dev-shm-usage", "--hide-scrollbars", "--force-device-scale-factor=1",
                "--default-background-color=00000000", f"--user-data-dir={profile}",
                f"--window-size={size[0]},{size[1]}", f"--screenshot={output_path}", svg_path.resolve().as_uri()]
        done = subprocess.run(args, capture_output=True, text=True, timeout=45)
        if done.returncode != 0 or not output_path.exists():
            raise RuntimeError(f"Chrome render thất bại: {done.stderr[-2000:]}")


def png_meta(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"PNG header không hợp lệ: {path.name}")
    w, h = struct.unpack(">II", data[16:24])
    return w, h, data[25]


def main() -> None:
    art_svg = ROOT / "request-status-hero.svg"
    art_png = ROOT / "request-status-hero.png"
    art_svg.write_text(hero_svg(), encoding="utf-8")
    render(art_svg, art_png, (470, 270))
    if png_meta(art_png)[:2] != (470, 270) or png_meta(art_png)[2] not in (4, 6):
        raise RuntimeError(f"Artwork phải 470×270 và có alpha; meta={png_meta(art_png)}")
    art_b64 = base64.b64encode(art_png.read_bytes()).decode("ascii")

    files = {
        "SH-04_clean.svg": screen_svg(art_b64),
        "SH-04_annotated.svg": screen_svg(art_b64, annotated=True),
    }
    for name, content in files.items():
        (ROOT / name).write_text(content, encoding="utf-8")
    render(ROOT / "SH-04_clean.svg", ROOT / "SH-04_clean.png", (WIDTH, HEIGHT))
    render(ROOT / "SH-04_annotated.svg", ROOT / "SH-04_annotated.png", (WIDTH, HEIGHT))
    for name in ("SH-04_clean.png", "SH-04_annotated.png"):
        if png_meta(ROOT / name)[:2] != (WIDTH, HEIGHT):
            raise RuntimeError(f"Sai kích thước {name}: {png_meta(ROOT / name)}")

    annotated = (ROOT / "SH-04_annotated.svg").read_text(encoding="utf-8")
    badge_count = len(re.findall(r'<g filter="url\(#badgeShadow\)"><circle', annotated))
    if badge_count != len(ELEMENTS):
        raise RuntimeError(f"Badge count {badge_count}, expected {len(ELEMENTS)}")

    (ROOT / "SCREEN.md").write_text(screen_document(), encoding="utf-8")
    archive = ROOT / "SH-04_design_handoff_v2.zip"
    members = ["PLAN.md", "SCREEN.md", "SH-04_clean.png", "SH-04_annotated.png",
               "SH-04_clean.svg", "SH-04_annotated.svg", "request-status-hero.png",
               "request-status-hero.svg", "build.py"]
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as zf:
        for name in members:
            zf.write(ROOT / name, arcname=name)
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() is not None or set(zf.namelist()) != set(members):
            raise RuntimeError("ZIP bị lỗi hoặc thiếu deliverable.")
    print(f"Rendered SH-04: clean={png_meta(ROOT/'SH-04_clean.png')[:2]}, annotated={png_meta(ROOT/'SH-04_annotated.png')[:2]}, artwork={png_meta(art_png)}")
    print(f"Element rows={len(ELEMENTS)}; annotation badges={badge_count}; ZIP={archive.name} ({archive.stat().st_size} bytes, {len(members)} files)")


if __name__ == "__main__":
    main()
