#!/usr/bin/env python3
"""Giải nén gói DD một cách an toàn và tạo thống kê nguồn, không thực thi file bên trong."""
import argparse, hashlib, json, pathlib, shutil, tarfile, zipfile
MAX_FILES=300
MAX_TOTAL=120*1024*1024
MAX_ONE=40*1024*1024
ALLOWED={'.md','.markdown','.txt','.json','.csv','.html','.png','.jpg','.jpeg','.webp','.svg','.xlsx','.docx','.pdf','.drawio'}

def safe_member(name):
    p=pathlib.PurePosixPath(name.replace('\\','/'))
    if p.is_absolute() or not p.parts or '..' in p.parts or ':' in p.parts[0]:raise ValueError(f'Đường dẫn không an toàn: {name}')
    if p.suffix.lower() not in ALLOWED:return None
    return p

def run(src,out):
    out.mkdir(parents=True,exist_ok=True)
    manifest=[];total=0
    def write(name,by):
        nonlocal total
        p=safe_member(name)
        if p is None:return
        if len(by)>MAX_ONE:raise ValueError('Tệp vượt giới hạn kích thước')
        total+=len(by)
        if total>MAX_TOTAL or len(manifest)>=MAX_FILES:raise ValueError('Gói DD vượt giới hạn an toàn')
        dest=out.joinpath(*p.parts);dest.parent.mkdir(parents=True,exist_ok=True)
        # Không đè các file có cùng đích.
        if dest.exists():raise ValueError(f'Trùng đường dẫn đích: {name}')
        dest.write_bytes(by)
        manifest.append({'duong_dan':str(dest.relative_to(out)).replace('\\','/'), 'dung_luong':len(by),'sha256':hashlib.sha256(by).hexdigest()})
    if src.is_dir():
        for f in sorted(src.rglob('*')):
            if not f.is_file() or f.is_symlink(): continue
            write(str(f.relative_to(src)),f.read_bytes())
    elif src.name.lower().endswith(('.tar.gz','.tgz','.tar')):
        with tarfile.open(src,'r:*') as t:
            for m in t:
                if m.issym() or m.islnk():raise ValueError('Không chấp nhận liên kết trong archive')
                if not m.isfile():continue
                if m.size>MAX_ONE:raise ValueError('Tệp quá lớn')
                with t.extractfile(m) as f:write(m.name,f.read(MAX_ONE+1))
    elif src.suffix.lower()=='.zip':
        with zipfile.ZipFile(src) as z:
            for m in z.infolist():
                if m.is_dir():continue
                if (m.external_attr>>16)&0o170000==0o120000:raise ValueError('Không chấp nhận symlink trong ZIP')
                if m.file_size>MAX_ONE:raise ValueError('Tệp quá lớn')
                with z.open(m) as f:write(m.filename,f.read(MAX_ONE+1))
    else:
        write(src.name,src.read_bytes())
    result={'nguon':str(src),'so_tep':len(manifest),'tong_byte':total,'tep':manifest}
    (out/'danh-muc-nguon.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True)
    a=p.parse_args();d=run(a.input,a.output);print(json.dumps({'so_tep':d['so_tep'],'tong_byte':d['tong_byte'],'thu_muc':str(a.output)},ensure_ascii=False))
