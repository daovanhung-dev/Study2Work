import 'package:flutter/material.dart';
import 'quen_mat_khau.dart';
import 'menu.dart';
import 'package:learn2earn/controllers/dang_nhap/dangnhap_ctrl.dart';
import 'package:learn2earn/helper_db/helper_supabase.dart';
import 'package:shimmer/shimmer.dart';

class DangNhap extends StatefulWidget {
  const DangNhap({super.key});

  @override
  State<DangNhap> createState() => _DangNhapState();
}

class _DangNhapState extends State<DangNhap> with SingleTickerProviderStateMixin {
  final TextEditingController _emailCtrl = TextEditingController();
  final TextEditingController _passCtrl = TextEditingController();

  bool _isLoading = false;
  bool _isChecking = true;

  late AnimationController _bgController;
  late Animation<Color?> _bgAnimation;

  @override
  void initState() {
    super.initState();
    _autoLogin();
    _bgController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 6),
    )..repeat(reverse: true);
    _bgAnimation = ColorTween(
      begin: Colors.blue.shade50,
      end: Colors.blue.shade100,
    ).animate(CurvedAnimation(parent: _bgController, curve: Curves.easeInOut));
  }

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    _bgController.dispose();
    super.dispose();
  }

  Future<void> _autoLogin() async {
    try {
      final user = await Sqlite.getDangNhap();
      if (user != null &&
          await Supabase.ktDangNhap(user['email'], user['matkhau'])) {
        await Future.delayed(const Duration(milliseconds: 600));
        if (mounted) _navigateToMenu();
        return;
      }
    } catch (_) {}
    if (mounted) setState(() => _isChecking = false);
  }

  void _showSnack(String message, {bool short = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: short
            ? const Duration(milliseconds: 800)
            : const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }

  Future<void> _onLoginPressed() async {
    final email = _emailCtrl.text.trim();
    final pass = _passCtrl.text.trim();

    if (email.isEmpty || pass.isEmpty) {
      _showSnack("Vui lòng nhập email và mật khẩu");
      return;
    }

    setState(() => _isLoading = true);

    try {
      final ok = await dangNhapDN(email, pass);
      if (ok) {
        _showSnack("Đăng nhập thành công!", short: true);
        await Future.delayed(const Duration(milliseconds: 500));
        _navigateToMenu();
      } else {
        _showSnack("Sai email hoặc mật khẩu!");
      }
    } catch (e) {
      _showSnack("Lỗi: $e");
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _navigateToMenu() {
    Navigator.pushReplacement(
      context,
      PageRouteBuilder(
        transitionDuration: const Duration(milliseconds: 600),
        pageBuilder: (_, __, ___) => const Menu(),
        transitionsBuilder: (_, animation, __, child) => FadeTransition(
          opacity: CurvedAnimation(parent: animation, curve: Curves.easeInOut),
          child: child,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isChecking) {
      return AnimatedBuilder(
        animation: _bgAnimation,
        builder: (context, child) => Scaffold(
          body: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [_bgAnimation.value!, Colors.white],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  _AnimatedLoader(),
                  SizedBox(height: 20),
                  _ShimmerText(),
                  SizedBox(height: 20),
                  _BouncingDots(),
                ],
              ),
            ),
          ),
        ),
      );
    }

    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: Stack(
        children: [
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.blue.shade50, Colors.white],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ),
            ),
          ),
          Container(color: Colors.white.withOpacity(0.15)), // overlay nhẹ
          SafeArea(
            child: SingleChildScrollView(
              padding: EdgeInsets.only(
                left: 16,
                right: 16,
                bottom: MediaQuery.of(context).viewInsets.bottom + 20,
                top: 40,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const SizedBox(height: 60),
                  Image.asset('assets/logo-nobr.png', width: 150),
                  const SizedBox(height: 40),
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.95),
                      borderRadius: BorderRadius.circular(25),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.08),
                          blurRadius: 15,
                          offset: const Offset(0, 6),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        TextField(
                          controller: _emailCtrl,
                          keyboardType: TextInputType.emailAddress,
                          decoration: InputDecoration(
                            labelText: "Email",
                            labelStyle: TextStyle(
                                color: Colors.grey.shade800,
                                fontWeight: FontWeight.w500),
                            prefixIcon: Icon(Icons.email_outlined,
                                color: Colors.blue.shade400),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(15),
                            ),
                            filled: true,
                            fillColor: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 20),
                        TextField(
                          controller: _passCtrl,
                          obscureText: true,
                          decoration: InputDecoration(
                            labelText: "Mật khẩu",
                            labelStyle: TextStyle(
                                color: Colors.grey.shade800,
                                fontWeight: FontWeight.w500),
                            prefixIcon:
                            Icon(Icons.lock_outline, color: Colors.blue.shade400),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(15),
                            ),
                            filled: true,
                            fillColor: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 10),
                        Align(
                          alignment: Alignment.centerRight,
                          child: TextButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => const QuenMatKhau(),
                                ),
                              );
                            },
                            child: Text("Quên mật khẩu?",
                                style: TextStyle(
                                    color: Colors.blue.shade400,
                                    fontWeight: FontWeight.w600)),
                          ),
                        ),
                        const SizedBox(height: 20),
                        SizedBox(
                          width: double.infinity,
                          height: 50,
                          child: ElevatedButton(
                            onPressed: _isLoading ? null : _onLoginPressed,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.blue.shade400,
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(15),
                              ),
                            ),
                            child: _isLoading
                                ? const SizedBox(
                              width: 25,
                              height: 25,
                              child: CircularProgressIndicator(
                                color: Colors.white,
                                strokeWidth: 3,
                              ),
                            )
                                : const Text("Đăng Nhập",
                                style: TextStyle(
                                    fontSize: 18, fontWeight: FontWeight.bold)),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 60),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// Loader/shimmer/dots nhẹ nhàng hơn, màu Facebook-like
