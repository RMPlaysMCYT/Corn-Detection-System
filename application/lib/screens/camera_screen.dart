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
          _cameras![0],
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
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _captureAndScan() async {
    if (_controller == null || !_controller!.value.isInitialized) return;

    try {
      final XFile image = await _controller!.takePicture();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Captured corn seed image: ${image.path}')),
        );
        // Pass image.path to your CNN classification model pipeline here
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error taking picture: $e')),
        );
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
              Container(
                height: 200, 
                width: 600, 
                color: Colors.blue,
                clipBehavior: Clip.antiAlias,
                child: _buildCameraPreview(),
              ),
              const SizedBox(height: 16),
              Group5ButtonBox(
                text: 'Capture', 
                onPressed: _controller != null && _controller!.value.isInitialized
                  ? _captureAndScan
                  : () {},
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCameraPreview(){
    if (_isInitializing){
      return const Center(
        child: CircularProgressIndicator(color: Colors.red,),
      );
    }

    if(_errorMessage != null){
      return Center(
        child: Text(
          _errorMessage!,
          style: const TextStyle(color: Colors.green),
          textAlign: TextAlign.center,
        ),
      );
    }
    if (_controller != null && _controller!.value.isInitialized) {
      return AspectRatio(
        aspectRatio: _controller!.value.aspectRatio,
        child: CameraPreview(_controller!),
      );
    }

    return const Center(
      child: Text(
        'Camera is not available',
        style: TextStyle(color: Colors.white),
      ),
    );
  }
}
