#!/usr/bin/env python3
"""Structural checks only. Does not verify logic, API contract or screenshot annotations."""
from pathlib import Path
import argparse
import re
import sys

REQUIRED = [
    '00-overview.md', '01-ui-elements.md', '02-events.md', '03-data-flow.md',
    '04-api-integration.md', '05-business-rules.md', '06-navigation.md',
    '07-test-cases.md'
]
LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
SCREEN = r'(?:SH|GS|ST|ME|AD)-\d{2,3}'
ID = re.compile(rf'\b({SCREEN}-(?:EL|EV|API|BR|TC)-\d{{3}})\b')
DECL = re.compile(rf'^#{{2,4}}\s+(?:\d+\.\s+)?({SCREEN}-(?:EL|EV|API|BR|TC)-\d{{3}})\b', re.M)


def check(screen):
    errors, warns = [], []
    if not screen.is_dir(): return [f'Folder not found: {screen}'], []
    text = {}
    for filename in REQUIRED:
        p = screen / filename
        if not p.exists(): errors.append(f'Missing: {filename}'); continue
        content = p.read_text(encoding='utf8')
        text[filename] = content
        if not content.strip(): errors.append(f'Empty: {filename}')
        if '{{' in content and '}}' in content: warns.append(f'Unfilled placeholders: {filename}')
        for url in LINK.findall(content):
            if url.startswith(('http://','https://','#','mailto:')): continue
            target = (p.parent / url.split('#')[0]).resolve()
            if not target.exists(): errors.append(f'Broken link in {filename}: {url}')
    for filename in ('screen-clean.png','screen-numbered.png'):
        if not (screen / 'images' / filename).exists(): errors.append(f'Missing image: images/{filename}')
    overview = text.get('00-overview.md','')
    found = re.search(rf'^#\s+({SCREEN})\b', overview, re.M)
    if not found: warns.append('No supported Screen ID heading in overview')
    elif not screen.name.startswith(found.group(1)): warns.append('Screen ID mismatch vs folder name')
    for filename, c in text.items():
        if not c.startswith('# '): warns.append(f'Missing top-level heading: {filename}')
    # A deliberately shallow cross-check of IDs, not semantic coverage.
    decl = set()
    for c in text.values(): decl |= set(DECL.findall(c))
    for prefix, filename in [('EL','01-ui-elements.md'), ('EV','02-events.md'), ('API','04-api-integration.md'), ('BR','05-business-rules.md'), ('TC','07-test-cases.md')]:
        body=text.get(filename,'')
        if not re.search(SCREEN+r'-'+prefix+r'-\d{3}', body):
            warns.append(f'No {prefix} IDs in owning document: {filename}')
    return errors, warns


def main():
    parser=argparse.ArgumentParser(description='Validate DD screen structure/links (not behavior)')
    parser.add_argument('paths', nargs='+', help='Screen directories')
    args=parser.parse_args(); all_errors=0
    for s in args.paths:
        screen=Path(s).resolve(); errors,warns=check(screen); all_errors += len(errors)
        print(f'\n{screen.name}: {"FAILED" if errors else "PASS"}')
        for e in errors: print('  ERROR:',e)
        for w in warns: print('  WARN: ',w)
    sys.exit(1 if all_errors else 0)

if __name__=='__main__': main()
