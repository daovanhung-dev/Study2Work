import 'package:flutter/material.dart';
class thongKe extends StatefulWidget {
  const thongKe({super.key});

  @override
  State<thongKe> createState() => _thongKeState();
}

class _thongKeState extends State<thongKe> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(backgroundColor: Color(0xFF7ecbff),title: Text("Thống kê"),),
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

