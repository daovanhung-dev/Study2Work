#!/usr/bin/env python3
"""Dựng bộ design handoff SH-02 bằng SVG và Chrome headless, không cần thư viện Python ngoài."""

from __future__ import annotations

import html
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WIDTH = 1440
HEIGHT = 960
FONT = "Noto Sans, Arial, sans-serif"
PALETTE = {
    "primary": "#0B5F8A",
    "hover": "#084968",
    "deep": "#073B57",
    "sky": "#43A5C5",
    "soft": "#E8F4FA",
    "page": "#F6FAFC",
    "surface": "#FFFFFF",
    "text": "#17324D",
    "muted": "#536A7A",
    "border": "#D4E2E9",
}


ELEMENTS = [
    {
        "id": 1,
        "name": "Study brand mark",
        "content": "Biểu tượng trang học mở trong brand link",
        "box": (160, 30, 38, 38),
        "type": "N/A",
        "visual": "SVG mark #0B5F8A, nền vuông bo 11px; nét trang trắng 2px; không đổ bóng",
        "semantic": "decorative image bên trong link có accessible name Study, Trang chủ",
        "event": "click/tap brand link → `/` (SH-01)",
        "state": "focus-visible 2px #0B5F8A offset 2px trên link cha; không có hover riêng cho mark",
        "responsive": "giữ 38×38px ở mọi breakpoint; hit area link cha ≥44×44px",
        "source": "STATIC_UI; design continuation từ SH-01",
    },
    {
        "id": 2,
        "name": "Study wordmark",
        "content": "Study",
        "box": (210, 34, 82, 30),
        "type": "Noto Sans 23px/30px/700 #073B57",
        "visual": "background none; border none; left aligned; thuộc cùng brand link với #1",
        "semantic": "link text; accessible name của brand link",
        "event": "click/tap → `/` (SH-01)",
        "state": "hover 140ms đổi màu #084968; focus-visible 2px #0B5F8A offset 2px; pressed #084968",
        "responsive": "giữ nguyên; brand link không bị ẩn ở 320px",
        "source": "STATIC_UI",
    },
    {
        "id": 3,
        "name": "Editorial eyebrow",
        "content": "STUDY · KHÔNG GIAN HỌC TẬP",
        "box": (212, 582, 282, 18),
        "type": "Noto Sans 13px/18px/700 #0B5F8A",
        "visual": "background none; border none; accent bar 3×18px #43A5C5 ở x=194; letter spacing 0.4px",
        "semantic": "static text",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "wrap tự nhiên; không thay đổi ý nghĩa",
        "source": "STATIC_UI",
    },
    {
        "id": 4,
        "name": "Editorial heading",
        "content": "Chào mừng bạn / trở lại.",
        "box": (212, 620, 400, 88),
        "type": "Noto Sans 36px/44px/700 #073B57",
        "visual": "background none; border none; hai dòng trái; khoảng dòng 0px ngoài line-height",
        "semantic": "h2",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "tablet giữ tối đa 2 dòng; mobile co cỡ theo container và không tràn ngang",
        "source": "STATIC_UI",
    },
    {
        "id": 5,
        "name": "Editorial supporting copy",
        "content": "Đăng nhập để mở lại không gian học tập / của bạn trên Study.",
        "box": (212, 736, 404, 52),
        "type": "Noto Sans 16px/26px/400 #536A7A",
        "visual": "background none; border none; left aligned; two lines",
        "semantic": "paragraph",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "wrap theo chiều rộng cột; không cắt nội dung",
        "source": "STATIC_UI",
    },
    {
        "id": 6,
        "name": "Editorial learning illustration",
        "content": "PNG minh họa sách mở, giấy và bút trong suốt; không chứa chữ hoặc dữ liệu",
        "box": (185, 196, 470, 313),
        "type": "N/A",
        "visual": "PNG artwork trong suốt 470×313px, căn giữa; sách/paper ocean palette với điểm coral nhỏ; decorative, không viền",
        "semantic": "decorative group, `aria-hidden=true`",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "tablet thu nhỏ; mobile có thể ẩn vì decorative",
        "source": "IMAGEGEN; original hero asset tạo riêng cho SH-02, file `learning-book-hero.png`",
    },
    {
        "id": 7,
        "name": "Login form surface",
        "content": "Form group chứa #8–#17",
        "box": (736, 176, 544, 608),
        "type": "N/A",
        "visual": "surface #FFFFFF; border 1px #D4E2E9; radius 16px; shadow 0 16px 48px rgba(7,59,87,0.06)",
        "semantic": "form group; không phải link/card action",
        "event": "không có event riêng; submit duy nhất qua #15 hoặc Enter trong field",
        "state": "không áp dụng; surface không có hover/pressed",
        "responsive": "desktop 544px; tablet max-width 600px; mobile full width trong gutter 16px",
        "source": "STATIC_UI",
    },
    {
        "id": 8,
        "name": "Form eyebrow",
        "content": "TÀI KHOẢN STUDY",
        "box": (784, 226, 240, 18),
        "type": "Noto Sans 13px/18px/700 #536A7A",
        "visual": "background none; border none; left aligned; letter spacing 0.5px",
        "semantic": "static text",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "giữ nguyên cỡ; không wrap ở 320px content width",
        "source": "STATIC_UI",
    },
    {
        "id": 9,
        "name": "Login heading",
        "content": "Đăng nhập",
        "box": (784, 262, 300, 48),
        "type": "Noto Sans 40px/48px/700 #073B57",
        "visual": "background none; border none; left aligned",
        "semantic": "h1",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "co theo viewport nhỏ; không clip tiếng Việt",
        "source": "STATIC_UI",
    },
    {
        "id": 10,
        "name": "Form supporting text",
        "content": "Sử dụng email và mật khẩu đã đăng ký.",
        "box": (784, 324, 432, 26),
        "type": "Noto Sans 16px/26px/400 #536A7A",
        "visual": "background none; border none; left aligned",
        "semantic": "paragraph",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "wrap theo form width",
        "source": "STATIC_UI; nội dung không thêm policy",
    },
    {
        "id": 11,
        "name": "Email label",
        "content": "Email",
        "box": (784, 390, 100, 20),
        "type": "Noto Sans 14px/20px/600 #17324D",
        "visual": "background none; border none; left aligned; liên kết input #12",
        "semantic": "label `for=email`",
        "event": "click/tap label focus #12",
        "state": "không có hover; focus theo input được label trỏ tới",
        "responsive": "giữ nguyên; label luôn hiển thị phía trên input",
        "source": "STATIC_UI; API #03 field `email`",
    },
    {
        "id": 12,
        "name": "Email input",
        "content": "Placeholder `Nhập email của bạn`; value để trống trong ảnh",
        "box": (784, 418, 448, 56),
        "type": "Noto Sans 15px/24px/400 #17324D; placeholder #536A7A",
        "visual": "input white; border 1px #536A7A; radius 8px; padding 16px; no icon",
        "semantic": "required input `type=email`, `autocomplete=username`, `inputmode=email`; label #11",
        "event": "focus/type/paste/password-manager fill; trim/validate theo current source; không tự submit khi blur",
        "state": "hover border #084968; focus-visible 2px #0B5F8A offset 2px; invalid border + inline error; no pressed state",
        "responsive": "width 100%, min-height 56px; giữ label; không zoom/clip tại 320px",
        "source": "API #03 `email`; current validator EmailStr, trim, max 255; không sample account",
    },
    {
        "id": 13,
        "name": "Password label",
        "content": "Mật khẩu",
        "box": (784, 504, 120, 20),
        "type": "Noto Sans 14px/20px/600 #17324D",
        "visual": "background none; border none; left aligned; liên kết input #14",
        "semantic": "label `for=password`",
        "event": "click/tap label focus #14",
        "state": "không có hover; focus theo input được label trỏ tới",
        "responsive": "giữ nguyên; label luôn hiển thị phía trên input",
        "source": "STATIC_UI; API #03 field `password`",
    },
    {
        "id": 14,
        "name": "Password input",
        "content": "Placeholder `Nhập mật khẩu`; value để trống trong ảnh",
        "box": (784, 532, 448, 56),
        "type": "Noto Sans 15px/24px/400 #17324D; placeholder #536A7A",
        "visual": "input white; border 1px #536A7A; radius 8px; padding 16px; no visibility icon",
        "semantic": "required input `type=password`, `autocomplete=current-password`; label #13",
        "event": "focus/type/paste/password-manager fill; client rejects only blank/whitespace per current source; no password-strength rule",
        "state": "hover border #084968; focus-visible 2px #0B5F8A offset 2px; invalid border + inline error; no pressed state",
        "responsive": "width 100%, min-height 56px; keep password manager and paste support",
        "source": "API #03 `password`; no sample credential or value",
    },
    {
        "id": 15,
        "name": "Submit button",
        "content": "Đăng nhập",
        "box": (784, 620, 448, 56),
        "type": "Noto Sans 16px/24px/600 #FFFFFF",
        "visual": "fill #0B5F8A; border none; radius 8px; centered; min hit target exceeds 44px",
        "semantic": "submit button",
        "event": "click/tap or Enter → validate fields → one `POST /api/v1/auth/login` JSON `{email,password}`; no Authorization header",
        "state": "hover 140ms fill #084968; focus-visible 2px #0B5F8A offset 2px; pressed #084968 without movement; pending label `Đang đăng nhập…`, disable duplicate submit",
        "responsive": "full form width; height 56px; 100% width on mobile",
        "source": "API #03 current source; contract status/schema mismatch documented separately",
    },
    {
        "id": 16,
        "name": "Signup prompt",
        "content": "Chưa có tài khoản?",
        "box": (837, 708, 175, 24),
        "type": "Noto Sans 15px/22px/400 #536A7A",
        "visual": "background none; border none; centered with #17",
        "semantic": "static text",
        "event": "không có",
        "state": "không áp dụng; không hover/focus/pressed",
        "responsive": "wrap before link only when needed; no overlap at 320px",
        "source": "STATIC_UI",
    },
    {
        "id": 17,
        "name": "Signup link",
        "content": "Tạo tài khoản",
        "box": (1018, 708, 130, 24),
        "type": "Noto Sans 15px/22px/600 #0B5F8A",
        "visual": "background none; border none; underline 1px #0B5F8A; inline beside #16",
        "semantic": "navigation link",
        "event": "click/tap → `/register` (SH-03)",
        "state": "hover 140ms color #084968; focus-visible 2px #0B5F8A offset 2px; pressed #084968",
        "responsive": "preserve ≥44px hit area; wrap to next line if required",
        "source": "SH-03 route from screen inventory; route remains design target",
    },
]

