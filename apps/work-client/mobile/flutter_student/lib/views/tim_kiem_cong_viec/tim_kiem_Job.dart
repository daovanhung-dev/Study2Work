import 'package:flutter/material.dart';
import 'package:learn2earn/controllers/tim_kiem_job/tim_kiem_ctrl.dart';
import 'package:learn2earn/models/sinh_vien/JD.dart';
import 'package:learn2earn/views/trang_chu/main/xem_chi_tiet_view.dart';
import 'package:learn2earn/controllers/UngTuyenCtrl.dart';
class TimKiemViecView extends StatefulWidget {
  const TimKiemViecView({super.key});

  @override
  State<TimKiemViecView> createState() => _TimKiemViecViewState();
}

class _TimKiemViecViewState extends State<TimKiemViecView> {
  final ctrl = TimKiemCtrl();
  final ung_tuyen_ctrl = UngTuyenCtrl();
  final _searchController = TextEditingController();

  final List<String> diaDiems = [
    "Tất cả", "Hà Nội", "TP.HCM", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu",
    "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận",
    "Cà Mau", "Cao Bằng", "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp",
    "Gia Lai", "Hà Giang", "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình",
    "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng",
    "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình",
    "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi",
    "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình",
    "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh",
    "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái",
  ];

  final loais = ["Tất cả", "Thực tập", "Part-time", "Full-time"];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => isLoading = true);
    await ctrl.loadJobs();
    setState(() => isLoading = false);
  }

  void _onSearchChanged(String v) {
    ctrl.tuKhoa = v;
    ctrl.filterJobs();
    setState(() {});
  }

  void _onFilterChanged() {
    ctrl.filterJobs();
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F7FB),
      appBar: AppBar(
        title: const Text("Tìm kiếm việc làm",
            style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1976D2),
        centerTitle: true,
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
        onRefresh: _loadData,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            children: [
              _buildSearchBar(),
              const SizedBox(height: 8),
              _buildFilters(),
              const SizedBox(height: 12),
              Expanded(child: _buildJobList()),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSearchBar() => TextField(
    controller: _searchController,
    decoration: InputDecoration(
      hintText: "Nhập tên công việc hoặc công ty...",
      prefixIcon: const Icon(Icons.search),
      filled: true,
      fillColor: Colors.white,
      contentPadding: const EdgeInsets.symmetric(vertical: 10),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: BorderSide.none,
      ),
    ),
    onChanged: _onSearchChanged,
  );

  Widget _buildFilters() => Row(
    children: [
      Expanded(
        child: _buildDropdown(
          value: ctrl.diaDiem,
          items: diaDiems,
          onChanged: (v) {
            ctrl.diaDiem = v!;
            _onFilterChanged();
          },
        ),
      ),
      const SizedBox(width: 10),
      Expanded(
        child: _buildDropdown(
          value: ctrl.loai,
          items: loais,
          onChanged: (v) {
            ctrl.loai = v!;
            _onFilterChanged();
          },
        ),
      ),
    ],
  );

  Widget _buildDropdown({
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          isExpanded: true,
          items: items
              .map((e) => DropdownMenuItem(
            value: e,
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 240),
              child: Text(e, overflow: TextOverflow.ellipsis),
            ),
          ))
              .toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildJobList() {
    if (ctrl.filtered.isEmpty) {
      return const Center(
        child: Text(
          "Không tìm thấy công việc phù hợp",
          style: TextStyle(color: Colors.grey),
        ),
      );
    }

    return ListView.separated(
      itemCount: ctrl.filtered.length,
      separatorBuilder: (_, __) => const SizedBox(height: 10),
      itemBuilder: (_, i) {
        final JD job = ctrl.filtered[i];
        return JobCardScrollable(
          jd: job,
          onTap: () {

          },
        );
      },
    );
  }
}

// ------------------------------------------------------------
// 🔹 CLASS THẺ JOB ĐẸP, KHÔNG OVERFLOW (ĐÃ FIX)
// ------------------------------------------------------------
class JobCardScrollable extends StatelessWidget {
  final JD jd;
  final VoidCallback? onTap;
  final double cardHeight;

  const JobCardScrollable({
    super.key,
    required this.jd,
    this.onTap,
    this.cardHeight = 420,
  });

