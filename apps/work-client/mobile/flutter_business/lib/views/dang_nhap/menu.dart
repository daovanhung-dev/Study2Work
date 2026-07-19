import 'dart:math';
import 'package:flutter/material.dart';
import 'package:learn2earn/views/cai_dat/setting.dart';
import 'package:learn2earn/views/ung_vien/ung_vien.dart';
import '../tro_chuyen/tro_chuyen.dart';
import '../trang_chu/main/trang_chu.dart';

class Menu extends StatefulWidget {
  const Menu({super.key});

  @override
  State<Menu> createState() => _MenuState();
}

class _MenuState extends State<Menu> with TickerProviderStateMixin {
  int _selectedIndex = 0;

  late final AnimationController _transitionController;
  late final AnimationController _waveController;

  late final Animation<double> _transitionAnim;
  late final Animation<double> _waveAnim;

  final List<Widget> _pages = const [
    trangChu(),
    UngVien(),
    TroChuyen(),
    Setting(),
  ];

  final List<IconData> _icons = const [
    Icons.home_outlined,
    Icons.person_outline,
    Icons.chat_bubble_outline,
    Icons.settings_outlined,
  ];

  IconData _activeIcon(int i) {
    switch (i) {
      case 0:
        return Icons.home;
      case 1:
        return Icons.person;
      case 2:
        return Icons.chat_rounded;
      case 3:
        return Icons.settings_rounded;
      default:
        return Icons.circle;
    }
  }

  @override
  void initState() {
    super.initState();
    _transitionController =
        AnimationController(vsync: this, duration: const Duration(milliseconds: 500));
    _waveController =
    AnimationController(vsync: this, duration: const Duration(seconds: 8))
      ..repeat(reverse: true);

    _transitionAnim = CurvedAnimation(parent: _transitionController, curve: Curves.easeInOut);
    _waveAnim = CurvedAnimation(parent: _waveController, curve: Curves.easeInOut);
  }

  @override
  void dispose() {
    _transitionController.dispose();
    _waveController.dispose();
    super.dispose();
  }

  void _onTap(int i) {
    if (i == _selectedIndex) return;
    setState(() => _selectedIndex = i);
    _transitionController.forward(from: 0);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      extendBody: true, // cho phép vẽ dưới bottom bar
      body: Stack(
        children: [
          AnimatedBuilder(
            animation: _waveAnim,
            builder: (_, __) => CustomPaint(
              size: size,
              painter: WavePainter(progress: _waveAnim.value),
            ),
          ),

          // Trang hiện tại
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 500),
            transitionBuilder: (child, anim) {
              final offset = Tween<Offset>(
                begin: const Offset(0.1, 0),
                end: Offset.zero,
              ).animate(anim);
              return SlideTransition(
                position: offset,
                child: FadeTransition(opacity: anim, child: child),
              );
            },
            child: Padding(
              padding: const EdgeInsets.only(bottom: 90), // tạo khoảng trống cho menu
              child: _pages[_selectedIndex],
            ),
          ),

          // Thanh menu
          Align(
            alignment: Alignment.bottomCenter,
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: _buildBottomBar(context),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomBar(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 24),
      padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.9),
        borderRadius: BorderRadius.circular(40),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 12,
            offset: const Offset(0, 3),
          )
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: List.generate(_icons.length, (i) {
          final bool active = i == _selectedIndex;
          return GestureDetector(
            onTap: () => _onTap(i),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              curve: Curves.easeInOut,
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: active ? Colors.blueAccent : Colors.transparent,
                shape: BoxShape.circle,
                boxShadow: active
                    ? [
                  BoxShadow(
                    color: Colors.blueAccent.withOpacity(0.4),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  )
                ]
                    : [],
              ),
              child: AnimatedScale(
                duration: const Duration(milliseconds: 300),
                scale: active ? 1.25 : 1.0,
                child: Icon(
                  active ? _activeIcon(i) : _icons[i],
                  color: active ? Colors.white : Colors.grey[700],
                  size: active ? 26 : 22,
                ),
              ),
            ),
          );
        }),
      ),
    );
  }
}

// ====================== WAVE NỀN ======================
class WavePainter extends CustomPainter {
  final double progress;
  WavePainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..shader = LinearGradient(
        colors: [
          const Color(0xFF4facfe).withOpacity(0.25),
          const Color(0xFF00f2fe).withOpacity(0.15),
        ],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ).createShader(Rect.fromLTWH(0, 0, size.width, size.height));

    final path = Path();
    double waveH = 25;
    double waveL = size.width / 1.2;
    path.moveTo(0, size.height);
    for (double i = 0; i <= size.width; i++) {
      path.lineTo(
        i,
        size.height -
            (sin((i / waveL * 2 * pi) + (progress * 2 * pi)) * waveH + 40),
      );
    }
    path.lineTo(size.width, size.height);
    path.close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
