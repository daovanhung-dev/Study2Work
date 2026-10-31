#!/usr/bin/env python3
"""Build the SH-03 visual handoff from editable SVG using local Chrome headless."""

from __future__ import annotations

import base64
import html
import shutil
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1440, 960
FONT = "Noto Sans, Arial, sans-serif"
COLORS = {
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
    "coral": "#E98C72",
    "error": "#B42318",
}


ELEMENTS = [
    {"n": 1, "name": "Study brand mark", "box": (160, 30, 38, 38), "marker": (146, 49), "content": "Open-page glyph", "font": "N/A; hình vector trắng, nét 2px", "visual": "Ô vuông ocean 38×38px, radius 11px; glyph trang mở cân giữa.", "semantic": "Ảnh trang trí trong brand link có accessible name ‘Study, Trang chủ’.", "event": "Click/tap mark hoặc wordmark #2 → `/` (SH-01).", "states": "Hover/pressed theo brand link; focus-visible 2px `#0B5F8A`, offset 2px.", "validation": "Không có; trạng thái link theo điều hướng.", "responsive": "38×38px; hit area brand link tối thiểu 44×44px, không ẩn ở mobile.", "source": "STATIC_UI; nối nhận diện với SH-02."},
    {"n": 2, "name": "Study wordmark", "box": (210, 34, 82, 30), "marker": (306, 49), "content": "Study", "font": "Noto Sans 23px/30px, 700, `#073B57`", "visual": "Text thuần, không nền; đặt cùng baseline với mark #1.", "semantic": "Nội dung text của brand link tới SH-01.", "event": "Click/tap → `/` (SH-01).", "states": "Hover/pressed `#084968`; focus-visible 2px ring trên link cha.", "validation": "Không có.", "responsive": "Giữ wordmark ở mọi breakpoint; không ép xuống dòng.", "source": "STATIC_UI."},
    {"n": 3, "name": "Editorial eyebrow", "box": (212, 582, 282, 18), "marker": (181, 591), "content": "HỌC TẬP BẮT ĐẦU TỪ ĐÂY", "font": "Noto Sans 13px/18px, 700, tracking 0.4px, `#0B5F8A`", "visual": "Chữ hoa màu ocean; thanh nhấn cyan 3×18px ở x=194; không có nền.", "semantic": "Text tĩnh trong phần giới thiệu.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Cho phép wrap có kiểm soát khi cột hẹp; nội dung vẫn là một eyebrow.", "source": "STATIC_UI."},
    {"n": 4, "name": "Editorial heading", "box": (212, 618, 408, 88), "marker": (197, 662), "content": "Bắt đầu hành trình / học tập.", "font": "Noto Sans 36px/44px, 700, `#073B57`", "visual": "Hai dòng, căn trái; weight đậm, không hiệu ứng trang trí trên chữ.", "semantic": "H2 giới thiệu SH-03.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Giữ thứ tự dòng trên desktop; giảm cỡ theo viewport và tránh tràn ở mobile.", "source": "STATIC_UI."},
    {"n": 5, "name": "Editorial supporting copy", "box": (212, 730, 404, 52), "marker": (197, 754), "content": "Tạo tài khoản học viên với họ tên, email và mật khẩu.", "font": "Noto Sans 16px/26px, 400, `#536A7A`", "visual": "Đoạn văn tối đa hai dòng, độ tương phản dịu, căn trái.", "semantic": "Paragraph mô tả ngắn.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Wrap tự nhiên; không ellipsis hoặc cắt câu ở 320px.", "source": "STATIC_UI."},
    {"n": 6, "name": "Minh họa hành trình học tập", "box": (185, 196, 470, 313), "marker": (173, 196), "content": "Notebook ocean, máy bay giấy gấp và đường quỹ đạo; không chứa chữ.", "font": "N/A; artwork vector raster thành PNG trong suốt.", "visual": "Nhóm minh họa riêng 470×313px; notebook đóng ở thấp, các nếp giấy bay lên, chấm coral nhỏ; shadow mềm.", "semantic": "Nhóm decorative, `aria-hidden=true`.", "event": "Không có tương tác hoặc focus.", "states": "Không hover/pressed; không phải control.", "validation": "Không chứa email, token, số liệu hoặc claim.", "responsive": "Giữ aspect ratio khi thu nhỏ; có thể ẩn trên mobile vì không mang nội dung thiết yếu.", "source": "STATIC_UI artwork vector original; `learning-path-hero.svg/png`."},
    {"n": 7, "name": "Registration form surface", "box": (736, 128, 544, 704), "marker": (1300, 139), "content": "Surface chứa form và các control #8–#19.", "font": "N/A.", "visual": "Trắng `#FFFFFF`, border 1px `#D4E2E9`, radius 16px, shadow diffuse 0 20px 56px rgba(7,59,87,.075); padding 48px.", "semantic": "Form surface; click nền không kích hoạt hành động.", "event": "Submit chỉ qua button #17 hoặc Enter trong field.", "states": "Không có hover/pressed riêng; elevation không đổi khi focus field.", "validation": "Bên trong hiển thị lỗi/thông báo theo state, giữ đúng hierarchy.", "responsive": "Desktop 544px; tablet max-width 600px; mobile full-width trong gutter 16px, padding 24px.", "source": "STATIC_UI; vị trí form theo plan SH-03."},
    {"n": 8, "name": "Form eyebrow", "box": (784, 176, 250, 18), "marker": (760, 185), "content": "TÀI KHOẢN HỌC VIÊN", "font": "Noto Sans 13px/18px, 700, tracking 0.5px, `#536A7A`", "visual": "Chữ hoa nhỏ, màu muted; căn trái.", "semantic": "Text tĩnh định danh nhóm form.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Không wrap trong chiều rộng form mobile.", "source": "STATIC_UI."},
    {"n": 9, "name": "Tiêu đề form", "box": (784, 212, 360, 48), "marker": (760, 236), "content": "Tạo tài khoản", "font": "Noto Sans 40px/48px, 700, `#073B57`", "visual": "H1 căn trái, khoảng thở rõ với eyebrow và helper.", "semantic": "H1 duy nhất của screen.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Co font khi card hẹp; tiếng Việt không clip.", "source": "STATIC_UI."},
    {"n": 10, "name": "Form helper", "box": (784, 272, 432, 26), "marker": (760, 285), "content": "Điền thông tin để tạo tài khoản Study.", "font": "Noto Sans 16px/26px, 400, `#536A7A`", "visual": "Một dòng hướng dẫn, không hiển thị policy chưa được source xác nhận.", "semantic": "Paragraph liên kết ngữ cảnh với form.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Có thể wrap thành hai dòng khi card thu hẹp.", "source": "STATIC_UI."},
    {"n": 11, "name": "Nhãn họ và tên", "box": (784, 332, 160, 20), "marker": (760, 342), "content": "Họ và tên", "font": "Noto Sans 14px/20px, 600, `#17324D`", "visual": "Label thường, khoảng cách 8px tới input #12.", "semantic": "`label[for=full_name]`; bấm label đưa focus tới #12.", "event": "Click/tap label → focus input #12.", "states": "Màu giữ nguyên; focus thuộc input.", "validation": "Không có lỗi riêng trên label; lỗi nằm cạnh input/summary.", "responsive": "Luôn hiện phía trên input; không dùng placeholder thay label.", "source": "API #01 field `full_name`."},
    {"n": 12, "name": "Ô họ và tên", "box": (784, 360, 448, 56), "marker": (760, 388), "content": "Placeholder: Nhập họ và tên", "font": "Noto Sans 15px/24px, 400; placeholder `#536A7A`/70%; value `#17324D`", "visual": "Nền trắng, border 1px `#536A7A`, radius 8px, padding ngang 16px; không icon.", "semantic": "Required text input; `name=full_name`, `autocomplete=name`.", "event": "Click/type/paste/autofill; trim khoảng trắng; giới hạn 1–150 ký tự theo validator hiện hành.", "states": "Hover border `#084968`; focus 2px ring `#0B5F8A` offset 2px; invalid dùng border `#B42318` + thông báo có text.", "validation": "Empty/whitespace hoặc >150 ký tự bị từ chối theo client/server validator; error liên kết qua `aria-describedby`.", "responsive": "Full width; cao 56px; bàn phím mobile phù hợp văn bản.", "source": "API #01 current validator và `RegisterRequest.full_name`."},
    {"n": 13, "name": "Nhãn email", "box": (784, 436, 120, 20), "marker": (760, 446), "content": "Email", "font": "Noto Sans 14px/20px, 600, `#17324D`", "visual": "Label thường; khoảng cách 8px tới input #14.", "semantic": "`label[for=email]`; bấm label đưa focus tới #14.", "event": "Click/tap label → focus input #14.", "states": "Màu giữ nguyên; focus thuộc input.", "validation": "Không có lỗi riêng trên label.", "responsive": "Luôn hiện phía trên input.", "source": "API #01 field `email`."},
    {"n": 14, "name": "Ô email", "box": (784, 464, 448, 56), "marker": (760, 492), "content": "Placeholder: Nhập email của bạn", "font": "Noto Sans 15px/24px, 400; placeholder `#536A7A`/70%; value `#17324D`", "visual": "Nền trắng, border 1px `#536A7A`, radius 8px, padding ngang 16px; không thêm icon/claim.", "semantic": "Required `type=email`, `inputmode=email`, `autocomplete=email`.", "event": "Click/type/paste/autofill; gửi email sau khi trim; không tự lower-case.", "states": "Hover/focus như #12; 409 duplicate hiển thị `Email đã tồn tại.` cạnh trường; invalid border + text error.", "validation": "EmailStr format, nonblank và max 255 theo current validator; lỗi 422 map từ `meta.fieldErrors`.", "responsive": "Full width 448×56px desktop; full-width theo card ở mobile.", "source": "API #01 current `EmailStr`/validator; 409 `DESIGN_STATE_CONFLICT`."},
    {"n": 15, "name": "Nhãn mật khẩu", "box": (784, 540, 120, 20), "marker": (760, 550), "content": "Mật khẩu", "font": "Noto Sans 14px/20px, 600, `#17324D`", "visual": "Label thường; khoảng cách 8px tới input #16.", "semantic": "`label[for=password]`; bấm label đưa focus tới #16.", "event": "Click/tap label → focus input #16.", "states": "Màu giữ nguyên; focus thuộc input.", "validation": "Không có lỗi riêng trên label.", "responsive": "Luôn hiện phía trên input.", "source": "API #01 field `password`."},
    {"n": 16, "name": "Ô mật khẩu", "box": (784, 568, 448, 56), "marker": (760, 596), "content": "Placeholder: Nhập mật khẩu; giá trị được che", "font": "Noto Sans 15px/24px, 400, `#17324D`", "visual": "Nền trắng, border 1px `#536A7A`, radius 8px, padding ngang 16px; không icon reveal.", "semantic": "Required `type=password`, `autocomplete=new-password`.", "event": "Click/type/paste/autofill; chỉ gửi trong POST JSON khi submit.", "states": "Hover/focus như #12; invalid có text/error border; không strength meter.", "validation": "Current source chỉ reject blank/whitespace; không suy ra độ dài tối thiểu hoặc complexity.", "responsive": "Full width 448×56px; giữ password-manager support và không lưu vào local storage.", "source": "API #01 current validator."},
    {"n": 17, "name": "Nút tạo tài khoản", "box": (784, 656, 448, 56), "marker": (760, 684), "content": "Tạo tài khoản", "font": "Noto Sans 16px/24px, 600, trắng", "visual": "Nền `#0B5F8A`, radius 8px, shadow nhẹ; full-width; label căn giữa.", "semantic": "Submit button duy nhất của form.", "event": "Click/tap hoặc Enter → validate → `POST /api/v1/auth/register` với `{email,password,full_name}`, không Authorization.", "states": "Hover/pressed `#084968` trong 140ms; focus ring 2px; loading label `Đang tạo tài khoản…`, disabled để chống double submit.", "validation": "Client validation trước request; 201 handoff, 409 duplicate, 422 field errors, 500 safe message; không tự retry mutation.", "responsive": "Full width, cao 56px (đạt hit target mobile).", "source": "API #01 route/source; expected SH-03 flow từ inventory."},
    {"n": 18, "name": "Lời nhắc tài khoản hiện có", "box": (872, 736, 150, 22), "marker": (850, 773), "content": "Đã có tài khoản?", "font": "Noto Sans 15px/22px, 400, `#536A7A`", "visual": "Văn bản tĩnh trong hàng footer; không có nền riêng.", "semantic": "Text dẫn trước liên kết #19.", "event": "Không có tương tác.", "states": "Không hover/focus/pressed.", "validation": "Không áp dụng.", "responsive": "Có thể wrap trên màn nhỏ; giữ liền ngữ nghĩa với link #19.", "source": "STATIC_UI."},
    {"n": 19, "name": "Liên kết đăng nhập", "box": (1038, 736, 118, 22), "marker": (1175, 747), "content": "Đăng nhập", "font": "Noto Sans 15px/22px, 600, `#0B5F8A`", "visual": "Text link gạch chân mảnh, không button fill.", "semantic": "Anchor tới route target `/login` (SH-02).", "event": "Click/tap → SH-02.", "states": "Hover `#084968`, underline đậm hơn; focus-visible 2px ring; hit target mở rộng ≥44×44px.", "validation": "Không có.", "responsive": "Không tách khỏi lời nhắc; wrap có kiểm soát ở card hẹp.", "source": "SH-03 inventory; SH-02 linked screen."},
]


