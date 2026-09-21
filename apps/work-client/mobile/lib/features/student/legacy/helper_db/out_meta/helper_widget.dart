import 'package:flutter/material.dart';

import 'package:study2work_mobile/app/theme/app_components.dart';
import 'package:study2work_mobile/app/theme/design_tokens.dart';

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
                color: AppColors.navy,
              ),
            ),
            TextSpan(
              text: value ?? "",
              style: const TextStyle(fontSize: 12, color: AppColors.navy),
            ),
          ],
        ),
      ),
      const SizedBox(height: 5),
    ],
  );
}

Widget btnCommon(
  String name,
  VoidCallback onPressed,
  double widthBtn,
  double heightBtn,
) {
  return AppPrimaryButton(label: name, onPressed: onPressed, width: widthBtn, height: heightBtn);
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
      decoration: InputDecoration(labelText: label, prefixIcon: icon != null ? Icon(icon) : null),
  );
}

Widget helperDropdown({
  required String? value,
  required List<String> items,
  required Function(String?) onChanged,
  required String label,
}) {
  return DropdownButtonFormField<String>(
    initialValue: value,
    hint: Text(label),
    decoration: InputDecoration(labelText: label),
    items: items.map((String item) {
      return DropdownMenuItem<String>(value: item, child: Text(item));
    }).toList(),
    onChanged: onChanged,
  );
}
