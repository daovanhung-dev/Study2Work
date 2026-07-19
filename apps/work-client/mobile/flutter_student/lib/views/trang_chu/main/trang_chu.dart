import 'package:flutter/material.dart';
import 'package:learn2earn/controllers/trang_chu/trang_chu_ctrl.dart';
import 'package:learn2earn/helper_db/out_meta/helper_db_error.dart';
import 'package:learn2earn/helper_db/out_meta/helper_supabase_error.dart';
import 'package:learn2earn/models/sinh_vien/JD.dart';
import 'package:learn2earn/views/trang_chu/main/thong_tin_chi_tiet.dart';
import 'package:learn2earn/views/trang_chu/main/xem_chi_tiet_view.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_CV.dart';
import 'package:learn2earn/views/tim_kiem_cong_viec/tim_kiem_Job.dart';
import 'thong_bao.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart';
import 'package:learn2earn/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart';

final sqlite = HelperDB.instance;
final supabase = DNSupabase.instance;

class TrangChu extends StatefulWidget {
  const TrangChu({super.key});

  @override
  State<TrangChu> createState() => _TrangChuState();
}

class _TrangChuState extends State<TrangChu>
    with SingleTickerProviderStateMixin {
  final TrangChuCtrl _ctrl = TrangChuCtrl();
  String? name;
  String? img;
  late final Future<List<JD>> _futureTopJobs;
  late final AnimationController _animController;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );
    _loadThongTin();
    _futureTopJobs = _safeGetTopJDs();
    _animController.forward();
  }

  Future<List<JD>> _safeGetTopJDs() async {
    try {
      return await _ctrl.get_Top_JD();
    } catch (e) {
      debugPrint('Lỗi khi lấy top jobs: $e');
      return <JD>[];
    }
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  Future<void> _loadThongTin() async {
    try {
      final nameTemp = await _ctrl.getNameSV();
      final imgTemp = await _ctrl.getImgSV();
      if (mounted) {
        setState(() {
          name = nameTemp;
          img = imgTemp;
        });
      }
    } catch (e) {
      debugPrint('Lỗi load thông tin: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    final bool isWide = mq.size.width > 600;
    final double horizontalMargin = isWide ? 28 : 16;

    return Scaffold(
      backgroundColor: const Color(0xFFF5F9FC),
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            _buildSliverAppBar(context),
            SliverPadding(
              padding: EdgeInsets.symmetric(
                horizontal: horizontalMargin,
                vertical: 12,
              ),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  _buildGreetingSection(),
                  const SizedBox(height: 12),
                  _buildDanhSachCongViec(context),
                  const SizedBox(height: 10),
                  _buildTienIchSection(context),
                  const SizedBox(height: 20),
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // AppBar dạng Sliver - Sửa overflow bằng cách responsive và ẩn subtitle khi quá nhỏ
  Widget _buildSliverAppBar(BuildContext context) {
    return SliverAppBar(
      pinned: true,
      expandedHeight: 20,
      backgroundColor: Colors.transparent,
      elevation: 0,
      flexibleSpace: LayoutBuilder(
        builder: (context, constraints) {
          final maxW = constraints.maxWidth;
          final bool isNarrow = maxW < 360;
          final double avatarRadius = isNarrow
              ? 20.0
              : (maxW > 420 ? 28.0 : 24.0);
          final EdgeInsets contentPadding = const EdgeInsets.symmetric(
            horizontal: 12.0,
            vertical: 8.0,
          );

          return Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF7ecbff), Color(0xFF0984e3)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: SafeArea(
              child: Padding(
                padding: contentPadding,
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    GestureDetector(
                      onTap: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const thongTinChiTiet(),
                        ),
                      ),
                      child: CircleAvatar(
                        radius: avatarRadius,
                        backgroundImage: (img != null && img!.isNotEmpty)
                            ? NetworkImage(img!)
                            : const AssetImage('assets/avatar_default.png')
                                  as ImageProvider,
                        backgroundColor: Colors.white.withOpacity(0.9),
                      ),
                    ),
                    const SizedBox(width: 10),
                    // Flexible area for texts: ensure it can shrink and use ellipsis
                    Expanded(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // name row: use Flexible to avoid overflow
                          Flexible(
                            child: Text(
                              'Xin chào, ${name ?? 'Bạn'}',
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.w700,
                              ),
                              overflow: TextOverflow.ellipsis,
                              maxLines: 1,
                            ),
                          ),
                          // optionally show subtitle on wider screens only
                          if (!isNarrow) const SizedBox(height: 4),
                          if (!isNarrow)
                            Flexible(
                              child: Text(
                                'Tìm việc, quản lý CV, chuẩn bị phỏng vấn',
                                style: const TextStyle(
                                  color: Colors.white70,
                                  fontSize: 13,
                                ),
                                overflow: TextOverflow.ellipsis,
                                maxLines: 1,
                              ),
                            ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    // Constrain IconButton so it won't force row to overflow
                    IconButton(
                      onPressed: () => Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const thongBao()),
                      ),
                      icon: const Icon(
                        Icons.notifications_none_rounded,
                        color: Colors.white,
                      ),
                      constraints: const BoxConstraints(
                        minWidth: 40,
                        minHeight: 40,
                      ),
                      splashRadius: 22,
                      padding: const EdgeInsets.all(6),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildGreetingSection() {
    return FadeTransition(
      opacity: CurvedAnimation(parent: _animController, curve: Curves.easeIn),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(14),
        decoration: _cardStyle(),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text(
              'Gợi ý hôm nay',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text(
              'Xem các vị trí nổi bật hoặc cập nhật CV để tăng cơ hội phỏng vấn.',
              style: TextStyle(fontSize: 13, color: Colors.black54),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDanhSachCongViec(BuildContext context) {
    final mq = MediaQuery.of(context);
    final double screenWidth = mq.size.width;
    final double screenHeight = mq.size.height;

    final double cardHeight = screenHeight * 0.36;
    final double normalizedCardHeight = cardHeight.clamp(240.0, 340.0);
    final double cardWidth = (screenWidth * 0.72).clamp(240.0, 360.0);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: _cardStyle(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Công việc nổi bật',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: normalizedCardHeight + 8,
            child: FutureBuilder<List<JD>>(
              future: _futureTopJobs,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return Center(
                    child: Text('Lỗi khi tải dữ liệu: ${snapshot.error}'),
                  );
                }
                if (!snapshot.hasData || snapshot.data!.isEmpty) {
                  return const Center(
                    child: Text('Không có công việc phù hợp'),
                  );
                }

                final jobs = snapshot.data!;
                return ListView.separated(
                  key: const PageStorageKey('topJobsHorizontal'),
                  scrollDirection: Axis.horizontal,
                  physics: const BouncingScrollPhysics(),
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  itemCount: jobs.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 14),
                  itemBuilder: (context, index) {
                    final jd = jobs[index];
                    return TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0.98, end: 1.0),
                      duration: Duration(milliseconds: 220 + (index * 40)),
                      curve: Curves.easeOut,
                      builder: (context, value, child) =>
                          Transform.scale(scale: value, child: child),
                      child: SizedBox(
                        width: cardWidth,
                        height: normalizedCardHeight,
                        child: _JobCardScrollable(
                          jd: jd,
                          cardHeight: normalizedCardHeight,
                          onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => XemChiTietView(id: jd.id),
                            ),
                          ),
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTienIchSection(BuildContext context) {
    final items = [
      {
        'icon': 'assets/manager.png',
        'title': 'Hồ sơ',
        'page': const QuanLyCVView(),
      },
      {
        'icon': 'assets/tien_ich1.png',
        'title': 'Tìm việc',
        'page': const TimKiemViecView(),
      },
      {
        'icon': 'assets/calendar.png',
        'title': 'Lịch PV',
        'page': const LichPhongVanView(),
      },
      {
        'icon': 'assets/online-learning.png',
        'title': 'Khóa học',
        'page': const KhoaHocView(),
      },
      {
        'icon': 'assets/help-desk.png',
        'title': 'Hỗ trợ',
        'page': const HoTroSinhVienView(),
      },
      {
        'icon': 'assets/newspaper.png',
        'title': 'Tin tức',
        'page': const TinTucView(),
      },
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 16),
          child: Text(
            'Tiện ích',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Colors.black87,
            ),
          ),
        ),
        const SizedBox(height: 14),
        SizedBox(
          height: 130,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            itemCount: items.length,
            separatorBuilder: (_, __) => const SizedBox(width: 16),
            itemBuilder: (context, index) {
              final item = items[index];
              return InkWell(
                borderRadius: BorderRadius.circular(20),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => item['page'] as Widget),
                ),
                child: TweenAnimationBuilder<double>(
                  tween: Tween<double>(begin: 1.0, end: 1.0),
                  duration: const Duration(milliseconds: 200),
                  builder: (context, scale, child) {
                    return Transform.scale(scale: scale, child: child);
                  },
                  child: Container(
                    width: 100,
                    padding: const EdgeInsets.symmetric(
                      vertical: 16,
                      horizontal: 12,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black12.withOpacity(0.05),
                          // bóng nhẹ, hướng xuống
                          blurRadius: 12,
                          offset: const Offset(0, 6),
                        ),
                      ],
                      border: const Border(
                        bottom: BorderSide(
                          color: Colors.grey, // viền dưới mảnh
                          width: 0.5,
                        ),
                      ),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 50,
                          height: 50,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: LinearGradient(
                              colors: [
                                Colors.blue.shade200,
                                Colors.blue.shade400,
                              ],
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black12.withOpacity(0.1),
                                // bóng icon nhẹ
                                blurRadius: 6,
                                offset: const Offset(0, 3),
                              ),
                            ],
                          ),
                          padding: const EdgeInsets.all(10),
                          child: Image.asset(item['icon'] as String),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          item['title'] as String,
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: Colors.black87,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  BoxDecoration _cardStyle() => BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(16),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.06),
        blurRadius: 10,
        offset: const Offset(0, 4),
      ),
    ],
  );
}

// ================= Job Card có scroll dọc nội bộ =================
class _JobCardScrollable extends StatelessWidget {
  final JD jd;
  final double cardHeight;
  final VoidCallback? onTap;

  const _JobCardScrollable({
    Key? key,
    required this.jd,
    this.cardHeight = 300,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // header/footer cố định, phần giữa có thể scroll
    const double headerMin = 72;
    const double footerMin = 78;
    final double availableMiddle = (cardHeight - headerMin - footerMin).clamp(
      80.0,
      220.0,
    );

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(14),
        child: Container(
          height: cardHeight,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: Colors.grey.shade200, width: 0.6),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.03),
                blurRadius: 8,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              SizedBox(
                height: headerMin - 8,
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: _buildLogo(),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            jd.tenViTri.isNotEmpty
                                ? jd.tenViTri
                                : 'Vị trí tuyển dụng',
                            style: const TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w700,
                              color: Colors.black87,
                            ),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            jd.tenCongTy.isNotEmpty
                                ? jd.tenCongTy
                                : 'Công ty chưa xác định',
                            style: const TextStyle(
                              fontSize: 13,
                              color: Colors.blueGrey,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 6),
              const Divider(height: 1),

              // Middle: scrollable khi nội dung vượt
              const SizedBox(height: 6),
              SizedBox(
                height: availableMiddle,
                child: SingleChildScrollView(
                  physics: const BouncingScrollPhysics(),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Wrap(
                        spacing: 8,
                        runSpacing: 6,
                        children: [
                          _infoChip(Icons.business_center, jd.nganh),
                          _infoChip(Icons.bar_chart, jd.capBac),
                          _infoChip(Icons.school, jd.trinhDo),
                          _infoChip(Icons.history_edu, jd.kinhNghiem),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          const Icon(
                            Icons.attach_money,
                            size: 16,
                            color: Colors.green,
                          ),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              jd.mucLuong.isNotEmpty
                                  ? jd.mucLuong
                                  : 'Thoả thuận',
                              style: const TextStyle(
                                color: Colors.green,
                                fontWeight: FontWeight.w600,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          const Icon(
                            Icons.location_on,
                            size: 16,
                            color: Colors.redAccent,
                          ),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              jd.diaDiem.isNotEmpty
                                  ? jd.diaDiem
                                  : 'Không rõ địa điểm',
                              style: const TextStyle(color: Colors.black54),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          const Icon(
                            Icons.access_time,
                            size: 16,
                            color: Colors.blue,
                          ),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              jd.thoiGian.isNotEmpty
                                  ? jd.thoiGian
                                  : 'Toàn thời gian / Bán thời gian',
                              style: const TextStyle(color: Colors.black54),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          const Icon(
                            Icons.event,
                            size: 16,
                            color: Colors.orange,
                          ),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              jd.hanNop.isNotEmpty
                                  ? 'Hạn nộp: ${jd.hanNop}'
                                  : 'Không rõ hạn nộp',
                              style: const TextStyle(color: Colors.black54),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),

                      if ((jd.baoCaoCho?.isNotEmpty ?? false) ||
                          (jd.kyNang?.isNotEmpty ?? false) ||
                          (jd.uuTien?.isNotEmpty ?? false)) ...[
                        const SizedBox(height: 8),
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 8,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              if (jd.baoCaoCho.isNotEmpty)
                                _infoRow(
                                  Icons.supervised_user_circle,
                                  'Báo cáo cho: ${jd.baoCaoCho}',
                                ),
                              if (jd.kyNang.isNotEmpty)
                                _infoRow(
                                  Icons.build,
                                  'Kỹ năng: ${_shorten(jd.kyNang, 90)}',
                                ),
                              if (jd.uuTien.isNotEmpty)
                                _infoRow(
                                  Icons.thumb_up,
                                  'Ưu tiên: ${_shorten(jd.uuTien, 80)}',
                                ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),

              // Footer cố định
              const SizedBox(height: 8),
              Container(
                height: footerMin - 40,
                width: double.infinity,
                padding: const EdgeInsets.symmetric(
                  horizontal: 10,
                  vertical: 10,
                ),
                decoration: BoxDecoration(
                  color: Colors.grey.shade50,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.grey.shade200),
                ),
                child: Text(
                  _shorten(jd.phucLoi.isNotEmpty ? jd.phucLoi : jd.moTa, 180),
                  style: const TextStyle(fontSize: 13, color: Colors.black87),
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLogo() {
    final String avt = jd.avt;
    if (avt.isNotEmpty) {
      return Image.network(
        avt,
        width: 52,
        height: 52,
        fit: BoxFit.cover,
        errorBuilder: (_, __, ___) => _defaultLogo(),
        loadingBuilder: (context, child, progress) {
          if (progress == null) return child;
          return SizedBox(
            width: 52,
            height: 52,
            child: Center(
              child: CircularProgressIndicator(
                value: progress.expectedTotalBytes != null
                    ? progress.cumulativeBytesLoaded /
                          (progress.expectedTotalBytes ?? 1)
                    : null,
              ),
            ),
          );
        },
      );
    } else {
      return _defaultLogo();
    }
  }

  Widget _infoChip(IconData icon, String text) {
    if (text.isEmpty) return const SizedBox.shrink();
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: Colors.blue, size: 14),
          const SizedBox(width: 6),
          Flexible(
            child: Text(
              text,
              style: const TextStyle(fontSize: 12, color: Colors.blue),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  Widget _infoRow(IconData icon, String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Colors.blueAccent, size: 14),
          const SizedBox(width: 6),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(fontSize: 13, color: Colors.black87),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  Widget _defaultLogo() => Container(
    width: 52,
    height: 52,
    color: Colors.grey.shade200,
    child: const Icon(Icons.image_not_supported, color: Colors.grey, size: 28),
  );

  String _shorten(String input, int max) =>
      input.length <= max ? input : '${input.substring(0, max - 3)}...';
}

// ================= Tiện ích nhỏ =================
class _TienIchItem extends StatelessWidget {
  final String iconPath;
  final String title;
  final Widget page;

  const _TienIchItem({
    required this.iconPath,
    required this.title,
    required this.page,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: const Color(0xFFdbf0fc),
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        onTap: () =>
            Navigator.push(context, MaterialPageRoute(builder: (_) => page)),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          width: 86,
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Flexible(
                child: Image.asset(
                  iconPath,
                  width: 34,
                  height: 34,
                  fit: BoxFit.contain,
                ),
              ),
              const SizedBox(height: 8),
              Flexible(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w600,
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
