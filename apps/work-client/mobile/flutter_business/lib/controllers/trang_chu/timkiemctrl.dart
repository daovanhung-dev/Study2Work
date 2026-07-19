import 'package:learn2earn/helper_db/helper_CV.dart';
import 'package:learn2earn/controllers/AI/ai_service.dart';
import 'package:learn2earn/models/CV.dart';
Future<void> TimKiem(String message) async {
  final AIService ai = AIService();
  String ChuyenNganh = 'Công nghệ thông tin, Kế Toán, ';
  String send = 'Tôi có CSDL như này (${ChuyenNganh}) mà doanh nghiệp tìm kiếm là (${message}), hãy đề xuất ngắn ngọn 1 chuyên ngành tìm trong CSDL tôi cung cấp, CẢNH BÁO(hãy nói luôn tên chuyên ngành và không nói gì thêm, nếu không phù hợp thì trả về null )';
  final String reply = await ai.sendMessage(send);
  print(reply);

}