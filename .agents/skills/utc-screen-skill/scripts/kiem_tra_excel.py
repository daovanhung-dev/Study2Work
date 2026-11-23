#!/usr/bin/env python3
"""Kiểm tra cấu trúc .xlsx bằng thư viện chuẩn (CHỈ ĐỌC), không sửa bảng tính."""
import argparse,re,sys,zipfile,xml.etree.ElementTree as ET,json
from pathlib import Path
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REQUIRED=['01. Bìa','02. Tổng quan','03. Thành phần','04. Sự kiện']

def inspect(path):
    issues=[];names=[]; formula_count=0;errors=[]
    with zipfile.ZipFile(path) as z:
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        names=[s.attrib['name'] for s in wb.findall('.//m:sheets/m:sheet',NS)]
        if names!=REQUIRED:issues.append(f'Tên/số trang tính không đúng: {names}')
        for f in z.namelist():
            if not re.fullmatch(r'xl/worksheets/sheet\d+\.xml',f):continue
            root=ET.fromstring(z.read(f))
            ff=root.findall('.//m:f',NS)
            formula_count+=len(ff)
            for c in root.findall('.//m:c',NS):
                value=c.find('m:v',NS)
                if c.attrib.get('t')=='e' and value is not None:errors.append((f,c.attrib.get('r'),value.text))
            for v in ff:
                if '#REF!' in (v.text or ''):issues.append(f'Lỗi tham chiếu công thức trong {f}')
    if errors:issues.append(f'Ô lỗi công thức: {errors[:8]}')
    if formula_count<100:issues.append(f'Có quá ít công thức so với mẫu: {formula_count}')
    return {'tep':str(path),'trang_tinh':names,'so_cong_thuc':formula_count,'loi':issues,'hop_le':not issues}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);a=ap.parse_args();o=inspect(a.input)
    print(json.dumps(o,ensure_ascii=False,indent=2));sys.exit(0 if o['hop_le'] else 2)
