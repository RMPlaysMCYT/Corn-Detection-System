import 'package:flutter/material.dart';

class SortingScreenFinished extends StatefulWidget {
  const SortingScreenFinished({super.key});

  @override
  _SortingScreenFinishedState createState() => _SortingScreenFinishedState();
}

class _SortingScreenFinishedState extends State<SortingScreenFinished> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          child: Row(
            children: [
              Text('Sorting Screen Finished')

            ],
          )
        ),
      ),
    );
  }
}