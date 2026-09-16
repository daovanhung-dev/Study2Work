import 'package:work_server/controllers/AI/ai_service.dart';

Future<void> timKiem(String message) async {
  final AIService ai = AIService();
  String chuyenNganh = 'Công nghệ thông tin, Kế Toán, ';
  String send =
      'Tôi có CSDL như này ($chuyenNganh) mà doanh nghiệp tìm kiếm là ($message), hãy đề xuất ngắn ngọn 1 chuyên ngành tìm trong CSDL tôi cung cấp, CẢNH BÁO(hãy nói luôn tên chuyên ngành và không nói gì thêm, nếu không phù hợp thì trả về null )';
  await ai.sendMessage(send);
}
