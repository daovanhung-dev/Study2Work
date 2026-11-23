#!/usr/bin/env python3
"""Kiểm tra chất lượng đặc tả UTC JSON. Chỉ đọc, không thực thi app/API."""
import argparse,json,re,sys
from collections import Counter
from pathlib import Path

VAGUE=['đúng thiết kế','theo thiết kế','theo yêu cầu','hoạt động bình thường','hiển thị chính xác','xử lý đúng','như mong đợi']

def check(data):
    errors=[]; warnings=[]; info=[]
    def err(x):errors.append(x)
    def warn(x):warnings.append(x)
    m=data.get('metadata',{})
    for k in ['screen_id','screen_name','dd_status','source_name']:
        if not m.get(k):err(f'Thiếu metadata.{k}')
    reqs=data.get('requirements',[]);elements=data.get('elements',[]);events=data.get('events',[]);apis=data.get('apis',[])
    for n,arr in [('yêu cầu',reqs),('thành phần',elements),('sự kiện',events),('API',apis)]:
        ids=[x.get('id') for x in arr]
        if any(not i for i in ids):err(f'{n}: có đối tượng thiếu mã')
        for d,c in Counter(ids).items():
            if d and c>1:err(f'{n}: trùng mã {d}')
    reqids={x['id'] for x in reqs if x.get('id')};eleids={x['id'] for x in elements if x.get('id')};ev_ids={x['id'] for x in events if x.get('id')};apiids={x['id'] for x in apis if x.get('id')}
    for el in elements:
        for e in el.get('event_ids',[]):
            if e not in ev_ids:err(f'Thành phần {el.get("id")}: sự kiện không tồn tại {e}')
    for ev in events:
        for el in ev.get('element_ids',[]):
            if el not in eleids:err(f'Sự kiện {ev.get("id")}: thành phần không tồn tại {el}')
        for a in ev.get('api_ids',[]):
            if a not in apiids:err(f'Sự kiện {ev.get("id")}: API không tồn tại {a}')
    cases=data.get('test_cases',{});all_cases=[]
    if not all(cases.get(k) for k in ['screen','elements','events']):err('Cần đủ ca kiểm thử cho cả ba lớp: toàn màn hình, thành phần, sự kiện')
    for group,limit,objs in [('screen',150,{m.get('screen_id')}),('elements',200,eleids),('events',200,ev_ids)]:
        cs=cases.get(group,[])
        if len(cs)>limit:err(f'Nhóm {group} vượt số dòng mẫu {limit}')
        for tc in cs:
            id=tc.get('id','[không mã]');all_cases.append((group,tc))
            if not tc.get('id'):err(f'{group}: có ca không có mã')
            if not tc.get('target_id') or tc['target_id'] not in objs:err(f'{id}: target_id không thuộc danh mục {group}: {tc.get("target_id")}')
            rr=tc.get('requirement_ids',[])
            if not rr:err(f'{id}: chưa liên kết mã yêu cầu')
            for r in rr:
                if r not in reqids:err(f'{id}: yêu cầu không tồn tại {r}')
            for a in tc.get('api_ids',[]):
                if a not in apiids:err(f'{id}: mã API không tồn tại {a}')
            if not tc.get('source_refs'):err(f'{id}: thiếu nguồn DD')
            for f in ('title','precondition','data','steps','expected'):
                if not tc.get(f):err(f'{id}: thiếu {f}')
            if isinstance(tc.get('steps'),list) and not all(isinstance(s,str) and s.strip() for s in tc['steps']):err(f'{id}: bước kiểm thử rỗng')
            if tc.get('design_status') not in ('Đã xác nhận','Chờ xác nhận','Không áp dụng'):err(f'{id}: tình trạng DD không hợp lệ')
            if tc.get('priority') not in ('Cao','Trung bình','Thấp'):err(f'{id}: ưu tiên không hợp lệ')
            text=tc.get('expected','').strip().lower()
            if text in VAGUE or len(text)<18:warn(f'{id}: kết quả mong đợi chưa đủ kiểm chứng: {text}')
            if tc.get('design_status')=='Chờ xác nhận' and not any(w in tc.get('expected','').lower() for w in ['chờ xác nhận','chưa được duyệt','sau khi duyệt','cần xác nhận','không được']):warn(f'{id}: DD chờ xác nhận nhưng kỳ vọng có thể bị hiểu là đã chốt')
    case_ids=[tc.get('id') for _,tc in all_cases]
    for d,c in Counter(case_ids).items():
        if d and c>1:err(f'Trùng mã ca kiểm thử {d}')
    covered={r for _,tc in all_cases for r in tc.get('requirement_ids',[])}
    for r in sorted(reqids-covered):err(f'Yêu cầu chưa có ca kiểm thử: {r}')
    for el in sorted(eleids-{tc.get('target_id') for _,tc in all_cases if _=='elements'}):err(f'Thành phần chưa có ca kiểm thử: {el}')
    for ev in sorted(ev_ids-{tc.get('target_id') for _,tc in all_cases if _=='events'}):err(f'Sự kiện chưa có ca kiểm thử: {ev}')
    blocked=bool(data.get('blockers')) or any(tc.get('design_status')=='Chờ xác nhận' for _,tc in all_cases) or 'BLOCK' in m.get('dd_status','').upper()
    if blocked:warn('CÓ ĐIỀU KIỆN CHẶN PHÁT HÀNH: chỉ dùng như bộ UTC DỰ KIẾN; không tự phê duyệt ca chờ xác nhận DD.')
    info=[f'{len(reqs)} yêu cầu, {len(elements)} thành phần, {len(events)} sự kiện, {len(apis)} API',
          f'{len(cases.get("screen",[]))} ca toàn màn hình, {len(cases.get("elements",[]))} ca thành phần, {len(cases.get("events",[]))} ca sự kiện',
          f'Tổng ca: {len(all_cases)}; yêu cầu được truy vết: {len(reqids&covered)}/{len(reqids)}']
    return {'hop_le_ve_cau_truc':not errors,'du_dieu_kien_phe_duyet':not errors and not blocked,'thong_tin':info,'loi':errors,'canh_bao':warnings}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--report',type=Path)
    a=p.parse_args();o=check(json.loads(a.input.read_text(encoding='utf-8')))
    txt=json.dumps(o,ensure_ascii=False,indent=2)
    print(txt)
    if a.report: a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(txt,encoding='utf-8')
    sys.exit(0 if not o['loi'] else 2)
if __name__=='__main__':main()
