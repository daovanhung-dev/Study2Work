import 'package:flutter/material.dart';
import 'package:learn2earn/views/tro_chuyen/chat.dart';
import 'package:learn2earn/controllers/chat/nhung_doan_chat_controller.dart';
import '../trang_chu/main/thong_bao.dart';
import 'package:learn2earn/helper_db/sinh_vien/helper_db.dart';

final sqlite = SinhVienSQLiteHelper.instance;

class TroChuyen extends StatefulWidget {
  const TroChuyen({super.key});

  @override
  State<TroChuyen> createState() => _TroChuyenState();
}

class _TroChuyenState extends State<TroChuyen> {
  int sinhvienId = 0;

  @override
  void initState() {
    super.initState();
    _loadSinhVienId();
  }

  void _loadSinhVienId() async {
    final id = await sqlite.getID();
    setState(() {
      sinhvienId = id;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFe9f6ff),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: const Color(0xFF7ecbff),
        leadingWidth: 60,
        leading: Padding(
          padding: const EdgeInsets.all(8),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(50),
            child: const CircleAvatar(
              backgroundImage: AssetImage("assets/logo.jpg"),
            ),
          ),
        ),
        title: const Text(
          "Trò chuyện",
          style: TextStyle(
              fontWeight: FontWeight.bold, fontSize: 20, color: Colors.white),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications, color: Colors.white),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const thongBao()),
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Stack(
          children: [
            Container(color: Colors.black.withOpacity(0.05)),
            SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 10),
                child: Column(
                  children: [
                    // 🔍 Thanh tìm kiếm
                    Container(
                      margin: const EdgeInsets.symmetric(horizontal: 12),
                      padding: const EdgeInsets.symmetric(horizontal: 15),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.95),
                        borderRadius: BorderRadius.circular(25),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.05),
                            blurRadius: 5,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: const Row(
                        children: [
                          Icon(Icons.search, color: Colors.grey),
                          SizedBox(width: 10),
                          Expanded(
                            child: TextField(
                              decoration: InputDecoration(
                                hintText: "Tìm kiếm cuộc trò chuyện...",
                                border: InputBorder.none,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 10),

                    // 💬 Danh sách chat
                    FutureBuilder<List<Map<String, dynamic>>>(
                      future: getChats(sinhvienId),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return const Padding(
                            padding: EdgeInsets.only(top: 100),
                            child: Center(child: CircularProgressIndicator()),
                          );
                        } else if (snapshot.hasError) {
                          return Center(child: Text("Lỗi: ${snapshot.error}"));
                        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                          return const Padding(
                            padding: EdgeInsets.only(top: 100),
                            child: Center(
                              child: Text(
                                "Chưa có cuộc trò chuyện nào",
                                style: TextStyle(
                                    fontSize: 16,
                                    color: Colors.black54,
                                    fontStyle: FontStyle.italic),
                              ),
                            ),
                          );
                        }

                        final dsChat = snapshot.data!;
                        dsChat.sort((a, b) {
                          final timeA = DateTime.tryParse(a["thoigian"] ?? "") ?? DateTime.now();
                          final timeB = DateTime.tryParse(b["thoigian"] ?? "") ?? DateTime.now();
                          return timeB.compareTo(timeA);
                        });

                        return Column(
                          children: dsChat.map((chatItem) {
                            final doanhnghiepId = chatItem["id"];
                            final hoten = chatItem["hoten"] ?? "Không rõ tên";
                            final lastMsg = chatItem["last_message"] ?? "Nhấn để xem chi tiết";
                            final time = _formatTime(chatItem["thoigian"]);

                            return GestureDetector(
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => ChatView(
                                      doanhnghiepId: doanhnghiepId,
                                    ),
                                  ),
                                );
                              },
                              child: Container(
                                margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
                                padding: const EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: Colors.white,
                                  borderRadius: BorderRadius.circular(15),
                                  boxShadow: [
                                    BoxShadow(
                                      color: Colors.black.withOpacity(0.06),
                                      blurRadius: 6,
                                      offset: const Offset(0, 3),
                                    ),
                                  ],
                                ),
                                child: Row(
                                  children: [
                                    CircleAvatar(
                                      radius: 28,
                                      backgroundColor: const Color(0xFF7ecbff),
                                      child: Text(
                                        hoten.isNotEmpty ? hoten[0].toUpperCase() : "?",
                                        style: const TextStyle(
                                            color: Colors.white,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 20),
                                      ),
                                    ),
                                    const SizedBox(width: 15),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            hoten,
                                            style: const TextStyle(
                                                fontWeight: FontWeight.bold,
                                                fontSize: 16,
                                                color: Colors.black87),
                                          ),
                                          const SizedBox(height: 4),
                                          Text(
                                            lastMsg,
                                            maxLines: 1,
                                            overflow: TextOverflow.ellipsis,
                                            style: const TextStyle(
                                                fontSize: 13,
                                                color: Colors.black54),
                                          ),
                                        ],
                                      ),
                                    ),
                                    Column(
                                      crossAxisAlignment: CrossAxisAlignment.end,
                                      children: [
                                        Text(
                                          time,
                                          style: const TextStyle(fontSize: 11, color: Colors.grey),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                        );
                      },
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color(0xFF7ecbff),
        onPressed: () {},
        child: const Icon(Icons.add_comment_rounded, color: Colors.white),
      ),
    );
  }

  String _formatTime(String? timeString) {
    if (timeString == null || timeString.isEmpty) return "Vừa xong";
    try {
      final time = DateTime.parse(timeString);
      final now = DateTime.now();
      final diff = now.difference(time);

      if (diff.inMinutes < 1) return "Vừa xong";
      if (diff.inMinutes < 60) return "${diff.inMinutes} phút trước";
      if (diff.inHours < 24) return "${diff.inHours} giờ trước";
      return "${time.day}/${time.month}/${time.year}";
    } catch (e) {
      return "Vừa xong";
    }
  }
}