def svg_defs() -> str:
    return '''<defs>
      <linearGradient id="panelGradient" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#EEF7FB"/><stop offset="1" stop-color="#E8F4FA"/>
      </linearGradient>
      <linearGradient id="buttonGradient" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#0D6894"/><stop offset="1" stop-color="#0B5F8A"/>
      </linearGradient>
      <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="140%">
        <feDropShadow dx="0" dy="18" stdDeviation="25" flood-color="#073B57" flood-opacity=".075"/>
      </filter>
      <filter id="buttonShadow" x="-12%" y="-20%" width="124%" height="150%">
        <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#073B57" flood-opacity=".13"/>
      </filter>
      <filter id="badgeShadow" x="-35%" y="-35%" width="170%" height="170%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#073B57" flood-opacity=".23"/>
      </filter>
      <radialGradient id="panelLight">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity=".72"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
      </radialGradient>
    </defs>'''


def hero_art_svg() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="470" height="313" viewBox="0 0 470 313">
  <defs>
    <linearGradient id="cover" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#147CA2"/><stop offset=".55" stop-color="#0B5F8A"/><stop offset="1" stop-color="#073B57"/></linearGradient>
    <linearGradient id="pages" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#DDEEF4"/></linearGradient>
    <linearGradient id="planeLight" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#D8EDF4"/></linearGradient>
    <linearGradient id="planeBlue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#64BBD1"/><stop offset="1" stop-color="#0B5F8A"/></linearGradient>
    <filter id="float" x="-35%" y="-45%" width="180%" height="200%"><feDropShadow dx="0" dy="9" stdDeviation="8" flood-color="#073B57" flood-opacity=".19"/></filter>
    <filter id="soft" x="-50%" y="-80%" width="200%" height="260%"><feGaussianBlur stdDeviation="8"/></filter>
  </defs>
  <ellipse cx="247" cy="239" rx="139" ry="20" fill="#0B5F8A" opacity=".11" filter="url(#soft)"/>
  <path d="M37 167C68 107 124 99 173 133c58 40 91 38 130-14 35-47 79-62 119-37" fill="none" stroke="#43A5C5" stroke-width="1.4" opacity=".44"/>
  <path d="M56 82c32-30 77-37 111-13 31 22 43 42 68 41" fill="none" stroke="#0B5F8A" stroke-width="1" opacity=".23"/>
  <path d="M313 63c46-36 99-22 120 18 13 24 8 48-8 69" fill="none" stroke="#43A5C5" stroke-width="1.1" opacity=".4"/>
  <path d="M77 190c31 9 57 5 79-12" fill="none" stroke="#0B5F8A" stroke-width="1" opacity=".2"/>
  <circle cx="91" cy="95" r="4.4" fill="#43A5C5"/><circle cx="91" cy="95" r="9" fill="#43A5C5" opacity=".12"/>
  <circle cx="394" cy="112" r="4" fill="#E98C72"/><circle cx="394" cy="112" r="10" fill="#E98C72" opacity=".14"/>
  <circle cx="347" cy="54" r="3" fill="#0B5F8A" opacity=".7"/><circle cx="131" cy="155" r="3.5" fill="#0B5F8A" opacity=".58"/>
  <g transform="translate(82 83) rotate(-14 45 24)" filter="url(#float)">
    <path d="M0 34 95 1 57 66 44 43 23 52 34 35Z" fill="url(#planeLight)"/>
    <path d="M0 34 95 1 34 35Z" fill="#FFFFFF"/>
    <path d="M34 35 95 1 57 66 44 43Z" fill="#B9DCE8"/>
    <path d="M0 34 44 43 57 66Z" fill="#83C8D8"/>
    <path d="M44 43 95 1" fill="none" stroke="#A9D5E2" stroke-width="1"/>
  </g>
  <g transform="translate(269 34) rotate(9 45 26)" filter="url(#float)">
    <path d="M0 37 112 0 68 78 53 50 27 59 41 39Z" fill="url(#planeLight)"/>
    <path d="M0 37 112 0 41 39Z" fill="#FFFFFF"/>
    <path d="M41 39 112 0 68 78 53 50Z" fill="#C6E3EB"/>
    <path d="M0 37 53 50 68 78Z" fill="url(#planeBlue)"/>
    <path d="M53 50 112 0" fill="none" stroke="#9DCFDA" stroke-width="1"/>
  </g>
  <g transform="translate(308 126) rotate(-12 22 12) scale(.55)" opacity=".92">
    <path d="M0 28 83 0 51 57 39 37 20 43 30 29Z" fill="url(#planeLight)"/>
    <path d="M0 28 83 0 30 29Z" fill="#FFFFFF"/>
    <path d="M30 29 83 0 51 57 39 37Z" fill="#B9DCE8"/>
    <path d="M0 28 39 37 51 57Z" fill="#43A5C5"/>
  </g>
  <path d="M190 111c20 21 33 39 43 66" fill="none" stroke="#43A5C5" stroke-width="1.2" stroke-dasharray="2 6" opacity=".55"/>
  <circle cx="232" cy="175" r="4" fill="#E98C72"/>
  <g transform="translate(103 180) rotate(-6 132 29)" filter="url(#float)">
    <path d="M8 21 245 0 265 16 32 50Z" fill="#073B57" opacity=".95"/>
    <path d="M17 9 244 0 263 15 31 45Z" fill="url(#pages)" stroke="#C7E0E9" stroke-width="1"/>
    <path d="m17 9 112 15 134-9-19-15Z" fill="#FFFFFF"/>
    <path d="M129 24 31 45l-1 8 100-19 133-12v-7Z" fill="#D9EAF0"/>
    <path d="m129 24 2 10 132-19-1-8Z" fill="#EEF7FA"/>
    <path d="M31 45 30 53 267 19l-4-4Z" fill="url(#cover)"/>
    <path d="M31 45 129 24l2 10-100 19Z" fill="#0B5F8A"/>
    <path d="M126 25 131 25 134 33 130 35Z" fill="#43A5C5" opacity=".82"/>
    <path d="M43 39 113 26M46 42 116 29M149 23l90-13M152 26l90-13" stroke="#B6D5E0" stroke-width=".8" opacity=".75"/>
    <path d="M42 47 114 33" stroke="#43A5C5" stroke-width="1" opacity=".7"/>
    <circle cx="240" cy="7" r="2" fill="#E98C72"/>
  </g>
  <path d="M221 213c23 7 39 6 59-2" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity=".8"/>
  <circle cx="151" cy="67" r="2" fill="#FFFFFF" opacity=".9"/><circle cx="369" cy="155" r="2" fill="#FFFFFF" opacity=".8"/>
