import 'dart:math';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:learn2earn/views/cai_dat/setting.dart';
import 'package:learn2earn/views/tim_kiem_cong_viec/tim_kiem_Job.dart';
import '../tro_chuyen/tro_chuyen.dart';
import '../trang_chu/main/trang_chu.dart';

class Menu extends StatefulWidget {
  const Menu({super.key});

  @override
  State<Menu> createState() => _MenuState();
}

class _MenuState extends State<Menu> with TickerProviderStateMixin {
  int _selectedIndex = 0;

  late final AnimationController _waveController;

  final List<Widget> _pages = const [
    TrangChu(),
    TimKiemViecView(),
    TroChuyen(),
    Setting(),
  ];

  final List<IconData> _icons = const [
    Icons.home_outlined,
    Icons.search_outlined,
    Icons.chat_bubble_outline,
    Icons.settings_outlined,
  ];

  IconData _activeIcon(int i) {
    switch (i) {
      case 0:
        return Icons.home_rounded;
      case 1:
        return Icons.search_rounded;
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
    _waveController =
    AnimationController(vsync: this, duration: const Duration(seconds: 6))
      ..repeat(reverse: true);
  }

  @override
  void dispose() {
    _waveController.dispose();
    super.dispose();
  }

  void _onTap(int i) {
    if (i == _selectedIndex) return;
    setState(() => _selectedIndex = i);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      extendBody: true,
      body: Stack(
        children: [
          // ==== Wave nền ====
          AnimatedBuilder(
            animation: _waveController,
            builder: (_, __) => CustomPaint(
              size: size,
              painter: WavePainter(progress: _waveController.value),
            ),
          ),

          // ==== Trang hiện tại ====
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 500),
            transitionBuilder: (child, anim) {
              final offset = Tween<Offset>(
                begin: const Offset(0.1, 0),
                end: Offset.zero,
              ).animate(anim);
              final scale = Tween<double>(begin: 0.95, end: 1).animate(anim);
              return SlideTransition(
                position: offset,
                child: FadeTransition(
                  opacity: anim,
                  child: ScaleTransition(scale: scale, child: child),
                ),
              );
            },
            child: Padding(
              key: ValueKey(_selectedIndex),
              padding: const EdgeInsets.only(bottom: 100),
              child: _pages[_selectedIndex],
            ),
          ),

          // ==== Bottom Menu Floating ====
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: _buildBottomBar(context),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomBar(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(40),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: 24),
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.25),
            borderRadius: BorderRadius.circular(40),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.08),
                blurRadius: 12,
                offset: const Offset(0, 4),
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
                    color: active ? Colors.blueAccent.withOpacity(0.8) : Colors.transparent,
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
                    scale: active ? 1.3 : 1.0,
                    curve: Curves.easeInOutBack,
                    child: Icon(
                      active ? _activeIcon(i) : _icons[i],
                      color: active ? Colors.white : Colors.grey[700],
                      size: active ? 28 : 24,
                    ),
                  ),
                ),
              );
            }),
          ),
        ),
      ),
    );
  }
}

// ====================== WAVE NỀN CẢI TIẾN ======================
class WavePainter extends CustomPainter {
  final double progress;
  WavePainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..shader = LinearGradient(
        colors: [
          const Color(0xFF4facfe).withOpacity(0.3),
          const Color(0xFF00f2fe).withOpacity(0.15),
        ],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ).createShader(Rect.fromLTWH(0, 0, size.width, size.height));

    final path = Path();
    double waveH = 30;
    double waveL = size.width / 1.5;
    path.moveTo(0, size.height);
    for (double i = 0; i <= size.width; i++) {
      path.lineTo(
        i,
        size.height - (sin((i / waveL * 2 * pi) + (progress * 2 * pi)) * waveH + 40),
      );
    }
    path.lineTo(size.width, size.height);
    path.close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
