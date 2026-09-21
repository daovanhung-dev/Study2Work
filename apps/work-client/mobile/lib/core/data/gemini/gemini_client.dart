import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:study2work_mobile/app/config/app_config.dart';

abstract interface class GeminiClient {
  Future<String> sendMessage(String message);
}

class AIService implements GeminiClient {
  final String apiKey = GEMINI_API_KEY;

  @override
  Future<String> sendMessage(String message) async {
    final url = Uri.parse(
      // Chuyển sang model mới
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=$apiKey',
    );

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        "contents": [
          {
            "parts": [
              {"text": message},
            ],
          },
        ],
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      if (data['candidates'] != null && data['candidates'].isNotEmpty) {
        return data['candidates'][0]['content']['parts'][0]['text'];
      } else {
        return "Không có nội dung trả về từ AI.";
      }
    } else {
      return "Đã xảy ra lỗi khi gọi Gemini API.";
    }
  }
}