</svg>'''


def svg_text(x: int, y: int, value: str, size: int, color: str, weight: int = 400,
             extra: str = "") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}px" '
            f'font-weight="{weight}" fill="{color}" {extra}>{html.escape(value)}</text>')


def screen_svg(art_data: str, annotated: bool = False) -> str:
    c = COLORS
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">', svg_defs()]
    parts += [f'<rect width="1440" height="960" fill="{c["page"]}"/>',
              '<rect width="1440" height="96" fill="#FFFFFF"/>',
              f'<path d="M0 95.5H1440" stroke="{c["border"]}" stroke-opacity=".7"/>',
              '<rect x="160" y="128" width="520" height="704" rx="16" fill="url(#panelGradient)"/>',
              '<ellipse cx="493" cy="294" rx="193" ry="155" fill="url(#panelLight)" opacity=".78"/>',
              '<rect x="736" y="128" width="544" height="704" rx="16" fill="#FFFFFF" stroke="#D4E2E9" filter="url(#cardShadow)"/>']

    # Header brand
    parts += ['<a href="/" aria-label="Study, Trang chủ">',
              '<rect x="160" y="30" width="38" height="38" rx="11" fill="#0B5F8A"/>',
              '<path d="M169 39h8l8 7v14h-16z" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round"/>',
              '<path d="M177 39v8h8M172.5 51.5h9M172.5 55.5h9" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>',
              f'<text x="210" y="58" font-family="{FONT}" font-size="23px" font-weight="700" fill="#073B57">Study</text>', '</a>']

    # Editorial left panel
    parts += [f'<image x="185" y="196" width="470" height="313" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{art_data}"/>',
              '<rect x="194" y="582" width="3" height="18" rx="1.5" fill="#43A5C5"/>',
              f'<text x="212" y="596" font-family="{FONT}" font-size="13px" font-weight="700" letter-spacing=".4px" fill="#0B5F8A">HỌC TẬP BẮT ĐẦU TỪ ĐÂY</text>',
              f'<text x="212" y="650" font-family="{FONT}" font-size="36px" font-weight="700" letter-spacing="-.55px" fill="#073B57">Bắt đầu hành trình</text>',
              f'<text x="212" y="694" font-family="{FONT}" font-size="36px" font-weight="700" letter-spacing="-.55px" fill="#073B57">học tập.</text>',
              f'<text x="212" y="750" font-family="{FONT}" font-size="16px" font-weight="400" fill="#536A7A">Tạo tài khoản học viên với họ tên, email và</text>',
              f'<text x="212" y="776" font-family="{FONT}" font-size="16px" font-weight="400" fill="#536A7A">mật khẩu.</text>']

    # Form content
    parts += [f'<text x="784" y="190" font-family="{FONT}" font-size="13px" font-weight="700" letter-spacing=".5px" fill="#536A7A">TÀI KHOẢN HỌC VIÊN</text>',
              f'<text x="784" y="248" font-family="{FONT}" font-size="40px" font-weight="700" letter-spacing="-.65px" fill="#073B57">Tạo tài khoản</text>',
              f'<text x="784" y="293" font-family="{FONT}" font-size="16px" font-weight="400" fill="#536A7A">Điền thông tin để tạo tài khoản Study.</text>']

    def field(label: str, label_y: int, box_y: int, placeholder: str, kind: str = "text") -> list[str]:
        color = "#536A7A"
        arr = [f'<text x="784" y="{label_y + 16}" font-family="{FONT}" font-size="14px" font-weight="600" fill="#17324D">{html.escape(label)}</text>',
               f'<rect x="784" y="{box_y}" width="448" height="56" rx="8" fill="#FFFFFF" stroke="#536A7A" stroke-width="1"/>']
        arr.append(f'<text x="801" y="{box_y + 35}" font-family="{FONT}" font-size="15px" font-weight="400" fill="{color}" opacity=".76">{html.escape(placeholder)}</text>')
        return arr

    parts += field("Họ và tên", 332, 360, "Nhập họ và tên")
    parts += field("Email", 436, 464, "Nhập email của bạn", "email")
    parts += field("Mật khẩu", 540, 568, "Nhập mật khẩu", "password")

    parts += ['<rect x="784" y="656" width="448" height="56" rx="8" fill="url(#buttonGradient)" filter="url(#buttonShadow)"/>',
              f'<text x="1008" y="691" text-anchor="middle" font-family="{FONT}" font-size="16px" font-weight="600" fill="#FFFFFF">Tạo tài khoản</text>',
              f'<text x="872" y="752" font-family="{FONT}" font-size="15px" font-weight="400" fill="#536A7A">Đã có tài khoản?</text>',
              '<a href="/login" aria-label="Đăng nhập">',
              f'<text x="1038" y="752" font-family="{FONT}" font-size="15px" font-weight="600" text-decoration="underline" text-decoration-thickness="1px" text-underline-offset="3px" fill="#0B5F8A">Đăng nhập</text>', '</a>']

    if annotated:
        for item in ELEMENTS:
            n = item["n"]
            x, y = item["marker"]
            # Surface marker is held just outside its top-right edge; other markers sit in whitespace beside the target.
            if n == 7:
                parts.append('<path d="M1280 139h8" stroke="#0B5F8A" stroke-width="1.2" opacity=".8"/>')
            parts.append(f'<g filter="url(#badgeShadow)"><circle cx="{x}" cy="{y}" r="12" fill="#0B5F8A" stroke="#FFFFFF" stroke-width="2"/><text x="{x}" y="{y + 4}" text-anchor="middle" font-family="{FONT}" font-size="11px" font-weight="700" fill="#FFFFFF">{n}</text></g>')

    parts.append('</svg>')
    return "\n".join(parts)


def screen_document() -> str:
    rows = []
    for item in ELEMENTS:
        x, y, w, h = item["box"]
        mx, my = item["marker"]
        cells = [f"**#{item['n']} — {item['name']}**<br>{html.escape(item['content'])}",
                 f"`x={x}, y={y}, w={w}, h={h}` px<br>Marker center `({mx}, {my})` in annotated PNG.",
                 f"{item['visual']}<br><br>**Font:** {item['font']}<br>**Color:** see exact token values above and `PLAN.md`.",
                 item["semantic"], item["event"], item["states"],
                 f"**Validation/loading:** {item['validation']}<br><br>**Responsive:** {item['responsive']}<br><br>**Source:** {item['source']}"]
        rows.append("| " + " | ".join(cell.replace("|", "&#124;").replace("\n", " ") for cell in cells) + " |")

    return f'''# SH-03 — Đặc tả thiết kế màn hình đăng ký học viên

