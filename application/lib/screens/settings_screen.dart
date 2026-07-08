import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});


  // Add Keys anyway:

  void _exitApplication() {
    if (Platform.isAndroid) {
      SystemNavigator.pop(); 
    } else if (Platform.isIOS) {
      exit(0); 
    } else {
      exit(0);
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            Row(
              children: [
                TextButton(
                  style: TextButton.styleFrom(
                    fixedSize: const Size(200, 50), // Width: 200, Height: 50
                  ),
                  onPressed: () {},
                  child: const Text('About'),
                ),
              ],
            ),
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(4.0),
                  child: Text("Version 1.0.0", textAlign: TextAlign.start),
                ),
              ],
            ),
            Row(
              children: [
                Container(
                  width: 600.0,
                  padding: const EdgeInsets.all(4.0),
                  child: Text(
                    "Developed by Group 5, in the Compliance for Capstone Project of 'Design and Development of IoT-Enabled Corn Zea Mays Seed Quality Segregation Prototype Using Convolutional Neural Network",
                    textAlign: TextAlign.start,
                  ),
                ),
              ],
            ),
            Row(
              children: [
                TextButton(
                  style: TextButton.styleFrom(
                    fixedSize: const Size(200, 50), // Width: 200, Height: 50
                  ),
                  onPressed: () {
                    _exitApplication();
                  },
                  child: const Text('Exit Application'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
