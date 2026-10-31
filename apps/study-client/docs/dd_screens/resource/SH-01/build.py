#!/usr/bin/env python3
"""Study2Work SH-01 editorial vector handoff. Run: python build.py"""
from pathlib import Path
import html, zipfile, re
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageChops
P=Path(__file__).resolve().parent
W,H=1440,1320
C=dict(bg='#F6FAFC',white='#FFFFFF',primary='#0B5F8A',hover='#084968',deep='#073B57',sky='#43A5C5',soft='#E8F4FA',text='#17324D',muted='#536A7A',border='#D4E2E9')
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', '<defs><filter id="shadow" x="-15%" y="-15%" width="130%" height="145%"><feDropShadow dx="0" dy="5" stdDeviation="12" flood-color="#073B57" flood-opacity=".045"/></filter></defs>']
E={}
def raw(x):s.append(x)
def rect(x,y,w,h,fill='white',stroke='none',r=0,sw=1,extra=''):raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def path(d,stroke='#0B5F8A',sw=2,fill='none',extra=''):raw(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def circle(x,y,r,fill,stroke='none',sw=1):raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(x,y,value,size=16,weight=400,color=C['text'],spacing=None):
 a=f' letter-spacing="{spacing}"' if spacing is not None else ''
 raw(f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}"{a}>{html.escape(value)}</text>')
def item(i,name,x,y,w,h,typ,visual,semantic,event,state,responsive,source):E[i]=dict(name=name,box=(x,y,w,h),typ=typ,visual=visual,semantic=semantic,event=event,state=state,responsive=responsive,source=source)
N='không có';NA='không áp dụng';static='STATIC_UI';sample='VISUAL_SAMPLE';
# page, top editorial rule, header
rect(0,0,W,H,C['bg']);rect(0,24,W,72,C['white']);path('M0 96H1440',C['border'],1)
# brand: folded-page mark, not lettermark
rect(160,43,34,34,C['primary'],r=9)
path('M170 52H181L186 57V69H170Z','white',1.6,'none');path('M181 52V57H186','white',1.6);path('M174 62H182 M174 66H180','white',1.2)
txt(207,68,'Study',24,700,C['deep'])
txt(656,67,'Trang chủ',15,600,C['primary']);rect(656,80,73,2,C['primary'],r=1)
txt(780,67,'Khóa học',15,600,C['text']);txt(1002,67,'Đăng nhập',15,600,C['text'])
rect(1139,36,141,48,C['primary'],r=10);txt(1176,66,'Đăng ký',15,600,C['white'])
# hero: copy x160 to ~760, illustration x800..1280
rect(160,143,4,17,C['sky'],r=2);txt(176,157,'HỌC ĐIỀU BẠN QUAN TÂM',13,600,C['primary'],.7)
txt(160,226,'Bắt đầu hành trình',48,700,C['deep']);txt(160,284,'học tập của bạn',48,700,C['deep'])
txt(160,334,'Khám phá các khóa học theo điều bạn quan tâm,',16,400,C['muted'])
txt(160,360,'và chọn một điểm khởi đầu phù hợp với mình.',16,400,C['muted'])
txt(160,408,'Tìm kiếm khóa học',14,600,C['text'])
rect(160,422,401,56,C['white'],C['border'],11);circle(185,449,7,'none',C['muted'],1.9);path('M190 454L196 460',C['muted'],1.9);txt(211,455,'Bạn muốn học điều gì?',15,400,C['muted'])
rect(573,422,185,56,C['primary'],r=11);txt(605,456,'Tìm khóa học',15,600,C['white'])
# Hero artwork: abstract desk / open course on laptop with editorial paper stack
# understated framing, geometry and linework
rect(802,135,478,347,C['soft'],r=26)
path('M827 175H861 M1220 450H1254',C['sky'],2)
circle(1223,179,33,'none','#B8D8E6',1.3);circle(1223,179,23,'none','#B8D8E6',1)
# paper behind screen
raw('<g transform="rotate(-11 1014 234)">')
rect(949,159,137,150,C['white'],'#C7DFE9',10)
rect(965,178,55,6,'#B9D9E8',r=3)
for yy,ww in [(196,100),(209,80),(222,94),(235,70)]:rect(965,yy,ww,4,'#D7E8EF',r=2)
rect(965,257,43,30,'#E8F4FA',r=5);path('M974 277L982 268L988 273L998 262','#43A5C5',2)
raw('</g>')
# laptop screen
rect(865,202,327,208,'#173D54',r=15)
rect(874,211,309,190,'#FFFFFF',r=9)
rect(874,211,309,29,'#F2F8FA',r=9)
circle(891,225,3,'#A5C9DA');circle(902,225,3,'#A5C9DA');circle(913,225,3,'#A5C9DA')
rect(891,257,72,127,'#E8F4FA',r=6)
for yy,ww in [(271,49),(289,58),(307,42),(325,54)]:rect(903,yy,ww,5,'#BBD7E5',r=2)
rect(982,258,118,9,'#0B5F8A',r=4)
rect(982,278,171,5,'#C3DAE5',r=2);rect(982,290,144,5,'#D4E2E9',r=2)
rect(982,310,173,74,'#F0F7FA',r=7)
# miniature learning diagram
circle(1014,348,16,'#C0DDEA');circle(1066,337,12,'#8FBFD3');circle(1124,354,18,'#D5E9F1')
path('M1030 345L1054 338 M1078 342L1106 351','#0B5F8A',2)
path('M844 411H1210L1192 425H863Z','#6F9FB5',1,'#C4DFEA');rect(951,413,147,4,'#8DB5C8',r=2)
# overlapping note card, clean editorial hierarchy
raw('<g transform="rotate(7 1160 349)">')
rect(1135,290,103,111,C['white'],'#C7DFE9',9,1,'filter="url(#shadow)"')
rect(1151,309,43,6,'#43A5C5',r=3);rect(1151,326,65,4,'#D4E2E9',r=2)
rect(1151,339,53,4,'#D4E2E9',r=2)
path('M1153 374L1169 356L1180 367L1198 348L1217 367','#0B5F8A',2)
raw('</g>')
# category region
path('M160 510H1280',C['border'],1)
txt(160,555,'Khám phá theo chủ đề',30,600,C['deep'])
txt(160,586,'Một vài chủ đề để tham khảo khi khám phá nội dung học.',14,400,C['muted'])
# Editorial taxonomy labels: noninteractive text and restrained vertical accent, no capsule/outline/hover.
rect(172,616,2,16,C['sky'],r=1);txt(184,631,'Lập trình',14,500,C['text'])
rect(307,616,2,16,C['sky'],r=1);txt(319,631,'Thiết kế',14,500,C['text'])
# course heading
txt(160,720,'Một số khóa học',30,600,C['deep'])
txt(1181,718,'Xem tất cả',15,600,C['primary']);path('M1181 724H1258',C['primary'],1)
# covers distinct artwork
cards=[(160,'Xây dựng ứng dụng Web','Tìm hiểu cách tạo giao diện và','kết nối các phần của website.','Nguyễn Minh Anh'),(541,'Thiết kế giao diện số','Làm quen với bố cục, màu sắc','và trải nghiệm người dùng.','Trần Hải Nam'),(922,'Nhập môn Python','Bắt đầu với tư duy lập trình','qua những bài tập thực tế.','Lê Thu Hà')]
for i,(x,title,desc1,desc2,mentor) in enumerate(cards):
 rect(x,753,357,369,C['white'],C['border'],15,1,'filter="url(#shadow)"')
 rect(x+16,769,325,169,['#E7F2F7','#EDF4F7','#E6F1F5'][i],r=10)
 if i==0:
  # code editor + browser preview
  rect(x+42,789,232,131,'#FFFFFF','#B8D5E3',9)
  rect(x+42,789,232,24,'#D5E8F0',r=9)
  for j in range(3):circle(x+56+j*12,801,3,'#7DAEC4')
  rect(x+56,825,53,82,'#E8F4FA',r=5)
  for yy in (836,849,862,875):rect(x+66,yy,31,4,'#B3D3E2',r=2)
  for yy,ww in [(827,90),(842,70),(857,106),(872,58),(887,83)]:rect(x+124,yy,ww,5,'#8BBBCF' if yy in (827,857) else '#D0E4EC',r=2)
  rect(x+240,835,73,64,'#0B5F8A',r=8)
  rect(x+251,848,51,6,'#8FC7DC',r=3);rect(x+251,862,38,5,'#D4E2E9',r=2);rect(x+251,874,46,5,'#D4E2E9',r=2)
 elif i==1:
  # graphic design composition grid / editorial layout
  rect(x+56,788,217,131,'#FFFFFF','#C3DCE7',8)
  rect(x+69,802,92,102,'#0B5F8A',r=4)
  circle(x+117,846,31,'#8EC3D8');path(f'M{x+83} 883L{x+111} 855L{x+131} 872L{x+150} 842', '#FFFFFF',2.5)
  rect(x+172,802,86,12,'#A6CBDC',r=3)
  for yy,ww in [(825,71),(839,82),(853,63),(874,77),(887,48)]:rect(x+172,yy,ww,5,'#D0E3EB',r=2)
  rect(x+237,817,77,75,'#F7FBFC','#BCD9E6',7)
  circle(x+275,851,20,'none','#43A5C5',2);path(f'M{x+258} 868L{x+291} 835','#0B5F8A',2)
 else:
  # data story: plotted series and minimal terminal
  rect(x+40,788,253,132,'#FFFFFF','#BEDAE7',9)
  rect(x+40,788,253,25,'#D5E8F0',r=9)
  for j in range(3):circle(x+54+j*12,801,3,'#7DAEC4')
  rect(x+56,827,95,76,'#E8F4FA',r=6)
  for yy,ww in [(839,66),(854,45),(869,72),(884,54)]:rect(x+66,yy,ww,5,'#8CBBD0' if yy in (839,869) else '#C6DFE9',r=2)
  path(f'M{x+174} 892L{x+195} 866L{x+216} 876L{x+240} 840L{x+271} 854','#0B5F8A',3)
  path(f'M{x+174} 897H{x+273}', '#C0DCE7',1)
  for dx,dy in [(195,866),(216,876),(240,840),(271,854)]:circle(x+dx,dy,4,'#43A5C5')
 # card text area
 txt(x+20,975,title,18,600,C['deep'])
 txt(x+20,1003,desc1,14,400,C['muted']);txt(x+20,1024,desc2,14,400,C['muted'])
 path(f'M{x+20} 1045H{x+337}',C['border'],1)
 circle(x+39,1082,19,'#E8F4FA',C['border'])
 circle(x+39,1076,6,'#7FAEC3');path(f'M{x+28} 1090Q{x+39} 1077 {x+50} 1090','#7FAEC3',2.4)
 txt(x+69,1088,mentor,14,500,C['text'])
# footer
path('M160 1177H1280',C['border'],1)
rect(160,1200,29,29,C['primary'],r=8);path('M169 1208H179L183 1212V1221H169Z','white',1.4);path('M179 1208V1212H183','white',1.4)
txt(202,1223,'Study',20,700,C['deep'])
txt(160,1260,'Một không gian để khám phá và bắt đầu học tập.',13,400,C['muted'])
txt(989,1227,'Khóa học',14,500,C['text']);txt(1091,1227,'Đăng nhập',14,500,C['text']);txt(1207,1227,'Đăng ký',14,500,C['text'])
# documentation metadata -- coordinates match visible geometry
T=lambda size,lh,weight,color:f'Inter {size}px/{lh}px/{weight} {color}'
R='desktop: giữ nguyên; tablet: co giãn; mobile: xếp theo luồng'
def add(i,name,b,typ,visual,semantic='static text',event=N,state=NA,responsive=R,source=static):item(i,name,*b,typ,visual,semantic,event,state,responsive,source)
link='hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968'
add(1,'Biểu tượng Study',(160,43,34,34),'N/A','fill #0B5F8A; white line icon; radius 9px; border none; left','brand link','đến `/`',link,'mobile: giữ cùng wordmark')
add(2,'Study wordmark',(207,45,77,29),T(24,29,700,C['deep']),'nền none; border none; left','brand link','đến `/`',link,'mobile: giữ')
add(3,'Trang chủ',(656,48,76,34),T(15,22,600,C['primary']),'underline #0B5F8A 2px; background none; border none','navigation link','đến `/`',link,'mobile: ẩn vì brand dẫn về `/`')
add(4,'Khóa học',(780,48,75,24),T(15,22,600,C['text']),'background none; border none','navigation link','đến `/courses` (GS-01)',link,'mobile: giữ trên cùng hàng compact')
add(5,'Đăng nhập',(1002,48,91,24),T(15,22,600,C['text']),'background none; border none','navigation link','đến `/login` (SH-02)',link,'mobile: giữ trên cùng hàng compact')
add(6,'Đăng ký',(1139,36,141,48),T(15,22,600,C['white']),'fill #0B5F8A; border none; radius 10px; centered','navigation link','đến `/register` (SH-03)',link,'mobile: giữ, compact target ≥44px')
add(7,'HỌC ĐIỀU BẠN QUAN TÂM',(176,139,295,18),T(13,18,600,C['primary']),'accent stripe x160 y143 4×17 #43A5C5; border none','static text',responsive='mobile: giữ; xuống dòng nếu cần')
add(8,'Bắt đầu hành trình / học tập của bạn',(160,174,580,116),T(48,58,700,C['deep']),'background none; border none; left','h1',responsive='tablet/mobile: reflow theo bề rộng, giữ 48/58 desktop')
add(9,'Hero supporting paragraph',(160,310,565,52),T(16,26,400,C['muted']),'background none; border none','paragraph',responsive='mobile: tự wrap theo 320px')
add(10,'Tìm kiếm khóa học',(160,388,188,20),T(14,20,600,C['text']),'background none; border none','visible input label',responsive='mobile: giữ trên input')
add(11,'Bạn muốn học điều gì?',(160,422,401,56),T(15,22,400,C['muted']),'fill white; border 1px #D4E2E9; radius 11px; left padding 51px','search textbox','typing lưu q; Enter submit', 'idle border #D4E2E9; focus 2px #0B5F8A offset 2px; typing cập nhật q; submitting chuyển route','mobile: full width')
add(12,'Biểu tượng kính lúp',(178,442,19,19),'N/A','outline #536A7A 1.9px; background none; border none','decorative icon',responsive='mobile: trong input')
add(13,'Tìm khóa học',(573,422,185,56),T(15,22,600,C['white']),'fill #0B5F8A; border none; radius 11px; centered','submit button','trim q; q khác rỗng → `/courses/search?q=${encodeURIComponent(q)}` (GS-02); rỗng → `/courses` (GS-01)',link,'mobile: full width dưới input')
add(14,'Editorial learning desk illustration',(802,135,478,347),'N/A','vector grouped: background #E8F4FA radius 26; laptop/paper; border none','decorative group',responsive='tablet: sau copy; mobile: ẩn')
add(15,'Khám phá theo chủ đề',(160,519,402,38),T(30,38,600,C['deep']),'background none; border none','h2')
add(16,'Một vài chủ đề để tham khảo khi khám phá nội dung học.',(160,566,560,20),T(14,20,400,C['muted']),'background none; border none','paragraph')
add(17,'Lập trình',(172,611,71,21),T(14,20,500,C['text']),'background transparent; border none; radius 0px; text left at x184 baseline y631; decorative accent x172 y616 2×16px #43A5C5','static label',event='không có',state='không áp dụng (không hover/focus/pressed)',responsive='tablet: inline, mobile: wrap; không pointer/hover',source='#05 GET /api/v1/categories; VISUAL_SAMPLE')
add(18,'Thiết kế',(307,611,66,21),T(14,20,500,C['text']),'background transparent; border none; radius 0px; text left at x319 baseline y631; decorative accent x307 y616 2×16px #43A5C5','static label',event='không có',state='không áp dụng (không hover/focus/pressed)',responsive='tablet: inline, mobile: wrap; không pointer/hover',source='#05 GET /api/v1/categories; VISUAL_SAMPLE')
add(19,'Một số khóa học',(160,684,340,38),T(30,38,600,C['deep']),'background none; border none','h2')
add(20,'Xem tất cả',(1181,697,78,28),T(15,22,600,C['primary']),'underline 1px #0B5F8A; background none; border none','navigation link','đến `/courses` (GS-01)',link,'mobile: giữ bên phải nếu đủ rộng; ngược lại xuống dòng')
for i,(x,title,d1,d2,mentor) in enumerate(cards):
 k=21+i*5
 add(k,f'Cover minh họa: {title}',(x+16,769,325,169),'N/A',f'vector editorial #{i+1}; nền {["#E7F2F7","#EDF4F7","#E6F1F5"][i]}; radius 10px; border none','decorative image',responsive='tablet: 2 cột; mobile: 1 cột',source='#06 GET /api/v1/courses; VISUAL_SAMPLE; thumbnail_url nullable')
 add(k+1,title,(x+20,952,317,26),T(18,26,600,C['deep']),'background white; border none; left','static course title',responsive='tablet: 2 cột; mobile: 1 cột',source='#06 title; VISUAL_SAMPLE')
 add(k+2,d1+' '+d2,(x+20,982,317,42),T(14,20,400,C['muted']),'background white; border none; left; two lines','static course description',responsive='mobile: wrap; null description → hide',source='#06 description nullable; VISUAL_SAMPLE')
 add(k+3,'Avatar mentor',(x+20,1063,38,38),'N/A','fill #E8F4FA; border 1px #D4E2E9; circular 38px; placeholder vector','decorative avatar',responsive='mobile: giữ 38px',source='#06 mentor.avatar_url nullable; VISUAL_SAMPLE')
 add(k+4,mentor,(x+69,1068,246,22),T(14,20,500,C['text']),'background white; border none; left','static mentor name',responsive='mobile: wrap nếu cần',source='#06 mentor.full_name; VISUAL_SAMPLE')
add(36,'Footer brand symbol',(160,1200,29,29),'N/A','fill #0B5F8A; white line icon; radius 8px; border none','brand link','đến `/`',link,'mobile: footer stack')
add(37,'Footer Study wordmark',(202,1203,67,25),T(20,25,700,C['deep']),'background none; border none','brand link','đến `/`',link,'mobile: footer stack')
add(38,'Một không gian để khám phá và bắt đầu học tập.',(160,1241,460,20),T(13,20,400,C['muted']),'background none; border none','static paragraph',responsive='mobile: wrap')
for k,name,x,w,route in [(39,'Khóa học',989,79,'/courses'),(40,'Đăng nhập',1091,94,'/login'),(41,'Đăng ký',1207,73,'/register')]:add(k,'Footer '+name,(x,1206,w,24),T(14,20,500,C['text']),'background none; border none','navigation link',f'đến `{route}`',link,'mobile: footer links wrap')
assert sorted(E)==list(range(1,42))
raw('</svg>')
svg='\n'.join(s)
(P/'SH-01_clean.svg').write_text(svg,encoding='utf-8')
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(P/'SH-01_clean.png'))
# Badges intentionally outside content; marker centers. Thin leader lines on card labels in card gutters.
pts=[(145, 48),(297, 59),(642, 57),(870, 57),(1107, 57),(1294, 49),(146, 149),(145, 207),(145, 344),(145, 398),(548, 439),(148, 449),(770, 435),(1267, 150),(145, 537),(145, 577),(147, 628),(392, 626),(145, 706),(1275, 708),
 (147, 785),(529, 964),(529, 1005),(147, 1080),(388, 1090),
 (529, 785),(910, 964),(910, 1005),(529, 1080),(769, 1090),
 (910, 785),(1293, 964),(1293, 1005),(910, 1080),(1150, 1090),
 (146, 1215),(284, 1215),(146, 1255),(977, 1245),(1090, 1245),(1264, 1245)]
