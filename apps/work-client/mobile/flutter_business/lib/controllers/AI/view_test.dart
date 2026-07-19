import 'package:flutter/material.dart';
import 'ai_service.dart';

class AITestScreen extends StatefulWidget {
  const AITestScreen({super.key});

  @override
  State<AITestScreen> createState() => _AITestScreenState();
}

class _AITestScreenState extends State<AITestScreen> {
  final TextEditingController _controller = TextEditingController();
  final AIService _aiService = AIService();
  String _response = '';
  bool _isLoading = false;

  Future<void> _sendToGemini() async {
    if (_controller.text.isEmpty) return;
    setState(() => _isLoading = true);

    final reply = await _aiService.sendMessage(_controller.text);

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
        backgroundColor: Colors.deepPurple,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: 'Nhập câu hỏi...',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _sendToGemini,
              icon: const Icon(Icons.send),
              label: const Text('Gửi đến AI'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                minimumSize: const Size(double.infinity, 48),
              ),
            ),
            const SizedBox(height: 20),
            if (_isLoading)
              const CircularProgressIndicator()
            else
              Expanded(
                child: SingleChildScrollView(
                  child: Text(
                    _response,
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