> **Artifact status:** DESIGN TARGET / NOT IMPLEMENTED. `apps/study-client/` chưa có Study Web runtime/router cho screen này. Ảnh là visual handoff tĩnh, không chứng minh form đang chạy.

## Tóm tắt thiết kế

- **Screen:** SH-03 — Đăng ký học viên; route mục tiêu `/register`; actor Guest; luồng AC-01.
- **Canvas ảnh:** 1440×960px; vùng nội dung rộng 1120px, đặt giữa; header trắng cao 96px.
- **Art direction:** editorial, yên tĩnh, tạo cảm giác bắt đầu một hành trình; panel trái có minh họa giấy gấp riêng, form phải ưu tiên đọc nhanh và thao tác dễ.
- **Tham chiếu:** cùng Study ocean palette và brand với SH-02; artwork khác hình sách mở của SH-02.
- **Font:** Noto Sans; fallback `Arial, sans-serif`. Kích thước và line-height theo từng element bên dưới.
- **Màu:** primary `#0B5F8A`; hover `#084968`; deep `#073B57`; cyan `#43A5C5` (decorative); soft `#E8F4FA`; page `#F6FAFC`; surface `#FFFFFF`; text `#17324D`; muted `#536A7A`; border `#D4E2E9`; error `#B42318`; coral `#E98C72` (chỉ artwork).
- **Thành phần ngoài 19 target:** không có navigation phụ, consent checkbox, icon social, CAPTCHA, OTP, password confirmation, meter hoặc modal.

