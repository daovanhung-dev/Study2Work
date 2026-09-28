import 'package:study2work_mobile/features/business/legacy/controllers/chat/chat_controller.dart'
    as legacy_chat;
import 'package:study2work_mobile/features/chat/domain/chat_repository.dart';
import 'package:study2work_mobile/shared/models/chat_message.dart';

final class BusinessChatRepository implements ChatRepository {
  @override
  Future<List<ChatMessage>> getMessages({
    required int studentId,
    required int businessId,
  }) async {
    final rows = await legacy_chat.getChat(studentId, businessId);
    return rows.map(ChatMessage.fromMap).toList(growable: false);
  }

  @override
  Future<void> sendMessage({
    required int studentId,
    required int businessId,
    required String content,
  }) {
    return legacy_chat.guiTinNhan(studentId, businessId, content);
  }
}
