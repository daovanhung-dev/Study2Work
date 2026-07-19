import 'package:flutter/material.dart';
import 'views/dang_nhap/dang_nhap.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import 'views/dang_nhap/quen_mat_khau.dart';
import 'views/dang_nhap/menu.dart';
import 'package:learn2earn/views/dang_nhap/dang_nhap.dart';
Future<void> main() async {

  WidgetsFlutterBinding.ensureInitialized();

  await Supabase.initialize(
    url: 'https://uoefzrjzuytobwuqzkdj.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVvZWZ6cmp6dXl0b2J3dXF6a2RqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyNzM1NDYsImV4cCI6MjA3Mzg0OTU0Nn0.pQv5LwZUPPKwfxuiOLwbrz8VmlDwLFuBxclzixk8XHE',
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'L2E',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: DangNhap(),
    );
  }
}
