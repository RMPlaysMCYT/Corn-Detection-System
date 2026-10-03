import 'package:flutter/material.dart';
import 'package:tflite_flutter/tflite_flutter.dart';

class MLModelService {
  Interpreter? _interpreter;

  // Asynchronously initialize the interpreter
  Future<void> initializeModel() async {
    try {
      final options = InterpreterOptions()..threads = 4;

      _interpreter = await Interpreter.fromAsset(
        'assets/my_model.tflite', 
        options: options,
      );
      
      print('TFLite Model initialized successfully.');
      
      _inspectTensors();
    } catch (e) {
      print('Failed to initialize TFLite model: $e');
    }
  }

  void _inspectTensors() {
    if (_interpreter == null) return;

    // Read details regarding shape and structure
    var inputTensor = _interpreter!.getInputTensors().first;
    var outputTensor = _interpreter!.getOutputTensors().first;

    print('Input Tensor Shape: ${inputTensor.shape}'); // e.g., [1, 224, 224, 3]
    print('Output Tensor Shape: ${outputTensor.shape}');
  }
  
  // Always close allocated resources to safeguard memory leaks
  void dispose() {
    _interpreter?.close();
  }
}