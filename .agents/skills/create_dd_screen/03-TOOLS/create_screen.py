#!/usr/bin/env python3
"""Create an eight-file DD screen scaffold from DD-Screen-Kit templates (stdlib only)."""
from pathlib import Path
from datetime import date
import argparse
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '01-TEMPLATES' / 'SCREEN_ID'


def main():
    p = argparse.ArgumentParser(description='Create a DD screen skeleton')
    p.add_argument('--id', required=True, help='Screen ID, e.g. SH-03')
    p.add_argument('--slug', required=True, help='PascalCase folder suffix, e.g. MyCourses')
    p.add_argument('--title', required=True, help='Vietnamese screen title')
    p.add_argument('--route', required=True, help='Route pattern, e.g. /my-courses')
    p.add_argument('--output', default='./MY-SCREENS', help='Destination root directory')
    a = p.parse_args()
    if not re.fullmatch(r'SH-\d{2,3}', a.id): p.error('--id phải có dạng SH-03 hoặc SH-123')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', a.slug): p.error('--slug phải là tên thư mục an toàn')
    dst = Path(a.output).expanduser().resolve() / f'{a.id}-{a.slug}'
    if dst.exists(): p.error(f'Đích đã tồn tại, sẽ không ghi đè: {dst}')
    shutil.copytree(SRC, dst)
    replacements = {
        '{{SCREEN_ID}}': a.id, '{{SCREEN_TITLE}}': a.title,
        '{{SCREEN_SLUG}}': a.slug, '{{ROUTE}}': a.route,
        '{{DATE}}': date.today().isoformat(),
    }
    for file in dst.rglob('*.md'):
        content = file.read_text(encoding='utf8')
        for old, new in replacements.items(): content = content.replace(old, new)
        file.write_text(content, encoding='utf8')
    print('Created:', dst)
    print('Next: add screen-clean.png and screen-numbered.png, replace remaining {{PLACEHOLDERS}},')
    print('then run: python3 03-TOOLS/validate_dd.py "' + str(dst) + '"')

if __name__ == '__main__': main()
