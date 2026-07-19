import 'package:flutter/material.dart';
class XemChiTiet extends StatefulWidget {
  const XemChiTiet({super.key});

  @override
  State<XemChiTiet> createState() => _XemChiTietState();
}

class _XemChiTietState extends State<XemChiTiet> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF7ecbff),
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
            Padding(
              padding: EdgeInsets.all(10),
              child: Center(
                child: SingleChildScrollView(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      //Danh sach tuyen dung
                      Container(
                        width: 320,
                        height: 700,
                        padding: EdgeInsets.symmetric(
                          vertical: 20,
                          horizontal: 20,
                        ),
                        margin: EdgeInsets.symmetric(vertical: 20),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(20),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.1),
                              spreadRadius: 5,
                              blurRadius: 7,
                              offset: Offset(0, 3),
                            ),
                          ],
                        ),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
