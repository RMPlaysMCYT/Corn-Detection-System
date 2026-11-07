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
  void initState(){
    super.initState();
    _initializeCameras();
  }

  Future<void> _initializeCameras() async{
    try{
      _cameras = await availableCameras();
      if (_cameras != null && _cameras!.isNotEmpty){
        _controller = CameraController(
          _cameras[0],
          ResolutionPreset.medium,
          enableAudio: false
          );
      }
    } catch (e) {
      _errorMessage = 'Failed to load camera: $e';
    } finally {
      if (mounted) {
        setState(() {
          _isInitializing = false;
        });
      }
    }
  }

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
