import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/services.dart';
import 'package:learn2earn/views/dang_nhap/dang_nhap.dart';

class KiemTraWifiView extends StatefulWidget {
  const KiemTraWifiView({super.key});

  @override
  State<KiemTraWifiView> createState() => _KiemTraWifiViewState();
}

class _KiemTraWifiViewState extends State<KiemTraWifiView>
    with SingleTickerProviderStateMixin {
  StreamSubscription<List<ConnectivityResult>>? _connectivitySub;
  bool _alreadyRetried = false;
  late AnimationController _rippleController;

  @override
  void initState() {
    super.initState();

    _rippleController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _kiemTraWifi();

      _connectivitySub = Connectivity().onConnectivityChanged.listen((results) {
        final status = results.isNotEmpty ? results.first : ConnectivityResult.none;

        if ((status == ConnectivityResult.wifi || status == ConnectivityResult.ethernet) &&
            !_alreadyRetried) {
          _alreadyRetried = true;
          Future.delayed(const Duration(seconds: 1), () => _kiemTraWifi());
        }
      });
    });
  }

  @override
  void dispose() {
    _rippleController.dispose();
    _connectivitySub?.cancel();
    super.dispose();
  }

  Future<void> _kiemTraWifi() async {
    try {
      final connectivityResultList = await Connectivity().checkConnectivity();
      final connectivityResult = connectivityResultList.isNotEmpty
          ? connectivityResultList.first
          : ConnectivityResult.none;

      if (connectivityResult == ConnectivityResult.wifi ||
          connectivityResult == ConnectivityResult.ethernet) {
        final hasNetwork = await _checkSocketConnection(timeoutSeconds: 3);
        if (hasNetwork) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (!mounted) return;
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (_) => const DangNhap()),
            );
          });
        } else {
          _showSnackAndExit("⚠️ WiFi đang bật nhưng không có Internet.");
        }
      } else {
        _showSnackAndExit("⚠️ Bạn chưa kết nối WiFi. Ứng dụng sẽ thoát.");
      }
    } catch (e) {
      _showSnackAndExit("❌ Lỗi kiểm tra mạng: $e");
    }
  }

  Future<bool> _checkSocketConnection({int timeoutSeconds = 3}) async {
    try {
      final socket = await Socket.connect('8.8.8.8', 53,
          timeout: Duration(seconds: timeoutSeconds));
      socket.destroy();
      return true;
    } catch (_) {
      return false;
    }
  }

  void _showSnackAndExit(String message) {
    if (!mounted) return;
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.redAccent,
          duration: const Duration(seconds: 3),
        ),
      );
      await Future.delayed(const Duration(seconds: 3));
      SystemNavigator.pop();
    });
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: Colors.blue.shade50,
      body: Stack(
        alignment: Alignment.center,
        children: [
          // Hiệu ứng sóng nước
          AnimatedBuilder(
            animation: _rippleController,
            builder: (context, child) {
              return CustomPaint(
                size: Size(size.width, size.height),
                painter: _WaterRipplePainter(_rippleController.value),
              );
            },
          ),

          // Nội dung trung tâm
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.waves_rounded,
                size: 100,
                color: Colors.blueAccent.withOpacity(0.8),
              ),
              const SizedBox(height: 20),
              const Text(
                "Đang kiểm tra kết nối...",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                  color: Colors.black87,
                ),
              ),
              const SizedBox(height: 25),
              const CircularProgressIndicator(
                strokeWidth: 3,
                color: Colors.blueAccent,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _WaterRipplePainter extends CustomPainter {
  final double animationValue;

  _WaterRipplePainter(this.animationValue);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blueAccent.withOpacity(0.05)
      ..style = PaintingStyle.fill;

    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = size.width * 0.5;

    for (int i = 0; i < 3; i++) {
      final radius = maxRadius * (animationValue + i * 0.3);
      paint.color = Colors.blueAccent.withOpacity(0.15 - i * 0.05);
      canvas.drawCircle(center, radius, paint);
    }
  }

  @override
  bool shouldRepaint(_WaterRipplePainter oldDelegate) =>
      oldDelegate.animationValue != animationValue;
}
