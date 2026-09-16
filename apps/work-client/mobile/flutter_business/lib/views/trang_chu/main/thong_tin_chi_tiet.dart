import 'package:flutter/material.dart';

class ThongTinChiTiet extends StatefulWidget {
  const ThongTinChiTiet({super.key});

  @override
  State<ThongTinChiTiet> createState() => _ThongTinChiTietState();
}

class _ThongTinChiTietState extends State<ThongTinChiTiet> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF7ecbff),
        title: Text("Thông tin chi tiết"),
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
