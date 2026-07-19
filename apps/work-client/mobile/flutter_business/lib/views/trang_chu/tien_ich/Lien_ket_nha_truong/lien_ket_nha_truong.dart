import 'package:flutter/material.dart';
class lienKet extends StatefulWidget {
  const lienKet({super.key});

  @override
  State<lienKet> createState() => _lienKetState();
}

class _lienKetState extends State<lienKet> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(backgroundColor: Color(0xFF7ecbff),title: Text("Liên kết nhà trường"),),
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