MARKERS = [
    (145, 49),
    (306, 49),
    (194, 612),
    (644, 664),
    (644, 773),
    (648, 208),
    (1294, 190),
    (760, 235),
    (760, 283),
    (760, 337),
    (760, 399),
    (1256, 446),
    (760, 513),
    (1256, 560),
    (1256, 648),
    (812, 720),
    (1162, 720),
]


def escape(value: object) -> str:
    """Escape text for safe insertion into SVG or Markdown strings."""
    return html.escape(str(value), quote=True)


def text_node(
    x: int,
    y: int,
    content: str,
    *,
    size: int,
    line_height: int,
    weight: int,
    color: str,
    anchor: str = "start",
    tracking: float = 0,
) -> str:
    """Create top-aligned text with a known font metric and escaped content."""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'dominant-baseline="hanging" font-family="{FONT}" font-size="{size}px" '
        f'font-weight="{weight}" line-height="{line_height}px" fill="{color}" '
        f'letter-spacing="{tracking}px">{escape(content)}</text>'
    )


def build_svg() -> str:
    """Build the clean SH-02 desktop screenshot as self-contained SVG."""
    c = PALETTE
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '<filter id="card-shadow" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur stdDeviation="18"/></filter>',
        '<clipPath id="left-panel-clip"><rect x="160" y="128" width="520" height="704" rx="16"/></clipPath>',
        '<clipPath id="form-clip"><rect x="736" y="176" width="544" height="608" rx="16"/></clipPath>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{c["page"]}"/>',
        '<rect x="0" y="0" width="1440" height="96" fill="#FFFFFF"/>',
        f'<path d="M0 95.5H1440" stroke="{c["border"]}" stroke-width="1"/>',
        # Left editorial surface and a custom generated transparent hero illustration.
        f'<rect x="160" y="128" width="520" height="704" rx="16" fill="{c["soft"]}"/>',
        '<image href="learning-book-hero.png" x="185" y="196" width="470" height="313" preserveAspectRatio="xMidYMid meet"/>',
        # Editorial copy on the left.
        '<rect x="194" y="582" width="3" height="18" rx="1.5" fill="#43A5C5"/>',
        text_node(212, 582, "STUDY · KHÔNG GIAN HỌC TẬP", size=13, line_height=18, weight=700, color=c["primary"], tracking=0.4),
        text_node(212, 620, "Chào mừng bạn", size=36, line_height=44, weight=700, color=c["deep"]),
        text_node(212, 664, "trở lại.", size=36, line_height=44, weight=700, color=c["deep"]),
        text_node(212, 736, "Đăng nhập để mở lại không gian học tập", size=16, line_height=26, weight=400, color=c["muted"]),
        text_node(212, 762, "của bạn trên Study.", size=16, line_height=26, weight=400, color=c["muted"]),
        # Form surface.
        '<rect x="743" y="186" width="544" height="608" rx="16" fill="#073B57" opacity="0.07" filter="url(#card-shadow)"/>',
        f'<rect x="736" y="176" width="544" height="608" rx="16" fill="{c["surface"]}" stroke="{c["border"]}" stroke-width="1"/>',
        # Header brand link visual.
        f'<rect x="160" y="30" width="38" height="38" rx="11" fill="{c["primary"]}"/>',
        '<path d="M169 39H180L188 47V59H169Z" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>',
        '<path d="M180 39V47H188M173 51H184M173 55H184" fill="none" stroke="#FFFFFF" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
        text_node(210, 34, "Study", size=23, line_height=30, weight=700, color=c["deep"]),
        # Form copy and controls.
        text_node(784, 226, "TÀI KHOẢN STUDY", size=13, line_height=18, weight=700, color=c["muted"], tracking=0.5),
        text_node(784, 262, "Đăng nhập", size=40, line_height=48, weight=700, color=c["deep"]),
        text_node(784, 324, "Sử dụng email và mật khẩu đã đăng ký.", size=16, line_height=26, weight=400, color=c["muted"]),
        text_node(784, 390, "Email", size=14, line_height=20, weight=600, color=c["text"]),
        f'<rect x="784" y="418" width="448" height="56" rx="8" fill="#FFFFFF" stroke="{c["muted"]}" stroke-width="1"/>',
        text_node(800, 435, "Nhập email của bạn", size=15, line_height=24, weight=400, color=c["muted"]),
        text_node(784, 504, "Mật khẩu", size=14, line_height=20, weight=600, color=c["text"]),
        f'<rect x="784" y="532" width="448" height="56" rx="8" fill="#FFFFFF" stroke="{c["muted"]}" stroke-width="1"/>',
        text_node(800, 549, "Nhập mật khẩu", size=15, line_height=24, weight=400, color=c["muted"]),
        f'<rect x="784" y="620" width="448" height="56" rx="8" fill="{c["primary"]}"/>',
        text_node(1008, 636, "Đăng nhập", size=16, line_height=24, weight=600, color="#FFFFFF", anchor="middle"),
        text_node(837, 708, "Chưa có tài khoản?", size=15, line_height=22, weight=400, color=c["muted"]),
        text_node(1018, 708, "Tạo tài khoản", size=15, line_height=22, weight=600, color=c["primary"]),
        '<path d="M1018 729H1144" stroke="#0B5F8A" stroke-width="1"/>',
        '</svg>',
    ]
    return "\n".join(parts)


