1. Chuẩn bị phần cứng: 1 cây máy tính 4gb, 256ssd, dây cáp mạng
2. Cấu hình mạng:
   1. Cấu hình tailscale : Nó là một cách truy cập server từ mạng khác lan khi chưa kết nối server với ip public
   2. Xin nhà mạng cấp địa chỉ ip public(nat, cgnat, port forward
   3. Truy cập admin router 192.168.1.1 cấu hình reverse static IP, Port Forward(Port = IP)
3. Cấu hình server: git, docker, ufw, nginx, apache(web).