## Bố cục

| Vùng | Bounds | Cấu trúc |
|---|---:|---|
| Header | `0,0,1440,96` | Nền trắng, hairline dưới; Study brand link ở đầu trái. |
| Editorial panel | `160,128,520,704` | Nền gradient rất nhẹ `#EEF7FB`→`#E8F4FA`, radius 16px; artwork trên, copy ở nửa dưới. |
| Registration surface | `736,128,544,704` | Trắng, viền 1px, radius 16px, shadow mềm, padding 48px. |
| Form content | `784,176,448,582` | Eyebrow, H1, helper, ba cặp label/input, nút submit, sign-in link. |

## Bản đồ element

Mỗi marker trên `SH-03_annotated.png` tương ứng một hàng trong bảng; `SH-03_clean.png` là cùng layout không có marker. Cỡ chữ dưới đây tính bằng px, ghi `font-size/line-height/weight`.

| Element và nội dung | Bounding box | Visual, typography và màu | Semantic | Click/tap | Hover, focus, pressed | Validation, loading và responsive |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Luồng tương tác và trạng thái

| State | Kích hoạt | Kết quả thiết kế |
|---|---|---|
| `IDLE` | Guest mở `/register` | Ảnh clean thể hiện ba trường rỗng, label rõ, button khả dụng; không có error, sample account hoặc claim email. |
| `FOCUS / TOUCHED` | Tập trung/blur field | Focus ring 2px `#0B5F8A`, offset 2px; không layout shift. Sau blur chỉ hiển thị lỗi khi dữ liệu không hợp lệ. |
| `CLIENT_VALIDATION` | Submit dữ liệu trống/sai | Họ tên trim 1–150; email trim/format/max 255; password nonblank. Gắn lỗi qua `aria-describedby`; lỗi nhiều trường có summary liên kết và focus được. |
| `SUBMITTING` | Form hợp lệ, request #01 đang chờ | Đổi label button thành `Đang tạo tài khoản…`, disable nút và chặn submit lặp; không tự retry. |
| `REGISTER_201_HANDOFF` | #01 trả HTTP 201 | Target flow chuyển SH-04 bằng `data.id`/`data.email`. Chỉ xác nhận tạo account theo response; không nói email đã gửi/verified. Cách vận chuyển state sang SH-04 còn cần quyết định. |
| `EMAIL_CONFLICT_409` | #01 trả 409 `DESIGN_STATE_CONFLICT` | Hiện `Email đã tồn tại.` ở field email và alert gọn; giữ họ tên/email, bỏ giá trị password sau response; cho phép sửa hoặc sang SH-02. |
| `VALIDATION_422` | #01 trả 422 `DESIGN_VALIDATION_ERROR` | Map `meta.fieldErrors` vào field; summary nếu nhiều field; không tự thêm chính sách mật khẩu. |
| `SERVER_500` | #01 trả `DESIGN_INTERNAL_ERROR` | Hiện câu an toàn `Không thể tạo tài khoản.`; giữ dữ liệu không nhạy cảm; không render stack/SQL/hash. |
| `NETWORK_UNKNOWN` | Không nhận HTTP response | Báo rằng chưa xác nhận hoàn tất; không retry mutation tự động; không khẳng định account được tạo. Giữ họ tên/email, không lưu password lâu dài. |