assert len(pts)==41 and len(set(pts))==41
base=Image.open(P/'SH-01_clean.png').convert('RGBA');overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
fontpath='/usr/share/fonts/truetype/inter/Inter-Bold.otf'
if not Path(fontpath).exists():fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f=ImageFont.truetype(fontpath,12)
for i,(x,y) in enumerate(pts,1):
 # draw leaders only for cards, extending from gutter badges toward text right edges
 if i in (12,22,23,27,28,32,33):
  d.line((x+14,y,x+22,y),fill='#8BB6C8',width=1) if i==12 else d.line((x-14,y,x-22,y),fill='#8BB6C8',width=1)
 d.ellipse((x-12,y-12,x+12,y+12),fill=C['primary'],outline='white',width=2)
 box=d.textbbox((0,0),str(i),font=f)
 d.text((x-(box[2]-box[0])/2,y-(box[3]-box[1])/2-box[1]/2),str(i),font=f,fill='white')
Image.alpha_composite(base,overlay).convert('RGB').save(P/'SH-01_annotated.png')
# documentation generated from same canonical element geometry
md=['# SH-01 — Public Study landing/home','', '**Trạng thái:** `DESIGN_TARGET / NOT_IMPLEMENTED` · **Route:** `/` · **Actor:** Guest · **AC-03** · **W0**.','', '## Phạm vi và ranh giới bằng chứng','', 'Đây là bản bàn giao thiết kế, không phải màn hình đã triển khai. Study Web source/router chưa có trong checkout. Các tên chủ đề, khóa học và mentor trên hình đều là `VISUAL_SAMPLE` tĩnh, không phải dữ liệu trả về từ API. Không có screen con, modal, drawer hoặc search suggestion.','', '## Layout desktop và responsive','', '| Vùng | Hình học chính xác ở 1440×1320 | Tablet 768–1023 | Mobile 320–767 |','|---|---|---|---|','| Container | x=160–1280, max-width 1120; gutter 32 | gutter 24 | gutter 16 |','| Header | y=24–96, h=72, surface white, border-bottom 1px | một hàng, thu hẹp spacing | brand thay Trang chủ; Courses/login/register một hàng compact, không drawer; target ≥44 |','| Hero | copy x=160–758; art x=802 y=135 w=478 h=347; search y=422 | copy rồi art theo chiều dọc | ẩn art; search input rồi button full-width |','| Categories | separator y=510; heading y=519; nhãn taxonomy x=172/307, y=611–632; accent 2×16 tại x=172/307 | giữ 2 nhãn text, wrap khi cần | wrap nhãn tĩnh; không click/tap/focus |','| Courses | heading y=684; cards x=160/541/922, y=753, w=357 h=369, gap=24 | 2 cột | 1 cột; nội dung dài tự tăng chiều cao |','| Footer | separator y=1177; brand y=1200; links y=1206 | co giãn | xếp dọc, links wrap |','', '## Bản đồ 41 thành phần','', 'Tọa độ `x,y,w,h` là **pixel tuyệt đối** của bản SVG desktop cuối cùng. Font Inter được cài cục bộ; không dùng font mạng. `N/A` nghĩa là không có typography. Những nhóm art trong một thumbnail là một leaf duy nhất. Các course card và nhãn taxonomy đều **không tương tác**.','', '| # | Tên/nội dung | x,y,w,h (px) | Typography | Background / border / radius / alignment | Semantics | Event / target | Hover, focus, pressed | Responsive | Source |','|---|---|---|---|---|---|---|---|---|---|']
for k,v in sorted(E.items()):
 x,y,w,h=v['box']; values=[f'#{k}',v['name'],f'{x},{y},{w},{h}',v['typ'],v['visual'],v['semantic'],v['event'],v['state'],v['responsive'],v['source']]
 md.append('| '+' | '.join(str(z).replace('|','/') for z in values)+' |')
