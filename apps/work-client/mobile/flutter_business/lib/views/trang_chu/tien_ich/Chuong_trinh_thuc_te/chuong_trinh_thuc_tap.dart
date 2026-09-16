import 'package:flutter/material.dart';

class ThucTapScreen extends StatefulWidget {
  const ThucTapScreen({super.key});

  @override
  State<ThucTapScreen> createState() => _ThucTapScreenState();
}

class _ThucTapScreenState extends State<ThucTapScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF7ecbff),
        title: Text("Chương trình thực tập"),
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