def annotated_svg(clean_svg: str) -> str:
    """Add one numbered circular badge for each planned visible target."""
    if len(MARKERS) != 17 or len(set(MARKERS)) != 17:
        raise ValueError("SH-02 marker centers must be 17 unique points")
    badges: list[str] = ['<g id="element-markers" font-family="Noto Sans, Arial, sans-serif">']
    for number, (cx, cy) in enumerate(MARKERS, start=1):
        badges.append(
            f'<circle cx="{cx}" cy="{cy}" r="12" fill="#0B5F8A" stroke="#FFFFFF" stroke-width="1"/>'
        )
        badges.append(
            f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="12px" font-weight="700" fill="#FFFFFF">{number}</text>'
        )
    badges.append("</g>")
    return clean_svg.replace("</svg>", "\n" + "\n".join(badges) + "\n</svg>")


def markdown_table() -> str:
    """Render the exact element map from the same records used by the SVG builder."""
    lines = [
        "| # | Element / content | Bounding box x,y,w,h (px) | Typography | Surface / alignment | Semantics | Click/tap | Hover/focus/pressed | Responsive | Data source |",
        "|---:|---|---|---|---|---|---|---|---|---|",
    ]
    for item in ELEMENTS:
        x, y, width, height = item["box"]
        values = [
            f'#{item["id"]}',
            f'{item["name"]}: {item["content"]}',
            f"{x},{y},{width},{height}",
            item["type"],
            item["visual"],
            item["semantic"],
            item["event"],
            item["state"],
            item["responsive"],
            item["source"],
        ]
        lines.append("| " + " | ".join(str(value).replace("|", "/") for value in values) + " |")
    return "\n".join(lines)


