import 'dart:async';
import 'package:flutter/material.dart';

class CameraScreen extends StatelessWidget {
  const CameraScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: const EdgeInsets.all(16.0),
        child: Center(
          child: Column(
            children: [
              Container(height: 200, width: 600, color: Colors.blue),
              const SizedBox(height: 20.0),
              
            ],
          ),
        ),
      ),
    );
  }
}