## API và screen liên quan: expected / current

| Mốc | Expected từ inventory/DD | Current source được kiểm tra | Tác động lên screen |
|---|---|---|---|
| Submit #01 | `POST /api/v1/auth/register`; body `email`, `password`, `full_name`; 201 trả `data.id`, `data.email`; 409 giữ trên form. | Public route 201; trim/validate email bằng `EmailStr`, max 255; password chỉ từ chối blank/whitespace; full_name trim 1–150; duplicate trả 409; hash Argon2id; insert role `STUDENT`; success không trả password/hash. | Form chỉ có đúng ba field; không thêm complexity/strength rules; phân biệt lỗi 409/422/500 như bảng state. |
| #01 sau commit | Inventory mô tả bước xác minh tiếp theo. | Current #01 chỉ log `verification_dispatch_pending`, không gọi API #02. Account status phụ thuộc default DB; live DB chưa được xác minh. | Giữ discrepancy; không hiển thị/promise status account. |
| SH-04 / #02 | SH-04 là screen kế tiếp trong inventory; gửi `user_id`/`email`, HTTP 202 được chấp nhận. | Provider mặc định là stub `accepted`; không gửi email thật và không tạo token/link. #02 là route độc lập, không được #01 gọi. | Link/transition tới SH-04 thuộc expected journey; tuyệt đối không ghi “email đã gửi” hoặc “đã xác minh”. SH-04 được mô tả riêng, không phải child-screen trong folder này. |
| DD status | API #01/#02 DD còn Draft — Needs Confirmation. | #01 response source không có `bio` như DD liệt kê; một số account/normalization/dispatch policy còn open. | Không đưa `bio`, token, trạng thái `ACTIVE`, hoặc claim chưa có source vào UI. |

