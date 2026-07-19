import 'package:flutter/material.dart';
class thongTinChiTiet extends StatefulWidget {
  const thongTinChiTiet({super.key});

  @override
  State<thongTinChiTiet> createState() => _thongTinChiTietState();
}

class _thongTinChiTietState extends State<thongTinChiTiet> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(backgroundColor: Color(0xFF7ecbff),title: Text("Thông tin chi tiết"),),
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
              child: Center(
                child: Column(
                  children: [
                  ],
                ),
              ),
            ),
          ],
        ),
      ),

    );
  }
}
