import 'package:camera/camera.dart';
import 'package:cornseedapplication/utilities/buttons.dart';
import 'package:flutter/material.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});
  @override
  State<CameraScreen> createState() => _CameraStateScreen();
}

class _CameraStateScreen extends State<CameraScreen>{

  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isInitializing = true;
  String? _errorMessage;





  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: const EdgeInsets.all(16.0),
        child: Center(
          child: Column(
            children: [
              Container(height: 200, width: 600, color: Colors.blue),
              const SizedBox(height: 16),
              Group5ButtonBox(text: 'Capture', onPressed: (){})
            ],
          ),
        ),
      ),
    );
  }
}
