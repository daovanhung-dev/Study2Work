import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:study2work_mobile/app/theme/app_components.dart';
import 'package:study2work_mobile/app/theme/design_tokens.dart';
import 'package:study2work_mobile/app/router/auth_navigation_state.dart';
import 'package:study2work_mobile/features/auth/domain/auth_repository.dart';
import 'quen_mat_khau.dart';
import 'package:study2work_mobile/features/student/legacy/controllers/dang_nhap/dangnhap_ctrl.dart';
import 'package:shimmer/shimmer.dart';

class DangNhap extends StatefulWidget {
  const DangNhap({this.authRepository, super.key});

  final AuthRepository? authRepository;

  @override
  State<DangNhap> createState() => _DangNhapState();
}

class _DangNhapState extends State<DangNhap>
    with SingleTickerProviderStateMixin {
  final TextEditingController _emailCtrl = TextEditingController();
  final TextEditingController _passCtrl = TextEditingController();

  bool _isLoading = false;
  bool _isChecking = true;

  late AnimationController _bgController;
  late Animation<Color?> _bgAnimation;

  @override
  void initState() {
    super.initState();
    _bgController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 6),
    )..repeat(reverse: true);
    _bgAnimation = ColorTween(
      begin: AppColors.primarySoft,
      end: AppColors.background,
    ).animate(CurvedAnimation(parent: _bgController, curve: Curves.easeInOut));

    _checkAutoLogin();
  }

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    _bgController.dispose();
    super.dispose();
  }

  Future<void> _checkAutoLogin() async {
    final ok = await (widget.authRepository?.restoreSession() ?? autoLogin());
    if (ok && mounted) {
      await Future.delayed(const Duration(milliseconds: 500));
      _navigateToMenu();
    } else if (mounted) {
      setState(() => _isChecking = false);
    }
  }

  void _showSnack(String message, {bool short = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: short
            ? const Duration(milliseconds: 800)
            : const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadii.control)),
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

    final ok = await
        (widget.authRepository?.login(email, pass) ?? dangNhapDN(email, pass));
    if (ok) {
      _showSnack("Đăng nhập thành công!", short: true);
      await Future.delayed(const Duration(milliseconds: 500));
      _navigateToMenu();
    } else {
      _showSnack("Sai email hoặc mật khẩu!");
    }

    if (mounted) setState(() => _isLoading = false);
  }

  void _navigateToMenu() {
    AuthNavigationState.instance.markAuthenticated();
    context.go('/student');
  }

  @override
  Widget build(BuildContext context) {
    if (_isChecking) return _buildLoadingScreen();

    return Scaffold(
      body: Stack(
        children: [
          _buildBackground(),
          SafeArea(
            child: SingleChildScrollView(
              padding: EdgeInsets.only(
                left: 16,
                right: 16,
                bottom: MediaQuery.of(context).viewInsets.bottom + 20,
                top: 60,
              ),
              child: Column(
                children: [
                  Image.asset('assets/student/logo-nobr.png', width: 150),
                  const SizedBox(height: 40),
                  _buildLoginCard(),
                  const SizedBox(height: 60),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBackground() {
    return AnimatedBuilder(
      animation: _bgAnimation,
      builder: (context, child) => Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [_bgAnimation.value!, AppColors.surface],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
      ),
    );
  }

  Widget _buildLoginCard() {
    return AppSurface(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          TextField(
            controller: _emailCtrl,
            keyboardType: TextInputType.emailAddress,
            decoration: InputDecoration(
              labelText: "Email",
              labelStyle: TextStyle(
                color: AppColors.navy,
                fontWeight: FontWeight.w500,
              ),
              prefixIcon: Icon(
                Icons.email_outlined,
                color: AppColors.action,
              ),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              filled: true,
              fillColor: AppColors.surface,
            ),
          ),
          const SizedBox(height: 20),
          TextField(
            controller: _passCtrl,
            obscureText: true,
            decoration: InputDecoration(
              labelText: "Mật khẩu",
              labelStyle: TextStyle(
                color: AppColors.navy,
                fontWeight: FontWeight.w500,
              ),
              prefixIcon: const Icon(Icons.lock_outline, color: AppColors.action),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              filled: true,
              fillColor: AppColors.surface,
            ),
          ),
          const SizedBox(height: 10),
          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const QuenMatKhauView()),
                );
              },
              child: Text(
                "Quên mật khẩu?",
                style: TextStyle(
                  color: AppColors.action,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            height: 50,
            child: ElevatedButton(
              onPressed: _isLoading ? null : _onLoginPressed,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.action,
                foregroundColor: AppColors.surface,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
              ),
              child: _isLoading
                  ? const SizedBox(
                      width: 25,
                      height: 25,
                      child: CircularProgressIndicator(
                        color: AppColors.surface,
                        strokeWidth: 3,
                      ),
                    )
                  : const Text(
                      "Đăng Nhập",
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLoadingScreen() {
    return AnimatedBuilder(
      animation: _bgAnimation,
      builder: (context, child) => Scaffold(
        body: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
            colors: [_bgAnimation.value!, AppColors.surface],
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
}

/// Loader / shimmer / bouncing dots
class _AnimatedLoader extends StatefulWidget {
  const _AnimatedLoader();

  @override
  State<_AnimatedLoader> createState() => _AnimatedLoaderState();
}

class _AnimatedLoaderState extends State<_AnimatedLoader>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat();
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
          color: AppColors.action,
        ),
      ),
    );
  }
}

class _ShimmerText extends StatelessWidget {
  const _ShimmerText();

  @override
  Widget build(BuildContext context) {
    return Shimmer.fromColors(
      baseColor: AppColors.action,
      highlightColor: AppColors.surface,
      period: Duration(seconds: 2),
      child: const Text(
        "Đang kiểm tra đăng nhập...",
        style: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w500,
          letterSpacing: 1.0,
        ),
      ),
    );
  }
}

class _BouncingDots extends StatefulWidget {
  const _BouncingDots();

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
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    )..repeat();
    _animation1 = Tween<double>(begin: 0, end: -8).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.0, 0.33, curve: Curves.easeInOut),
      ),
    );
    _animation2 = Tween<double>(begin: 0, end: -8).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.33, 0.66, curve: Curves.easeInOut),
      ),
    );
    _animation3 = Tween<double>(begin: 0, end: -8).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.66, 1.0, curve: Curves.easeInOut),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Widget _dot(Animation<double> animation) {
    return AnimatedBuilder(
      animation: animation,
      builder: (_, child) =>
          Transform.translate(offset: Offset(0, animation.value), child: child),
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 3),
        width: 10,
        height: 10,
        decoration: BoxDecoration(
          color: AppColors.action,
          shape: BoxShape.circle,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [_dot(_animation1), _dot(_animation2), _dot(_animation3)],
    );
  }
}
