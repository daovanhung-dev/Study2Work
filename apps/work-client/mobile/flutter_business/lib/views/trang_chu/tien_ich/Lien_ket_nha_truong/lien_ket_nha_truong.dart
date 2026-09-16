import 'package:flutter/material.dart';

class LienKetScreen extends StatefulWidget {
  const LienKetScreen({super.key});

  @override
  State<LienKetScreen> createState() => _LienKetScreenState();
}

class _LienKetScreenState extends State<LienKetScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF7ecbff),
        title: Text("Liên kết nhà trường"),
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