**Expected flow:** SH-03 → API #01 → HTTP 201 và `data.id`/`data.email` → SH-04 → API #02 → accepted theo stub hiện tại; sau đó SH-02 theo journey.  
**Current implementation:** màn Study Web chưa có runtime; API #01 đăng ký và ghi log pending nhưng không gọi #02; API #02 dùng stub mặc định. Đây là discrepancy cần giữ nguyên trong handoff.

## Liên kết screen

| Nguồn | Sự kiện | Đích |
|---|---|---|
| Brand mark #1 / wordmark #2 | Click/tap | `/` — SH-01 (route mục tiêu). |
| Submit #17 khi API #01 trả 201 | Handoff theo expected AC-01 | SH-04 `/register/verification` (screen độc lập, ngoài phạm vi package này). |
| Link #19 | Click/tap | `/login` — SH-02 cho tài khoản đã có. |

## Accessibility và responsive

- Thứ tự bàn phím: brand → họ tên → email → mật khẩu → submit → đăng nhập.
- Label cố định cho mỗi field; lỗi có text, được nối `aria-describedby`; summary nhiều lỗi có thể focus và liên kết tới field.
- Body text cần đạt contrast ≥4.5:1; boundary field ≥3:1; không dùng màu làm dấu hiệu lỗi duy nhất; focus ring không bị clip.
- Hover/focus transition chỉ đổi màu/underline trong 140ms, không dịch layout; tôn trọng `prefers-reduced-motion`.
- 1440px: layout hai cột như hình. 768–1023px: panel được thu gọn hoặc ẩn để card tối đa 600px. 320–767px: gutter 16px, card full-width, padding 24px, control 56px cao, không scroll ngang; minh họa có thể ẩn.