md += ['','## API boundary và orchestration','', '- **#05** `GET /api/v1/categories`: locale mặc định `vi-VN`, exact locale, chỉ category `ACTIVE`; fields `id`, `name`, `slug`, `description` nullable. Empty với HTTP 200 là success. Chỉ hiển thị metadata read-only, không lọc khóa học.','- **#06** `GET /api/v1/courses?page=1&size=3`: chỉ `PUBLISHED`; page=1; default size=20, range 1–100. Fields `id`, `title`, `description` nullable, `thumbnail_url` nullable, `price` decimal-string, `status`, `mentor.full_name`, `mentor.avatar_url` nullable. Chỉ render title, description, thumbnail, mentor; không render giá vì không biết currency/unit, không render status.','- **Không truyền `category` vào #06** vì API hiện trả 422. Không có course.category trong response. Không tạo giả rating, review, student count, popularity, testimonial, API/route/field khác.','- Fetch categories và courses độc lập; mỗi section có state và retry riêng. Không tự quy định cache TTL. Trace ID chỉ hiển thị khi backend thực sự trả.','', '## Search và điều hướng','', '- Input có label hiển thị “Tìm kiếm khóa học”, placeholder “Bạn muốn học điều gì?”. Enter và button cùng submit handler.','- `qTrimmed = q.trim()`. Nếu khác rỗng, điều hướng **GS-02** `/courses/search?q=${encodeURIComponent(qTrimmed)}` (encode đúng một lần). Nếu rỗng, điều hướng **GS-01** `/courses` và **không gửi q rỗng**. Không có autocomplete/suggestion.','- Header/footer brand và Trang chủ → `/`; Khóa học/Xem tất cả/footer Khóa học → GS-01 `/courses`; Đăng nhập → SH-02 `/login`; Đăng ký → SH-03 `/register`.','- Card khóa học không link. Course detail **GS-03** thuộc luồng GS-01, không được mở từ SH-01. Nhãn taxonomy #17/#18 là static labels, không filter, không event.','', '## States chi tiết','', '| Section | Loading | Ready | Empty | Error |','|---|---|---|---|---|','| Categories #05 | skeleton dạng dòng chữ nhỏ (không capsule), aria-busy, không tạo dữ liệu giả | hiện ACTIVE từ response | HTTP 200 empty: “Chưa có chủ đề để hiển thị.” | thông báo lỗi riêng, “Thử lại” gọi lại đúng GET #05 |','| Courses #06 | 3 skeleton card ổn định, aria-busy, không tạo data giả | render tối đa 3 course từ page=1,size=3 | “Hiện chưa có khóa học để giới thiệu.” | thông báo lỗi riêng, “Thử lại” gọi lại đúng GET #06 |','| Nullable | N/A | thumbnail/avatar null dùng placeholder kín đáo; description null ẩn và reflow | N/A | không gán URL giả |','| Search | idle: placeholder | focus: outline 2px; typing: cập nhật local q | submit blank → GS-01 | submitting: điều hướng, không giả endpoint tìm kiếm |','', 'Các thông báo trạng thái chỉ là **state specification**, không phải thành phần hiển thị thêm trên main mockup và không nằm trong marker map.','', '## Accessibility / visual tokens','', '- Font: Inter local, fallback system sans. H1 **48/58/700** đúng guide; body **16/26/400**; section **30/38/600**; card title **18/26/600**; description **14/20/400**; mentor **14/20/500**; nav **15/22/600**; eyebrow **13/18/600**.','- Tokens: page `#F6FAFC`, surface `#FFFFFF`, primary `#0B5F8A`, hover/pressed `#084968`, deep `#073B57`, sky `#43A5C5` chỉ decorative, soft `#E8F4FA`, text `#17324D`, muted `#536A7A`, border `#D4E2E9`.','- Focus visible 2px `#0B5F8A` offset 2px; min interactive hit area 44×44; search controls 56px; button header 48px. Tương phản chữ chính được chọn theo WCAG AA; kiểm thử lại trong browser ở breakpoint thật.','- Tab order: brand → Trang chủ → Khóa học → Đăng nhập → Đăng ký → textbox → submit → Xem tất cả → footer brand → footer Khóa học → footer Đăng nhập → footer Đăng ký. Art, nhãn taxonomy, card và avatar không focus.','- Hover 140ms chỉ đổi màu/underline, không layout shift. `prefers-reduced-motion: reduce` tắt transition không thiết yếu. Decorative art `aria-hidden`; card cover minh họa không đọc như thông tin mới.','', '## Discrepancy và giới hạn','', '- Không có mismatch đã biết giữa bản render desktop và các type target chính của guide. Đây là thiết kế target, không xác nhận frontend/backend đã tích hợp.','- Chỉ desktop 1440×1320 được render; tablet/mobile là quy tắc triển khai cần QA tại 320px. Sample course/mentor/category không chứng minh dữ liệu production.','', '## Checklist nghiệm thu','', '- [x] Hai PNG 1440×1320 xuất từ cùng một SVG, clean khác annotated chỉ ở lớp marker.','- [x] 41 marker duy nhất, 24×24, primary fill, trắng 12px bold, viền trắng.','- [x] H1 48/58; course description 14/20; 3 artwork vector khác nhau; hero art học tập mới.','- [x] Không giá/rating/status/số học viên/category trên card; không card link/category filter.','- [x] API #05/#06, điều hướng, nullable, independent state, retry, accessibility và breakpoint đã đặc tả.','- [ ] QA thực tế tại tablet/mobile khi code ứng dụng.']
(P/'SCREEN.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
with zipfile.ZipFile(P.parent/'SH-01_design_handoff_v5.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in ('SH-01_annotated.png','SH-01_clean.png','SCREEN.md','SH-01_clean.svg','build.py'):z.write(P/n,n)
print('DONE',len(E),'elements, zip bytes',(P.parent/'SH-01_design_handoff_v5.zip').stat().st_size)
