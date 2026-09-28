import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:study2work_mobile/app/theme/design_tokens.dart';
import 'package:study2work_mobile/shared/providers/app_providers.dart';

class AITestScreen extends ConsumerStatefulWidget {
  const AITestScreen({super.key});

  @override
  ConsumerState<AITestScreen> createState() => _AITestScreenState();
}

class _AITestScreenState extends ConsumerState<AITestScreen> {
  final TextEditingController _controller = TextEditingController();
  String _response = '';
  bool _isLoading = false;

  Future<void> _sendToGemini() async {
    if (_controller.text.isEmpty) return;
    setState(() => _isLoading = true);

    final reply = await ref.read(geminiClientProvider).sendMessage(_controller.text);

    setState(() {
      _response = reply;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Trợ lý AI (Gemini)'),
        backgroundColor: AppColors.primary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: 'Nhập câu hỏi...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _sendToGemini,
              icon: const Icon(Icons.send),
              label: const Text('Gửi đến AI'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.action,
                minimumSize: const Size(double.infinity, 48),
              ),
            ),
            const SizedBox(height: 20),
            if (_isLoading)
              const CircularProgressIndicator()
            else
              Expanded(
                child: SingleChildScrollView(
                  child: Text(_response, style: const TextStyle(fontSize: 16)),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
