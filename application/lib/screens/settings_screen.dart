import 'dart:async';
import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Settings")),
      body: Center(
        child: Column(
          children: [
            Row(
              children: [TextButton(onPressed: () {}, child: Text("About"))],
            ),
          ],
        ),
      ),
    );
  }
}
