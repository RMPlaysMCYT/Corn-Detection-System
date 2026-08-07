import 'package:flutter/material.dart';

class SortingScreen extends StatefulWidget {
  const SortingScreen({super.key});

  @override
  _SortingScreenState createState() => _SortingScreenState();
}

class _SortingScreenState extends State<SortingScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text('Sorting Screen'),
      ),
    );
  }
}