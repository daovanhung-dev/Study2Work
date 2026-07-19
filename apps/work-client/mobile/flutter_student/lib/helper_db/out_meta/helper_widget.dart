import 'package:flutter/material.dart';

Widget buildRich(String label, String? value) {
  return Column(
    children: [
      RichText(
        text: TextSpan(
          children: [
            TextSpan(
              text: "$label: ",
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            TextSpan(
              text: value ?? "",
              style: const TextStyle(fontSize: 12, color: Colors.black),
            ),
          ],
        ),
      ),
      SizedBox(height: 5),
    ],
  );
}

Widget btn_common(
  String name,
  VoidCallback onPressed,
  double width_btn,
  double height_btn,
) {
  return SizedBox(
    width: width_btn,
    height: height_btn,
    child: ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.blue,
        // 🌊 màu nền xanh
        foregroundColor: Colors.white,
        // chữ trắng
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12), // bo góc mềm mại
        ),
        elevation: 4, // bóng đổ nhẹ
      ),
      onPressed: onPressed,
      child: Text(
        "$name",
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
    ),
  );
}
Widget helperTextField({
  required TextEditingController controller,
  required String label,
  IconData? icon,
  bool isPassword = false,
  TextInputType keyboardType = TextInputType.text,
}) {
  return TextField(
    controller: controller,
    obscureText: isPassword,
    keyboardType: keyboardType,
    decoration: InputDecoration(
      labelText: label,
      prefixIcon: icon != null ? Icon(icon) : null,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
    ),
  );
}

Widget helperDropdown({
  required String? value,
  required List<String> items,
  required Function(String?) onChanged,
  required String label,
}) {
  return DropdownButtonFormField<String>(
    value: value,
    hint: Text(label),
    decoration: InputDecoration(
      labelText: label,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
    ),
    items: items.map((String item) {
      return DropdownMenuItem<String>(
        value: item,
        child: Text(item),
      );
    }).toList(),
    onChanged: onChanged,
  );
}