def build_screen_md() -> str:
    """Build the full Vietnamese screen specification and evidence boundary."""
    return f'''# SH-02 — Đăng nhập Study

**Trạng thái:** `DESIGN_TARGET / NOT_IMPLEMENTED` · **Route:** `/login` (đề xuất) · **Actor:** Guest · **AC-02** · **Priority:** P0.

## Phạm vi và ranh giới bằng chứng

Đây là design handoff, không phải UI đã implement. Checkout hiện không có Study Web source, router hay auth client. Screen catalog chỉ là baseline thiết kế. Ảnh chính hiển thị trạng thái idle, không có lỗi và không điền email/mật khẩu mẫu. Không có modal, drawer, screen con hoặc auth provider ngoài email/password trong scope.

API #03 và #04 được đối chiếu với source hiện tại. API #03 có discrepancy contract: catalog/DD #03 ghi HTTP 201 `DESIGN_RESOURCE_CREATED` với `ApiEnvelope<UserProfile>` và errors 422/500; AC-02/current route ghi HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, current source trả profile cùng access/refresh token fields và thêm errors 401/403. DD #03 còn `Draft — Needs Confirmation`; screen không quyết định thay API owner. Không thiết kế chi tiết cơ chế lưu token ở client vì source Study Web và approved persistence policy chưa có.

## Plan tóm tắt

- Art direction `premium editorial sign-in`, dùng ocean palette và brand mark cùng họ SH-01, nhưng artwork riêng. Minh họa sách/giấy/bút là PNG trong suốt tạo riêng bằng imagegen, không có chữ giả, dữ liệu hoặc logo ngoài.
- Desktop chia hai vùng: editorial panel trái, form là vùng hành động chính bên phải. Container 1120px centered trên canvas 1440×960. Card trắng viền mảnh, shadow rất nhẹ, nhịp 4px.
- Chỉ có email, mật khẩu, nút đăng nhập và link đăng ký. Không thêm quên mật khẩu, remember-me, show-password, CAPTCHA, OTP hay social login.
- Main screenshot có đúng 17 mục tiêu đánh số; error/loading/role branches mô tả ở các phần sau và không giả xuất hiện trong ảnh idle. Artwork riêng được tạo bằng imagegen, lưu kèm dạng `learning-book-hero.png`.

## Layout và responsive

| Vùng | Desktop 1440×960 | Tablet 768–1023 | Mobile 320–767 |
|---|---|---|---|
| Container/header | max-width 1120px; x=160..1280; header 96px, brand x=160 y=30 | gutter 24px; brand giữ nguyên | gutter 16px; brand hiển thị, không drawer |
| Editorial panel | x=160 y=128 w=520 h=704; radius 16; nền #E8F4FA | giảm art, copy giữ dễ đọc | xếp sau form hoặc ẩn riêng art decorative; không che action |
| Illustration | x=185 y=196 w=470 h=313; transparent PNG, centered above editorial copy | thu nhỏ theo panel | decorative; có thể thu nhỏ hoặc ẩn |
| Login form | x=736 y=176 w=544 h=608; padding 48px; inner width 448px | max-width 600px, căn giữa | full width trừ gutter 16px; input và button 100% |
| Inputs/button | email y=418 h=56; password y=532 h=56; button y=620 h=56; radius 8px | giữ cao 56px | giữ ≥56px và hit area ≥44×44px |
| Footer | không thêm footer marketing/legal ngoài scope | không đổi | không đổi |

Bounding boxes dưới đây là pixel tuyệt đối của SVG 1440×960. Font thực tế là `Noto Sans` từ system sans fallback vì Inter chưa có trên môi trường render. `N/A` nghĩa là không áp typography.

## Bản đồ 17 elements

{{ELEMENT_TABLE}}

## API, validation và event flow

### API #03 — `POST /api/v1/auth/login`

- Public JSON body `{{email, password}}`; không gửi Authorization header.
- Current source: email trim + EmailStr validation + max 255; password phải là string và không được whitespace-only; không có password-strength policy. Source lookup user, verify stored password hash, và chỉ cho `status == ACTIVE`.
- Success hiện là HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; data profile có id/full_name/email/role/avatar_url/phone/status/timestamps và access_token/refresh_token/token_type/expires_in/refresh_expires_in. Chỉ refresh-token hash được ghi vào DB. Không vẽ/hiển thị token hoặc password hash.
- 401: credentials sai hoặc account không tồn tại; current source trả cùng message “Email hoặc mật khẩu không đúng.”.
- 403: current source từ chối mọi status khác ACTIVE với “Tài khoản không được phép đăng nhập.”; không tự diễn giải chỉ là `LOCKED` và không khẳng định rate limit/lockout.
- 422: `meta.fieldErrors` map tới field. Client có thể trim/format check theo current source; catalog validation boundaries vẫn chưa duyệt.
- 500: chỉ hiển thị thông điệp an toàn “Không thể hoàn tất đăng nhập.”, không đưa raw DB/hash/config detail vào UI.

### API #04 — `GET /api/v1/users/me`

- Chỉ gọi sau khi #03 xác thực role `STUDENT`; dùng Bearer access token. #04 shared guard chặn role khác bằng 403 trước DB.
- API #04 trả current profile; source không có `bio`. Không gọi `/users/me` cho Mentor/Admin.
- Role Mentor/Admin hiện là `G-02 BLOCK`: API #03 có thể trả role token nhưng không có bootstrap profile endpoint phù hợp. Không thể xác định destination thành công của các role này bằng current source.

### Điều hướng

- Brand #1/#2 → `/` (SH-01); link #17 → `/register` (SH-03).
- Sau Student login: gọi #04, rồi chỉ dùng `returnTo` nếu là relative internal route trong allowlist. Default ST-01 `/student` là candidate, chờ product/role-shell xác nhận. Không nhận absolute/external URL.
- API #03 success / API #04 role/source sequencing và token persistence còn discrepancy; không gộp lỗi #03 403 với #04 403.
- R-X01 `POST /api/v1/auth/refresh` có source nhưng không có API ID/contract hiện hành; screen không thêm nút refresh/logout.

## UI states

| State | Điều kiện | Hiển thị và hành vi |
|---|---|---|
| `IDLE` | Mở `/login`, chưa submit | Form trống, button “Đăng nhập”, không alert; chính là ảnh bàn giao. |
| `FOCUS` | Focus field/link/button | Focus ring 2px #0B5F8A offset 2px; không layout shift. |
| `DIRTY` | Có input | Giữ nội dung; cho paste/password manager; chưa gửi request. |
| `CLIENT_VALIDATION` | Submit thiếu/sai input theo policy current source | Email local format/length; password blank/whitespace. Inline error gắn `aria-describedby`. Nếu có nhiều lỗi, summary focusable ở đầu form có link tới field; move focus một lần sau submit. |
| `SUBMITTING` | POST #03 pending | Button đổi thành “Đang đăng nhập…”, disabled để chặn duplicate; không tự retry POST. |
| `AUTH_401` | POST #03 trả 401 | Alert “Email hoặc mật khẩu không đúng.”; giữ email, không nêu field nào sai, không tiết lộ tài khoản tồn tại. |
| `ACCOUNT_INACTIVE_403` | POST #03 trả 403 | Alert dùng current source wording “Tài khoản không được phép đăng nhập.”; policy phân biệt status vẫn chưa được BA/BE chốt. |
| `VALIDATION_422` | POST #03 trả 422 | Đọc fieldErrors từ meta; liên kết field cụ thể. Không tạo password policy ngoài source. |
| `SERVER_500` | POST #03 trả 500 | Alert “Không thể hoàn tất đăng nhập.”; giữ email; không hiện raw detail. |
| `NETWORK_ERROR` | Không nhận được HTTP response | Thông báo kết nối ngắn, cho phép người dùng submit lại chủ động; không tuyên bố đã login. |
| `STUDENT_PROFILE_401/403/500` | #03 đã thành công nhưng #04 lỗi | Tách endpoint context khỏi login errors; #04 403 không được hiển thị như sai credentials. 401/403 về trạng thái SH-05/safe previous route theo router được duyệt. |
| `ROLE_BOOTSTRAP_BLOCK` | #03 success role khác STUDENT | G-02; không gọi #04, không giả dashboard hoặc login failure. Cần quyết định BE/Product trước khi hoàn tất route state. |
| `RETURN_TO_REJECTED` | returnTo là absolute/external hoặc không allowlist | Bỏ giá trị không an toàn; dùng default chỉ khi destination role được phê duyệt. Không redirect external. |

Empty state không áp dụng cho form login. Loading/error không thay đổi main idle screenshot; thông báo động là variants của form, không thêm fake alert vào ảnh mặc định.

## Accessibility và visual tokens

- Font `Noto Sans` system sans fallback; heading #9 40/48/700; editorial heading #4 36/44/700; body 16/26/400; labels 14/20/600; controls 56px.
- Palette: page #F6FAFC; panel #E8F4FA; surface #FFFFFF; primary #0B5F8A; hover #084968; deep #073B57; accent #43A5C5 only decorative; text #17324D; muted #536A7A; border #D4E2E9. Input boundary uses canonical `#536A7A` (5.66:1 against white); focus uses #0B5F8A.
- Form labels are persistent, uniquely associated with inputs. Sequence: brand → email → password → submit → signup. Decorative art `aria-hidden`; no illustration focus.
- Paste/password-manager support; `autocomplete=username` and `current-password`; no token/password in URL, logs, screenshot or visible copy.
- Text contrast ≥4.5:1, control boundary ≥3:1, focus visible and not obscured. Hover 140ms color only; `prefers-reduced-motion` disables nonessential transitions.

## Discrepancies, open decisions, review checklist

| ID | Evidence | Status / impact |
|---|---|---|
| API #03 response/errors | Catalog/DD #03 vs AC/source have status, payload, code discrepancies | `DISCREPANCY / Draft — Needs Confirmation`; UI consumes only current source in implementation, API contract owner must reconcile. |
| API #04 role | Source guard role=STUDENT only | `BLOCK G-02`; do not route Mentor/Admin to Student profile. |
| Token session | Source emits tokens and refreshes, client policy absent | `SOURCE_REQUIRED`; no client persistence assertion. |
| Login destination | returnTo allowlist is target behavior; default route is not approved | `OPEN_DECISION`; ST-01 candidate only. |
| Study Web runtime | No app/router/API consumer source in checkout | `NOT_IMPLEMENTED`; these assets are design-only. |

- [ ] 17 unique markers #1–#17, each 24×24px with white 12px/700 text and 1px white keyline.
- [ ] Clean/annotated geometry matches; only marker layer differs; both PNG 1440×960.
- [ ] Every row has a specific size, font, event, state, responsive and data source; coordinates match SVG.
- [ ] No label, placeholder, button, text, illustration or marker overlap; Vietnamese text glyphs render cleanly.
- [ ] No unsupported recovery/social/OTP/remember-me/session or role-dashboard affordance.
- [ ] Visual review at full resolution complete; no app runtime, live DB or deployment claim.
'''.replace("{ELEMENT_TABLE}", markdown_table())


