import 'package:flutter/material.dart';

class LichPhongVanScreen extends StatefulWidget {
  const LichPhongVanScreen({super.key});

  @override
  State<LichPhongVanScreen> createState() => _LichPhongVanScreenState();
}

class _LichPhongVanScreenState extends State<LichPhongVanScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF7ecbff),
        title: Text("Lịch phỏng vấn"),
      ),
      body: SizedBox.expand(
        child: Stack(
          children: [
            Container(
              decoration: BoxDecoration(),
              child: Image.asset(
                "assets/bg_trangchu.jpg",
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
