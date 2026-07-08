import 'dart:async';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Home")),
      body: Center(child: Column(children: [
        Container(
          padding: const EdgeInsets.all(16.0),
          child: Container(
            width: 300.0,
            height: 160.0,
            color: Colors.blue,
          )
        )
                    ]
                )),
    );
  }
}
