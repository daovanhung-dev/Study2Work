import 'package:flutter/material.dart';
import 'package:study2work_mobile/app/theme/design_tokens.dart';

class LocCvPlaceholderScreen extends StatefulWidget {
  const LocCvPlaceholderScreen({super.key});

  @override
  State<LocCvPlaceholderScreen> createState() => _LocCvPlaceholderScreenState();
}

class _LocCvPlaceholderScreenState extends State<LocCvPlaceholderScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(backgroundColor: AppColors.action, title: Text("Lọc CV")),
      body: SizedBox.expand(
        child: Stack(
          children: [
            Container(
              decoration: BoxDecoration(),
              child: Image.asset(
                "assets/business/bg_trangchu.jpg",
                fit: BoxFit.cover,
                width: double.infinity,
                height: double.infinity,
              ),
            ),
            SingleChildScrollView(
              child: Center(child: Column(children: [])),
            ),
          ],
        ),
      ),
    );
  }
}