def chrome_binary() -> str:
    """Find the installed Chrome/Chromium executable used for deterministic SVG rasterization."""
    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("Chrome/Chromium executable is required to render the PNGs")


def render_svg(svg_path: Path, png_path: Path, browser: str) -> None:
    """Render one SVG to a 1440×960 PNG using an isolated temporary Chrome profile."""
    with tempfile.TemporaryDirectory(prefix="sh02-chrome-") as profile:
        command = [
            browser,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--user-data-dir={profile}",
            f"--screenshot={png_path}",
            "--virtual-time-budget=1500",
            svg_path.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=90)
        if result.returncode != 0 or not png_path.exists():
            raise RuntimeError(
                "Chrome render failed. "
                f"stdout={result.stdout[-1000:]} stderr={result.stderr[-2000:]}"
            )


def build() -> None:
    """Write SVG/Markdown, render both images and package the exact SH-02 handoff."""
    clean = build_svg()
    annotated = annotated_svg(clean)
    (ROOT / "SH-02_clean.svg").write_text(clean, encoding="utf-8")
    (ROOT / "SH-02_annotated.svg").write_text(annotated, encoding="utf-8")
    (ROOT / "SCREEN.md").write_text(build_screen_md(), encoding="utf-8")
    browser = chrome_binary()
    render_svg(ROOT / "SH-02_clean.svg", ROOT / "SH-02_clean.png", browser)
    render_svg(ROOT / "SH-02_annotated.svg", ROOT / "SH-02_annotated.png", browser)
    package = ROOT / "SH-02_design_handoff_v1.zip"
    files = (
        "PLAN.md",
        "SCREEN.md",
        "SH-02_clean.png",
        "SH-02_annotated.png",
        "SH-02_clean.svg",
        "SH-02_annotated.svg",
        "learning-book-hero.png",
        "build.py",
    )
    with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(ROOT / name, arcname=name)
    print(f"Wrote {package}")
    print(f"Rendered both PNGs with {browser}; markers={len(MARKERS)}; elements={len(ELEMENTS)}")


if __name__ == "__main__":
    build()
