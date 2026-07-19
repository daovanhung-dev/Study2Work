import 'package:flutter/material.dart';
class lichPhongVan extends StatefulWidget {
  const lichPhongVan({super.key});

  @override
  State<lichPhongVan> createState() => _lichPhongVanState();
}

class _lichPhongVanState extends State<lichPhongVan> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(backgroundColor: Color(0xFF7ecbff),title: Text("Lịch phỏng vấn"),),
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


