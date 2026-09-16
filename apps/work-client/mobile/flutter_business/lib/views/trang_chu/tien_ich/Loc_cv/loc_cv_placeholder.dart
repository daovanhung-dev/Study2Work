import 'package:flutter/material.dart';

class LocCvPlaceholderScreen extends StatefulWidget {
  const LocCvPlaceholderScreen({super.key});

  @override
  State<LocCvPlaceholderScreen> createState() => _LocCvPlaceholderScreenState();
}

class _LocCvPlaceholderScreenState extends State<LocCvPlaceholderScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(backgroundColor: Color(0xFF7ecbff), title: Text("Lọc CV")),
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