## Quyết định còn mở

1. API #01 DD đang Draft: xác nhận account status/default, response profile, email case-normalization và policy mật khẩu trước khi biến target thành runtime.
2. Inventory yêu cầu follow-up SH-04 nhưng source #01 không gọi #02: cần product/backend quyết định owner và điểm dispatch verification.
3. Handoff `data.id`/`data.email` qua route/state tới SH-04 chưa có contract transport trong web client.
4. Không có contract đồng ý điều khoản nên screen không render consent checkbox.

## File trong gói

- `SH-03_clean.png`, `SH-03_annotated.png`: hai ảnh canvas 1440×960.
- `SH-03_clean.svg`, `SH-03_annotated.svg`: vector source; artwork PNG được embed để mở độc lập.
- `learning-path-hero.svg`, `learning-path-hero.png`: artwork riêng, PNG nền trong suốt.
- `PLAN.md`: plan source-backed cho screen; `build.py`: script dựng và đóng zip.
- `SH-03_design_handoff_v1.zip`: archive chứa đầy đủ các file trên cùng SCREEN.md.
'''


def render(svg_path: Path, output_path: Path, size: tuple[int, int]) -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        raise RuntimeError("Không tìm thấy Chrome/Chromium headless để raster SVG.")
    with tempfile.TemporaryDirectory(prefix="sh03-chrome-") as profile:
        command = [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
                   "--disable-dev-shm-usage", "--hide-scrollbars", "--force-device-scale-factor=1",
                   "--default-background-color=00000000", f"--user-data-dir={profile}",
                   f"--window-size={size[0]},{size[1]}", f"--screenshot={output_path}", svg_path.resolve().as_uri()]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=45)
        if completed.returncode != 0 or not output_path.exists():
            raise RuntimeError(f"Chrome render thất bại: {completed.stderr[-2000:]}")


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"Không phải PNG hợp lệ: {path.name}")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    hero_path = ROOT / "learning-path-hero.svg"
    hero_png = ROOT / "learning-path-hero.png"
    hero_path.write_text(hero_art_svg(), encoding="utf-8")
    render(hero_path, hero_png, (470, 313))
    art_data = base64.b64encode(hero_png.read_bytes()).decode("ascii")

    clean_svg = ROOT / "SH-03_clean.svg"
    annotated_svg = ROOT / "SH-03_annotated.svg"
    clean_png = ROOT / "SH-03_clean.png"
    annotated_png = ROOT / "SH-03_annotated.png"
    clean_svg.write_text(screen_svg(art_data), encoding="utf-8")
    annotated_svg.write_text(screen_svg(art_data, annotated=True), encoding="utf-8")
    render(clean_svg, clean_png, (WIDTH, HEIGHT))
    render(annotated_svg, annotated_png, (WIDTH, HEIGHT))

    for image in (clean_png, annotated_png):
        if png_dimensions(image) != (WIDTH, HEIGHT):
            raise RuntimeError(f"Sai kích thước {image.name}: {png_dimensions(image)}")
    if png_dimensions(hero_png) != (470, 313):
        raise RuntimeError(f"Sai kích thước artwork: {png_dimensions(hero_png)}")

    screen_path = ROOT / "SCREEN.md"
    screen_path.write_text(screen_document(), encoding="utf-8")
    archive = ROOT / "SH-03_design_handoff_v1.zip"
    members = ["PLAN.md", "SCREEN.md", "SH-03_clean.png", "SH-03_annotated.png",
               "SH-03_clean.svg", "SH-03_annotated.svg", "learning-path-hero.png",
               "learning-path-hero.svg", "build.py"]
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as bundle:
        for name in members:
            bundle.write(ROOT / name, arcname=name)
    with zipfile.ZipFile(archive) as bundle:
        if set(bundle.namelist()) != set(members) or bundle.testzip() is not None:
            raise RuntimeError("ZIP không đầy đủ hoặc có member hỏng.")
    print(f"Built SH-03 in {ROOT}")
    print(f"PNG: {png_dimensions(clean_png)}, {png_dimensions(annotated_png)}; hero: {png_dimensions(hero_png)}")
    print(f"ZIP: {archive.name} ({archive.stat().st_size} bytes; {len(members)} members)")


if __name__ == "__main__":
    main()