class _AnimatedLoader extends StatefulWidget {
  const _AnimatedLoader({super.key});

  @override
  State<_AnimatedLoader> createState() => _AnimatedLoaderState();
}

class _AnimatedLoaderState extends State<_AnimatedLoader>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller =
    AnimationController(vsync: this, duration: const Duration(seconds: 2))
      ..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RotationTransition(
      turns: _controller,
      child: const SizedBox(
        width: 50,
        height: 50,
        child: CircularProgressIndicator(
          strokeWidth: 4,
          color: Colors.blueAccent,
        ),
      ),
    );
  }
}

class _ShimmerText extends StatelessWidget {
  const _ShimmerText({super.key});

  @override
  Widget build(BuildContext context) {
    return Shimmer.fromColors(
      baseColor: Colors.blue.shade300,
      highlightColor: Colors.white,
      period: const Duration(seconds: 2),
      child: const Text(
        "Đang kiểm tra đăng nhập...",
        style: TextStyle(
            fontSize: 16, fontWeight: FontWeight.w500, letterSpacing: 1.0),
      ),
    );
  }
}

class _BouncingDots extends StatefulWidget {
  const _BouncingDots({super.key});

  @override
  State<_BouncingDots> createState() => _BouncingDotsState();
}

class _BouncingDotsState extends State<_BouncingDots>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation1;
  late Animation<double> _animation2;
  late Animation<double> _animation3;

  @override
  void initState() {
    super.initState();
    _controller =
    AnimationController(vsync: this, duration: const Duration(seconds: 1))
      ..repeat();
    _animation1 =
        Tween<double>(begin: 0, end: -8).animate(CurvedAnimation(
          parent: _controller,
          curve: const Interval(0.0, 0.33, curve: Curves.easeInOut),
        ));
    _animation2 =
        Tween<double>(begin: 0, end: -8).animate(CurvedAnimation(
          parent: _controller,
          curve: const Interval(0.33, 0.66, curve: Curves.easeInOut),
        ));
    _animation3 =
        Tween<double>(begin: 0, end: -8).animate(CurvedAnimation(
          parent: _controller,
          curve: const Interval(0.66, 1.0, curve: Curves.easeInOut),
        ));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Widget _dot(Animation<double> animation) {
    return AnimatedBuilder(
      animation: animation,
      builder: (_, child) => Transform.translate(
        offset: Offset(0, animation.value),
        child: child,
      ),
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 3),
        width: 10,
        height: 10,
        decoration: BoxDecoration(
            color: Colors.blue.shade300, shape: BoxShape.circle),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        _dot(_animation1),
        _dot(_animation2),
        _dot(_animation3),
      ],
    );
  }
}
