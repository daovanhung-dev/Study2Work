#!/usr/bin/env python3
"""Sinh UTC Screen 4 trang tính từ đặc tả JSON. Không tự suy diễn DD.
Yêu cầu: artifact_tool. Python >=3.10.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from artifact_tool import Workbook, SpreadsheetFile
except ImportError as exc:
    raise SystemExit('Thiếu artifact_tool. Chạy trong môi trường có artifact_tool.') from exc

TABS = ['01. Bìa','02. Tổng quan','03. Thành phần','04. Sự kiện']
COLS = ['Mã ca kiểm thử','Mã yêu cầu','Mã đối tượng','Nhóm kiểm thử','Mục tiêu kiểm thử',
        'Điều kiện tiên quyết','Dữ liệu kiểm thử','Các bước thực hiện','Kết quả mong đợi',
        'API liên quan','Nguồn DD','Mức ưu tiên','Tình trạng DD','Trạng thái thực thi',
        'Kết quả thực tế','Bằng chứng','Mã lỗi','Người kiểm thử','Ngày kiểm thử','Kiểm tra hồ sơ']
CASES = {'screen':(TABS[1],117,266),'elements':(TABS[2],71,270),'events':(TABS[3],71,270)}
BLUE='#183A63'; DEEP='#112A47'; CYAN='#0B6E88'; LIGHT='#E8F3F6'; BG='#F5F8FC'; WHITE='#FFFFFF'; LINE='#D6E1ED'; MUTED='#52647A'; GOLD='#FFF5DD'; DARK='#1C304A'

def cell(s,a,v):
    s.get_range(a).values=[[v]]
def formula(s,a,v):
    s.get_range(a).formulas=[[v]]
def merge(s,rng,txt=None):
    s.merge_cells(rng)
    if txt is not None: cell(s,rng.split(':')[0],txt)
def band(s,rng,color=BLUE):
    title=None
    if not color.startswith('#'):
        title=color
        color=BLUE
    if title is not None:
        s.merge_cells(rng)
        cell(s,rng.split(':')[0],title)
    r=s.get_range(rng);r.format.fill=color;r.format.font.color=WHITE;r.format.font.bold=True;r.format.row_height=25

def basic_sheet(s,maxcol='T'):
    s.get_range(f'A1:{maxcol}3').format.fill=DEEP
    s.get_range(f'A1:{maxcol}3').format.font.color=WHITE
    s.get_range(f'A1:{maxcol}3').format.row_height=26
    s.get_range(f'A1:{maxcol}1').format.font.bold=True
    s.get_range(f'A1:{maxcol}1').format.font.size=17
    s.get_range('A:A').format.column_width=18
    s.get_range('B:B').format.column_width=25
    s.get_range('C:C').format.column_width=23
    s.get_range('D:D').format.column_width=23
    s.get_range('E:E').format.column_width=26
    s.get_range('F:F').format.column_width=28
    s.get_range('G:G').format.column_width=27
    s.get_range('H:H').format.column_width=32
    s.get_range('I:I').format.column_width=34
    s.get_range('J:J').format.column_width=24
    s.get_range('K:K').format.column_width=30
    s.get_range('L:L').format.column_width=16
    s.get_range('M:M').format.column_width=18
    s.get_range('N:N').format.column_width=19
    s.get_range('O:O').format.column_width=26
    s.get_range('P:P').format.column_width=28
    s.get_range('Q:Q').format.column_width=16
    s.get_range('R:R').format.column_width=19
    s.get_range('S:S').format.column_width=18
    s.get_range('T:T').format.column_width=22

def header(s,row,cols):
    s.get_range_by_indexes(row-1,0,1,len(cols)).values=[cols]
    band(s,f'A{row}:{chr(64+len(cols))}{row}',CYAN)
    s.get_range(f'A{row}:{chr(64+len(cols))}{row}').format.wrap_text=True
    s.get_range(f'A{row}:{chr(64+len(cols))}{row}').format.row_height=36

def case_table(s,row,end,items):
    header(s,row-1,COLS)
    h=end-row+1
    # Data region prepared as input-ready, no fake test cases.
    s.get_range(f'A{row}:T{end}').format.row_height=46
    s.get_range(f'A{row}:T{end}').format.wrap_text=True
    s.get_range(f'A{row}:T{end}').format.vertical_alignment='top'
    s.get_range(f'A{row}:S{end}').format.fill=WHITE
    s.get_range(f'T{row}:T{end}').format.fill=LIGHT
    s.get_range(f'L{row}:L{end}').data_validation={'rule':{'type':'list','values':['Cao','Trung bình','Thấp']}}
    s.get_range(f'M{row}:M{end}').data_validation={'rule':{'type':'list','values':['Đã xác nhận','Chờ xác nhận','Không áp dụng']}}
    s.get_range(f'N{row}:N{end}').data_validation={'rule':{'type':'list','values':['Chưa chạy','Đạt','Không đạt','Bị chặn','Không áp dụng']}}
    s.get_range(f'T{row}').formulas=[[f'=IF(A{row}="","",IF(OR(B{row}="",C{row}="",E{row}="",F{row}="",H{row}="",I{row}="",K{row}=""),"Thiếu thông tin",IF(M{row}="Chờ xác nhận","Chờ xác nhận DD",IF(AND(N{row}<>"Chưa chạy",N{row}<>"Không áp dụng",OR(O{row}="",P{row}="",R{row}="",S{row}="")),"Thiếu bằng chứng","Hợp lệ"))))']]
    if h>1: s.get_range(f'T{row}:T{end}').fill_down()
    s.get_range(f'T{row}:T{end}').conditional_formats.add_custom(f'=T{row}="Thiếu thông tin"',{'fill':'#FFEBE9'})
    s.get_range(f'T{row}:T{end}').conditional_formats.add_custom(f'=T{row}="Chờ xác nhận DD"',{'fill':GOLD})
    s.get_range(f'T{row}:T{end}').conditional_formats.add_custom(f'=T{row}="Hợp lệ"',{'fill':'#E7F6ED'})
    if len(items)>h: raise ValueError(f'Có {len(items)} ca, vượt dung lượng {h} của {s.name}')
    if items:
        values=[]
        for t in items:
            steps=t.get('steps',[])
            if isinstance(steps,list): steps='\n'.join(f'{i+1}. {x}' for i,x in enumerate(steps))
            values.append([
                t.get('id',''),'; '.join(t.get('requirement_ids',[])),t.get('target_id',''),t.get('group',''),
                t.get('title',''),t.get('precondition',''),t.get('data',''),steps,('API '+t.get('expected','') if t.get('expected','').startswith('#') else t.get('expected','')),
                '; '.join(t.get('api_ids',[])),'; '.join(t.get('source_refs',[])),t.get('priority','Trung bình'),
                t.get('design_status','Chờ xác nhận'),'Chưa chạy','','','','','',''
            ])
        s.get_range_by_indexes(row-1,0,len(values),20).values=values
        # Restore formula cells after payload write.
        s.get_range(f'T{row}').formulas=[[f'=IF(A{row}="","",IF(OR(B{row}="",C{row}="",E{row}="",F{row}="",H{row}="",I{row}="",K{row}=""),"Thiếu thông tin",IF(M{row}="Chờ xác nhận","Chờ xác nhận DD",IF(AND(N{row}<>"Chưa chạy",N{row}<>"Không áp dụng",OR(O{row}="",P{row}="",R{row}="",S{row}="")),"Thiếu bằng chứng","Hợp lệ"))))']]
        if h>1: s.get_range(f'T{row}:T{end}').fill_down()

def overview(s,spec):
    m=spec.get('metadata',{});o=spec.get('overall',{}); apis=spec.get('apis',[]);reqs=spec.get('requirements',[])
    basic_sheet(s); merge(s,'A1:T1','02  /  TỔNG QUAN MÀN HÌNH VÀ KIỂM THỬ TOÀN MÀN HÌNH')
    merge(s,'A2:T2','Đặc tả tổng thể • Danh mục API • Yêu cầu truy vết • Ca kiểm thử toàn màn hình')
    band(s,'A5:T5','Thông tin thiết kế và phạm vi')
    fields=[('Mã màn hình',m.get('screen_id','')),('Tên màn hình',m.get('screen_name','')),('Tuyến truy cập',m.get('route','')),('Tác nhân / quyền',m.get('actor','')),
            ('Mục tiêu',o.get('objective','')),('Đầu vào',o.get('inputs','')),('Đầu ra',o.get('outputs','')),('Luồng chính',o.get('main_flow','')),
            ('Trạng thái giao diện',', '.join(o.get('states',[]))),('Tiền điều kiện',o.get('preconditions','')),('Quy tắc bảo mật',o.get('security','')),
            ('Ngoài phạm vi',o.get('out_of_scope','')),('Nguồn DD',m.get('source_name',''))]
    for rr,(label,val) in enumerate(fields,6):
        cell(s,f'A{rr}',label); merge(s,f'B{rr}:T{rr}',val)
        s.get_range(f'A{rr}').format.fill=LIGHT
        s.get_range(f'A{rr}').format.font.bold=True
        s.get_range(f'B{rr}:T{rr}').format.wrap_text=True
        s.get_range(f'A{rr}:T{rr}').format.row_height=36 if len(str(val))>120 else 27
    band(s,'A22:T22','Danh mục API dùng bởi màn hình (không tự bổ sung API ngoài DD)')
    api_cols=['Mã API','Phương thức','Đường dẫn','Sự kiện gọi','Tham số đầu vào','Dữ liệu đầu ra','Lỗi/ngoại lệ','Xác thực','Tình trạng DD','Nguồn DD']
    header(s,23,api_cols)
    s.get_range('A24:J40').format.row_height=43; s.get_range('A24:J40').format.wrap_text=True
    if len(apis)>17: raise ValueError('Vượt 17 API trong mẫu; cần mở rộng vùng API bằng code')
    if apis:
        r=[]
        for a in apis:
            r.append([a.get('id',''),a.get('method',''),a.get('path',''),'; '.join(a.get('event_ids',[])),
                    a.get('request',''),a.get('response',''),a.get('errors',''),a.get('auth',''),a.get('design_status',''),a.get('source_ref','')])
        s.get_range_by_indexes(23,0,len(r),10).values=r
    band(s,'A42:T42','Ma trận yêu cầu và độ bao phủ (nguồn duy nhất để liên kết mã yêu cầu)')
    header(s,43,['Mã yêu cầu','Nội dung yêu cầu','Nhóm','Trạng thái DD','Nguồn DD','Ghi chú / điều kiện','Ưu tiên','Bao phủ TC'])
    s.get_range('A44:H103').format.row_height=34;s.get_range('A44:H103').format.wrap_text=True
    s.get_range('H44:H103').format.fill=LIGHT
    fr='=IF(A44="","",IF(COUNTIF($V$3:$V$1600,A44)>0,"Có ca kiểm thử","Chưa có ca kiểm thử"))'
    s.get_range('H44').formulas=[[fr]];s.get_range('H44:H103').fill_down()
    if len(reqs)>60: raise ValueError('Vượt 60 yêu cầu trong mẫu; cần mở rộng template')
    if reqs:
        vals=[[r.get('id',''),r.get('description',''),r.get('group',''),r.get('design_status',''),r.get('source_ref',''),r.get('notes',''),r.get('priority',''),None] for r in reqs]
        s.get_range_by_indexes(43,0,len(vals),8).values=vals
        s.get_range('H44').formulas=[[fr]];s.get_range('H44:H103').fill_down()
    band(s,'A105:T105','Vấn đề chờ xác nhận / điều kiện chặn phát hành')
    header(s,106,['Mã vấn đề','Mô tả','Ảnh hưởng','Quyết định cần có','Nguồn DD','Trạng thái'])
    s.get_range('A107:F114').format.row_height=43;s.get_range('A107:F114').format.wrap_text=True
    blockers=spec.get('blockers',[])
    if len(blockers)>8: raise ValueError('Vượt 8 vấn đề; cần mở rộng mục blocker')
    if blockers:
        vals=[[b.get('id',''),b.get('description',''),b.get('impact',''),b.get('decision',''),b.get('source_ref',''),b.get('status','Chưa giải quyết')] for b in blockers]
        s.get_range_by_indexes(106,0,len(vals),6).values=vals
    band(s,'A115:T115','CA KIỂM THỬ ĐẶC TÍNH CHUNG TOÀN MÀN HÌNH')
    merge(s,'A116:T116','Các ca kiểm thử luồng khởi tạo, trạng thái tổng thể, dữ liệu, lỗi, điều hướng, bảo mật và khả năng tiếp cận')
    case_table(s,117,266,spec.get('test_cases',{}).get('screen',[]))
    # Bảng truy vết máy đọc, nằm sau cột T; Excel tính độ bao phủ bằng COUNTIF chính xác,
    # tránh phụ thuộc vào cách engine xử lý ký tự * và ô chứa nhiều mã.
    s.get_range('V1:W1').values=[['PHỤ TRỢ — MÃ YÊU CẦU','MÃ CA KIỂM THỬ (chỉ sửa JSON rồi sinh lại)']]
    s.get_range('V1:W1').format.fill=CYAN
    s.get_range('V1:W1').format.font.color=WHITE
    s.get_range('V:V').format.column_width=26
    s.get_range('W:W').format.column_width=42
    links=[]
    for gr in ('screen','elements','events'):
        for tc in spec.get('test_cases',{}).get(gr,[]):
            links.extend([[rid,tc.get('id','')] for rid in tc.get('requirement_ids',[])])
    if len(links)>1598: raise ValueError('Quá 1598 quan hệ yêu cầu–ca; cần mở rộng bảng phụ trợ')
    if links: s.get_range_by_indexes(2,21,len(links),2).values=links
    s.freeze_panes.freeze_rows(3)

def object_sheet(s,items,cases,what):
    basic_sheet(s)
    if what=='elements':
        merge(s,'A1:T1','03  /  THÀNH PHẦN MÀN HÌNH')
        merge(s,'A2:T2','Danh mục từng thành phần • Kiểm thử hiển thị / dữ liệu / trạng thái / UI–UX / khả năng tiếp cận')
        cols=['Mã thành phần','Marker','Tên / nhãn','Loại','Vị trí','Đặc tính / dữ liệu','Sự kiện liên quan','Tình trạng DD','Nguồn DD']
        tc_name='CA KIỂM THỬ CHO TỪNG THÀNH PHẦN'
    else:
        merge(s,'A1:T1','04  /  SỰ KIỆN MÀN HÌNH')
        merge(s,'A2:T2','Danh mục sự kiện • Thao tác / xử lý logic / API / trạng thái / điều hướng / ngoại lệ')
        cols=['Mã sự kiện','Tên sự kiện','Kích hoạt','Thành phần liên quan','API liên quan','Xử lý / đầu ra','Trạng thái DD','Nguồn DD']
        tc_name='CA KIỂM THỬ CHO TỪNG SỰ KIỆN'
    band(s,'A7:T7','Danh mục đối tượng theo tài liệu thiết kế')
    header(s,9,cols)
    s.get_range('A10:I59').format.row_height=38;s.get_range('A10:I59').format.wrap_text=True
    if len(items)>50: raise ValueError('Vượt 50 thành phần/sự kiện trong mẫu; cần mở rộng')
    if items:
        rows=[]
        for it in items:
            if what=='elements':
                rows.append([it.get('id',''),it.get('marker',''),it.get('name',''),it.get('type',''),it.get('position',''),it.get('properties',''),'; '.join(it.get('event_ids',[])),it.get('design_status',''),it.get('source_ref','')])
            else:
                rows.append([it.get('id',''),it.get('name',''),it.get('trigger',''),'; '.join(it.get('element_ids',[])), '; '.join(it.get('api_ids',[])),it.get('processing',''),it.get('design_status',''),it.get('source_ref','')])
        s.get_range_by_indexes(9,0,len(rows),len(cols)).values=rows
    band(s,'A65:T65',tc_name)
    merge(s,'A66:T66','Mỗi ca phải có dữ liệu cụ thể, bước lặp lại được, kỳ vọng kiểm chứng được và nguồn DD tương ứng.')
    merge(s,'A67:T67','Nếu DD chưa chốt: đánh dấu “Chờ xác nhận”; không tự điền quyết định nghiệp vụ; không đánh dấu “Đạt”.')
    case_table(s,71,270,cases)
    s.freeze_panes.freeze_rows(9)

def cover(s,spec):
    m=spec.get('metadata',{})
    s.get_range('A:A').format.column_width=22
    for col in 'BCDEFGHIJKLMN': s.get_range(f'{col}:{col}').format.column_width=17
    merge(s,'A1:N3','BỘ BIỂU MẪU KIỂM THỬ MÀN HÌNH — UTC')
    s.get_range('A1:N3').format.fill=DEEP;s.get_range('A1:N3').format.font.color=WHITE;s.get_range('A1:N3').format.font.bold=True;s.get_range('A1:N3').format.font.size=19;s.get_range('A1:N3').format.row_height=28
    merge(s,'A4:N4','TÀI LIỆU KIỂM THỬ THEO ĐẶC TẢ DD • PHẠM VI: TOÀN MÀN HÌNH / THÀNH PHẦN / SỰ KIỆN')
    s.get_range('A4:N4').format.fill=CYAN;s.get_range('A4:N4').format.font.color=WHITE;s.get_range('A4:N4').format.row_height=27
    band(s,'A6:N6','I. THÔNG TIN PHÁT HÀNH')
    ls=[('Mã màn hình',m.get('screen_id','')),('Tên màn hình',m.get('screen_name','')),('Dự án / phân hệ',m.get('module','')),('Tuyến màn hình',m.get('route','')),('Phiên bản tài liệu',m.get('version','1.0')),('Phiên bản DD',m.get('dd_version','')),('Trạng thái DD',m.get('dd_status','')),('Trạng thái runtime',m.get('runtime_status','')),
        ('Người lập',m.get('author','')),('Người rà soát',m.get('reviewer','')),('Người phê duyệt',m.get('approver','')),('Ngày phát hành',m.get('date',''))]
    for i,(label,value) in enumerate(ls,7):
        merge(s,f'A{i}:C{i}',label);merge(s,f'D{i}:N{i}',value)
        s.get_range(f'A{i}:C{i}').format.fill=LIGHT;s.get_range(f'A{i}:C{i}').format.font.bold=True
        s.get_range(f'D{i}:N{i}').format.fill=BG
        s.get_range(f'A{i}:N{i}').format.row_height=27
    band(s,'A21:N21','II. THỐNG KÊ TỰ ĐỘNG — CHỈ TÍNH CA CÓ MÃ')
    pairs=[('Số ca toàn màn hình',"=COUNTA('02. Tổng quan'!A117:A266)"),
           ('Số ca thành phần',"=COUNTA('03. Thành phần'!A71:A270)"),
           ('Số ca sự kiện',"=COUNTA('04. Sự kiện'!A71:A270)"),
           ('Tổng số ca', '=D22+D23+D24'),
           ('Ca đã thực thi',"=COUNTIF('02. Tổng quan'!N117:N266,\"Đạt\")+COUNTIF('02. Tổng quan'!N117:N266,\"Không đạt\")+COUNTIF('02. Tổng quan'!N117:N266,\"Bị chặn\")+COUNTIF('03. Thành phần'!N71:N270,\"Đạt\")+COUNTIF('03. Thành phần'!N71:N270,\"Không đạt\")+COUNTIF('03. Thành phần'!N71:N270,\"Bị chặn\")+COUNTIF('04. Sự kiện'!N71:N270,\"Đạt\")+COUNTIF('04. Sự kiện'!N71:N270,\"Không đạt\")+COUNTIF('04. Sự kiện'!N71:N270,\"Bị chặn\")"),
           ('Ca đạt',"=COUNTIF('02. Tổng quan'!N117:N266,\"Đạt\")+COUNTIF('03. Thành phần'!N71:N270,\"Đạt\")+COUNTIF('04. Sự kiện'!N71:N270,\"Đạt\")"),
           ('Ca không đạt',"=COUNTIF('02. Tổng quan'!N117:N266,\"Không đạt\")+COUNTIF('03. Thành phần'!N71:N270,\"Không đạt\")+COUNTIF('04. Sự kiện'!N71:N270,\"Không đạt\")"),
           ('Ca bị chặn',"=COUNTIF('02. Tổng quan'!N117:N266,\"Bị chặn\")+COUNTIF('03. Thành phần'!N71:N270,\"Bị chặn\")+COUNTIF('04. Sự kiện'!N71:N270,\"Bị chặn\")"),
           ('Tỷ lệ thực thi','=IFERROR(D26/D25,0)'),('Tỷ lệ đạt trên số đã chạy','=IFERROR(D27/D26,0)'),
           ('Yêu cầu có ca kiểm thử',"=COUNTIF('02. Tổng quan'!H44:H103,\"Có ca kiểm thử\")"),
           ('Yêu cầu chưa có ca kiểm thử',"=COUNTIF('02. Tổng quan'!H44:H103,\"Chưa có ca kiểm thử\")")]
    for i,(name,f) in enumerate(pairs,22):
        merge(s,f'A{i}:C{i}',name);merge(s,f'D{i}:F{i}');formula(s,f'D{i}',f)
        s.get_range(f'A{i}:C{i}').format.fill=LIGHT;s.get_range(f'A{i}:C{i}').format.font.bold=True
        s.get_range(f'D{i}:F{i}').format.fill=BG;s.get_range(f'D{i}:F{i}').format.font.bold=True
        s.get_range(f'A{i}:N{i}').format.row_height=27
    for i in (30,31):s.get_range(f'D{i}').set_number_format('0.0%')
    band(s,'A36:N36','III. ĐIỀU KIỆN PHÁT HÀNH VÀ QUY TẮC SỬ DỤNG')
    rules=[
    '01. Chỉ viết kỳ vọng xuất phát từ DD / API contract / quyết định được duyệt; không coi ảnh tĩnh là runtime.',
    '02. Bắt buộc bao phủ ba lớp: toàn màn hình, từng thành phần, từng sự kiện.',
    '03. Các mục DD chưa phê duyệt phải ghi “Chờ xác nhận”; ca này không được phê duyệt để chạy.',
    '04. Ghi nguồn DD tới file + mục; mã yêu cầu và đối tượng phải tồn tại trong danh mục.',
    '05. Trạng thái “Đạt” chỉ được chọn sau khi chạy thật và có kết quả, bằng chứng, người/ngày chạy.',
    '06. Nếu DD còn BLOCKED, chỉ phát hành bản KẾ HOẠCH UTC; chưa gắn nhãn SẴN SÀNG KIỂM THỬ.',
    '07. Mẫu KHÔNG xác nhận việc tuân thủ ISO/ISTQB/WCAG; chỉ áp dụng phương pháp và tiêu chí tham chiếu.'
    ]
    for i,x in enumerate(rules,37):merge(s,f'A{i}:N{i}',x);s.get_range(f'A{i}:N{i}').format.row_height=28
    band(s,'A46:N46','IV. NGUỒN PHƯƠNG PHÁP / TÀI LIỆU QUỐC TẾ')
    for i,x in enumerate([
        'ISTQB CTFL v4.0.1 — https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf',
        'ISO/IEC/IEEE 29119-3:2021 — https://www.iso.org/standard/79429.html',
        'WCAG 2.2 (W3C) — https://www.w3.org/TR/WCAG22/',
        'OWASP WSTG — https://owasp.org/www-project-web-security-testing-guide/'
    ],47):merge(s,f'A{i}:N{i}',x);s.get_range(f'A{i}:N{i}').format.row_height=25
    s.freeze_panes.freeze_rows(4)

def main():
    p=argparse.ArgumentParser(description='Sinh UTC Screen Excel từ JSON (hoặc tạo mẫu trống)')
    p.add_argument('--input',type=Path,help='Đặc tả UTC dạng JSON có nguồn DD')
    p.add_argument('--output',type=Path,required=True,help='Đường dẫn Excel đầu ra')
    p.add_argument('--mau',action='store_true',help='Tạo mẫu rỗng; không nhập dữ liệu giả định')
    p.add_argument('--preview',type=Path,help='Tùy chọn xuất PNG bìa kiểm tra')
    args=p.parse_args()
    if not args.mau and not args.input: p.error('Cần --input hoặc --mau')
    spec=json.loads(args.input.read_text(encoding='utf-8')) if args.input else {}
    wb=Workbook.create()
    sheets={name:wb.worksheets.add(name) for name in TABS}
    cover(sheets[TABS[0]],spec)
    overview(sheets[TABS[1]],spec)
    object_sheet(sheets[TABS[2]],spec.get('elements',[]),spec.get('test_cases',{}).get('elements',[]),'elements')
    object_sheet(sheets[TABS[3]],spec.get('events',[]),spec.get('test_cases',{}).get('events',[]),'events')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(args.output))
    if args.preview:
        try: wb.render({'sheet_name':TABS[0],'range':'A1:N34','scale':1.35}).save(str(args.preview))
        except Exception as e: print('Cảnh báo: Không xuất được ảnh xem trước:',e,file=sys.stderr)
    print(json.dumps({'tep':str(args.output),'trang_tinh':TABS,'ca_toan_man_hinh':len(spec.get('test_cases',{}).get('screen',[])),'ca_thanh_phan':len(spec.get('test_cases',{}).get('elements',[])),'ca_su_kien':len(spec.get('test_cases',{}).get('events',[]))},ensure_ascii=False))

if __name__=='__main__':main()
