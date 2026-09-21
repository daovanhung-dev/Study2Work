import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'views/dang_nhap/dang_nhap.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'S2W',
      theme: AppTheme.light(),
      home: DangNhap(),
    );
  }
}
