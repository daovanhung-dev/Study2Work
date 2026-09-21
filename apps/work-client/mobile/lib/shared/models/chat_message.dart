class ChatMessage {
  const ChatMessage({
    required this.id,
    required this.senderId,
    required this.receiverId,
    required this.content,
    this.sentAt,
    this.status,
  });

  final int id;
  final int senderId;
  final int receiverId;
  final String content;
  final DateTime? sentAt;
  final String? status;

  factory ChatMessage.fromMap(Map<String, dynamic> row) {
    return ChatMessage(
      id: int.tryParse(row['id']?.toString() ?? '') ?? 0,
      senderId: int.tryParse(row['nguoigui']?.toString() ?? '') ?? 0,
      receiverId: int.tryParse(row['nguoinhan']?.toString() ?? '') ?? 0,
      content: row['noidung']?.toString() ?? '',
      sentAt: row['ngaygui'] is DateTime
          ? row['ngaygui'] as DateTime
          : DateTime.tryParse(row['ngaygui']?.toString() ?? ''),
      status: row['trangthai']?.toString(),
    );
  }
}
