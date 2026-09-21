import 'package:study2work_mobile/shared/models/chat_message.dart';

abstract interface class ChatRepository {
  Future<List<ChatMessage>> getMessages({
    required int studentId,
    required int businessId,
  });

  Future<void> sendMessage({
    required int studentId,
    required int businessId,
    required String content,
  });
}
