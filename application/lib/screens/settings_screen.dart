import 'dart:io';
import 'package:cornseedapplication/utilities/texts.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  void _exitApplication() {
    if (Platform.isAndroid) {
      SystemNavigator.pop();
    } else {
      exit(0);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                SettingsPage,
                style: const TextStyle(
                  fontSize: 24.0,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16.0),
              TextButton(
                style: TextButton.styleFrom(
                  alignment: Alignment.centerLeft,
                  padding: EdgeInsets.zero,
                ),
                onPressed: () {},
                child: const Text(
                  'About the System',
                  style: TextStyle(fontSize: 16.0),
                ),
              ),
              const Text(
                'Version 1.0.0',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 12.0),
              // Responsive text wrapping container
              Row(
                children: const [
                  Expanded(
                    child: Text(
                      "Developed by Group 5, in the Compliance for Capstone Project of 'Design and Development of IoT-Enabled Corn Zea Mays Seed Quality Segregation Prototype Using Convolutional Neural Network'",
                      textAlign: TextAlign.start,
                      softWrap: true,
                      style: TextStyle(height: 1.4),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24.0),
              TextButton.icon(
                icon: const Icon(Icons.exit_to_app, color: Colors.red),
                label: const Text(
                  'Exit Application',
                  style: TextStyle(color: Colors.red),
                ),
                onPressed: _exitApplication,
              ),
            ],
          ),
        ),
      ),
    );
  }
}