  @override
  Widget build(BuildContext context) {
    const double headerH = 72;
    const double footerH = 70;
    final double midH = (cardHeight - headerH - footerH).clamp(80, 220);

    return InkWell(
      borderRadius: BorderRadius.circular(14),
      onTap: onTap,
      child: Container(
        height: cardHeight,
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: Colors.grey.shade200),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.04),
              blurRadius: 6,
              offset: const Offset(0, 3),
            )
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // HEADER
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildLogo(jd.avt),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // title: maxLines 2 + ellipsis
                      Text(
                        jd.tenViTri.isNotEmpty ? jd.tenViTri : "Vị trí tuyển dụng",
                        style: const TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                            color: Colors.black87),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 4),
                      // company: single line truncated
                      Text(
                        jd.tenCongTy.isNotEmpty
                            ? jd.tenCongTy
                            : "Công ty chưa xác định",
                        style: const TextStyle(fontSize: 13, color: Colors.blueGrey),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                )
              ],
            ),

            const SizedBox(height: 8),
            const Divider(height: 1),
            const SizedBox(height: 8),

            // MIDDLE SCROLLABLE
            SizedBox(
              height: midH,
              child: SingleChildScrollView(
                physics: const BouncingScrollPhysics(),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // CHIPS: each chip constrained to avoid overflow
                    Wrap(
                      spacing: 8,
                      runSpacing: 6,
                      children: [
                        _chip(context, Icons.business_center, jd.nganh),
                        _chip(context, Icons.school, jd.trinhDo),
                        _chip(context, Icons.bar_chart, jd.capBac),
                        _chip(context, Icons.history_edu, jd.kinhNghiem),
                      ],
                    ),
                    const SizedBox(height: 8),

                    // rows: each uses Flexible to prevent overflow
                    _row(Icons.attach_money, jd.mucLuong.isNotEmpty ? jd.mucLuong : "Thỏa thuận", Colors.green),
                    _row(Icons.location_on, jd.diaDiem.isNotEmpty ? jd.diaDiem : "Không rõ địa điểm", Colors.redAccent),
                    _row(Icons.access_time, jd.thoiGian.isNotEmpty ? jd.thoiGian : "Toàn thời gian / Bán thời gian", Colors.blue),
                    _row(Icons.event, jd.hanNop.isNotEmpty ? "Hạn nộp: ${jd.hanNop}" : "Không rõ hạn nộp", Colors.orange),

                    if ((jd.kyNang.isNotEmpty) || (jd.uuTien.isNotEmpty))
                      Padding(
                        padding: const EdgeInsets.only(top: 6),
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50.withOpacity(0.3),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              if (jd.kyNang.isNotEmpty) _smallInfo(Icons.build, "Kỹ năng: ${_short(jd.kyNang, 120)}"),
                              if (jd.uuTien.isNotEmpty) _smallInfo(Icons.thumb_up, "Ưu tiên: ${_short(jd.uuTien, 120)}"),
                            ],
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 8),

            // FOOTER: limited lines and ellipsis
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.grey.shade50,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                _short(jd.phucLoi.isNotEmpty ? jd.phucLoi : jd.moTa, 220),
                style: const TextStyle(fontSize: 13, color: Colors.black87),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
            ),

            const SizedBox(height: 6),

            // BUTTON: constrained so it never causes overflow
            Align(
              alignment: Alignment.centerRight,
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 140),
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    textStyle: const TextStyle(fontSize: 13),
                  ),
                  onPressed: () {
                    Navigator.push(context,MaterialPageRoute(builder: (context) => XemChiTietView(id: jd.id),),);
                  },
                  icon: const Icon(Icons.arrow_forward_ios, size: 14),
                  label: const Text("Xem chi tiết"),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLogo(String avt) {
    // always return fixed-size widget (no overflow)
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: SizedBox(
        width: 52,
        height: 52,
        child: avt.isNotEmpty
            ? Image.network(
          avt,
          width: 52,
          height: 52,
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => _defaultLogo(),
          loadingBuilder: (context, child, progress) {
            if (progress == null) return child;
            return Center(
              child: SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  value: progress.expectedTotalBytes != null
                      ? progress.cumulativeBytesLoaded / (progress.expectedTotalBytes ?? 1)
                      : null,
                ),
              ),
            );
          },
        )
            : _defaultLogo(),
      ),
    );
  }

  Widget _defaultLogo() => Container(
    width: 52,
    height: 52,
    color: Colors.grey.shade200,
    child: const Icon(Icons.image_not_supported, color: Colors.grey, size: 26),
  );

  // Chip with constrained width and ellipsis
  Widget _chip(BuildContext context, IconData icon, String text) {
    if (text.isEmpty) return const SizedBox.shrink();
    // compute reasonable max for chip based on screen width
    final maxChip = MediaQuery.of(context).size.width * 0.45;
    return ConstrainedBox(
      constraints: BoxConstraints(maxWidth: maxChip, minWidth: 0),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        decoration: BoxDecoration(
          color: Colors.blue.shade50,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(icon, size: 14, color: Colors.blue),
          const SizedBox(width: 5),
          Flexible(
            child: Text(
              text,
              style: const TextStyle(fontSize: 12, color: Colors.blue),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ]),
      ),
    );
  }

  // Row that protects long text using Flexible
  Widget _row(IconData icon, String text, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Icon(icon, size: 15, color: color),
          const SizedBox(width: 5),
          Flexible(
            child: Text(
              text,
              style: TextStyle(fontSize: 13, color: color),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  Widget _smallInfo(IconData icon, String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 14, color: Colors.blueAccent),
          const SizedBox(width: 5),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(fontSize: 13, color: Colors.black87),
              maxLines: 3,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  String _short(String s, int max) => s.length <= max ? s : "${s.substring(0, max - 3)}...";
}
