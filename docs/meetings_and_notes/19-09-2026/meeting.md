# JWT

1. Có 2 biến : access_token và refresh_token
2. Luồng hoạt động:
   1. Sau khi đăng nhập thành công
   2. Tạo mới refresh_token, xóa refresh_token cũ nếu có
   3. Hash refresh_token
   4. Lưu refresh_token vào database
   5. Tạo mới access_token(ID người dùng + thời hạn sử dụng)) và gửi cho client(access_token và refresh_token) lưu tại local storage
   6. Sau đó mỗi lần thao tác tới server thì cần access_token để server xác nhận người dùng
   7. Nếu access_token bị hết hạn thì client gửi refresh_token cho server để server tạo mới access_token
   8. Nếu refresh_token bị hết hạn thì thường sẽ là đăng nhập lại, hoặc dùng cơ chế tạo mới refresh_token private
