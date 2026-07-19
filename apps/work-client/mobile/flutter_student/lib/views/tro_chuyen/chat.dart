import 'package:flutter/material.dart';
import 'package:learn2earn/controllers/chat/chat_controller.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:supabase/supabase.dart' hide RealtimeClient;
import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';
import 'dart:async';

final sqlite = SinhVienSQLiteHelper.instance;

class ChatView extends StatefulWidget {
  final int doanhnghiepId; // doanh nghiệp chat cùng

  const ChatView({super.key, required this.doanhnghiepId});

  @override
  State<ChatView> createState() => _ChatViewState();
}

class _ChatViewState extends State<ChatView> with TickerProviderStateMixin {
  int? sinhvienId;
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final GlobalKey<AnimatedListState> _listKey = GlobalKey<AnimatedListState>();
  List<Map<String, dynamic>> messages = [];
  late RealtimeChannel _channel;

  @override
  void initState() {
    super.initState();
    _loadSinhVienId();
  }

  // 🔹 Lấy ID sinh viên từ SQLite
  void _loadSinhVienId() async {
    final id = await sqlite.getID();
    setState(() {
      sinhvienId = id;
    });
    _loadMessages();
    _listenRealtime();
  }

  // 🔹 Load tin nhắn cũ
  Future<void> _loadMessages() async {
    if (sinhvienId == null) return;

    final data = await getChat(sinhvienId!, widget.doanhnghiepId);

    // Sắp xếp từ cũ → mới
    data.sort((a, b) {
      final timeA = DateTime.tryParse(a['ngaygui'] ?? '') ?? DateTime.now();
      final timeB = DateTime.tryParse(b['ngaygui'] ?? '') ?? DateTime.now();
      return timeA.compareTo(timeB);
    });

    setState(() {
      messages = data;
    });

    // AnimatedList insert
    for (int i = 0; i < messages.length; i++) {
      _listKey.currentState?.insertItem(i, duration: const Duration(milliseconds: 0));
    }

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
      }
    });
  }

  // 🔹 Lắng nghe Realtime
  void _listenRealtime() {
    if (sinhvienId == null) return;

    _channel = subscribeMessages((newMsg) {
      if (newMsg['sinhvien_id'] == sinhvienId &&
          newMsg['doanhnghiep_id'] == widget.doanhnghiepId) {
        final exists = messages.any((m) =>
        m['noidung'] == newMsg['noidung'] &&
            m['ngaygui'] == newMsg['ngaygui'] &&
            m['nguoigui'] == newMsg['nguoigui']);
        if (!exists) {
          _addMessage(newMsg);
        }
      }
    });
  }

  // 🔹 Thêm tin nhắn mới vào AnimatedList
  void _addMessage(Map<String, dynamic> msg) {
    setState(() {
      messages.add(msg);
    });
    _listKey.currentState?.insertItem(
      messages.length - 1,
      duration: const Duration(milliseconds: 400),
    );

    Timer(const Duration(milliseconds: 300), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 400),
          curve: Curves.easeOut,
        );
      }
    });
  }

  // 🔹 Gửi tin nhắn
  void _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty || sinhvienId == null) return;

    _controller.clear();

    try {
      await guiTinNhan(sinhvienId!, widget.doanhnghiepId, text);
    } catch (e) {
      // Nếu lỗi mạng → thêm tạm local
      final newMsg = {
        "nguoigui": sinhvienId,
        "noidung": text,
        "ngaygui": DateTime.now().toIso8601String(),
        "sinhvien_id": sinhvienId,
        "doanhnghiep_id": widget.doanhnghiepId,
      };
      _addMessage(newMsg);
    }
  }

  // 🔹 Định dạng thời gian
  String _formatTime(String? time) {
    if (time == null || time.isEmpty) return "Vừa xong";
    try {
      final dt = DateTime.parse(time);
      final now = DateTime.now();
      final diff = now.difference(dt);

      if (diff.inSeconds < 60) return "Vừa xong";
      if (diff.inMinutes < 60) return "${diff.inMinutes} phút trước";
      if (diff.inHours < 24) return "${diff.inHours} giờ trước";
      if (diff.inDays == 1) return "Hôm qua";
      if (diff.inDays < 7) return "${diff.inDays} ngày trước";

      return "${dt.day.toString().padLeft(2, '0')}/${dt.month.toString().padLeft(2, '0')} lúc ${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}";
    } catch (e) {
      return time;
    }
  }

  // 🔹 Xây dựng widget tin nhắn
  Widget _buildMessage(BuildContext context, int index, Animation<double> animation) {
    final chat = messages[index];
    final isSender = chat["nguoigui"]?.toString() == "$sinhvienId";

    return SizeTransition(
      sizeFactor: animation,
      axisAlignment: 0.0,
      child: Align(
        alignment: isSender ? Alignment.centerRight : Alignment.centerLeft,
        child: ConstrainedBox(
          constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.7),
          child: SlideTransition(
            position: Tween<Offset>(
              begin: Offset(isSender ? 1 : -1, 0),
              end: Offset.zero,
            ).animate(CurvedAnimation(parent: animation, curve: Curves.easeOut)),
            child: ScaleTransition(
              scale: Tween<double>(begin: 0.9, end: 1.0).animate(
                CurvedAnimation(parent: animation, curve: Curves.elasticOut),
              ),
              child: Container(
                margin: const EdgeInsets.symmetric(vertical: 5),
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                decoration: BoxDecoration(
                  gradient: isSender
                      ? LinearGradient(colors: [Colors.blue[400]!, Colors.blue[300]!])
                      : LinearGradient(colors: [Colors.grey[300]!, Colors.grey[200]!]),
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(isSender ? 16 : 4),
                    topRight: Radius.circular(isSender ? 4 : 16),
                    bottomLeft: const Radius.circular(16),
                    bottomRight: const Radius.circular(16),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.08),
                      blurRadius: 5,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      chat["noidung"] ?? "",
                      style: const TextStyle(fontSize: 14, color: Colors.black87),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      _formatTime(chat["ngaygui"]?.toString()),
                      style: const TextStyle(fontSize: 10, color: Colors.black54),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _channel.unsubscribe();
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        backgroundColor: const Color(0xFF7ecbff),
        title: const Text("Trò chuyện"),
        elevation: 2,
        shadowColor: Colors.blue.withOpacity(0.2),
      ),
      body: Column(
        children: [
          Expanded(
            child: AnimatedList(
              key: _listKey,
              controller: _scrollController,
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
              initialItemCount: messages.length,
              itemBuilder: _buildMessage,
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            color: Colors.white.withOpacity(0.95),
            child: Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      borderRadius: BorderRadius.circular(25),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.05),
                          blurRadius: 4,
                          offset: const Offset(0, 2),
                        )
                      ],
                    ),
                    child: TextField(
                      controller: _controller,
                      decoration: const InputDecoration(
                        hintText: "Nhập tin nhắn...",
                        border: InputBorder.none,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                GestureDetector(
                  onTap: _sendMessage,
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [Colors.blue[400]!, Colors.blue[300]!],
                      ),
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.blue.withOpacity(0.4),
                          blurRadius: 6,
                          offset: const Offset(0, 3),
                        ),
                      ],
                    ),
                    child: const Icon(Icons.send, color: Colors.white),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
